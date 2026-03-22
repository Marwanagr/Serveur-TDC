from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from datetime import datetime
import base64
import os
import uuid
from services.watermark_svc import apply_watermark, extract_watermark
from db import keys_col, posts_col, users_col, views_col
from core.security import verify_token
from services.crypto import encrypt_image, decrypt_image

router = APIRouter()


@router.get("/posts/all")
def get_all_posts():
    try:
        posts = posts_col.find({}, {"_id": 0})
        result = []
        for post in posts:
            key_data = keys_col.find_one({"image_id": post["image_id"]}, {"_id": 0})
            result.append({
                "image_id": post["image_id"],
                "caption": post.get("caption", ""),
                "owner_username": key_data.get("owner_username", "") if key_data else "",
                "image": post["image"],
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_post")
async def add_post(
    user_id: str = Form(...),
    owner_username: str = Form(...),
    token: str = Form(...),
    caption: str = Form(...),
    image: UploadFile = File(...),
    authorized_users: str = Form(default="")
):
    try:
        if not verify_token(owner_username, token):
            raise HTTPException(status_code=403, detail="Token invalide ou expiré.")

        authorized_list = (
            [] if authorized_users.strip() == ""
            else [u.strip() for u in authorized_users.split(",") if u.strip()]
        )

        invalid_users = [u for u in authorized_list if not users_col.find_one({"username": u})]
        if invalid_users:
            raise HTTPException(status_code=404, detail=f"Utilisateurs introuvables : {invalid_users}")

        content = await image.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image trop lourde (max 10MB).")

        image_id = str(uuid.uuid4())
        generated_key = base64.b64encode(os.urandom(32)).decode()
        encrypted_image = encrypt_image(content, generated_key)

        posts_col.insert_one({
            "image_id": image_id,
            "user_id": user_id,
            "caption": caption,
            "image": encrypted_image
        })

        keys_col.insert_one({
            "image_id": image_id,
            "user_id": user_id,
            "owner_username": owner_username,
            "key": generated_key,
            "valid": True,
            "autorisations": authorized_list,
            "created_at": datetime.utcnow()
        })

        return {
            "message": "Publication ajoutée avec succès.",
            "image_id": image_id,
            "autorisations": authorized_list
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/posts/{image_id}")
def get_post(image_id: str, payload: dict = Body(default={})):
    try:
        username = payload.get("username")
        token = payload.get("token")

        post = posts_col.find_one({"image_id": image_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post non trouvé.")

        key_data = keys_col.find_one({"image_id": image_id})
        if not key_data:
            raise HTTPException(status_code=404, detail="Clé non trouvée.")

        is_owner = username == key_data["owner_username"]
        is_authorized = username in key_data.get("autorisations", [])
        has_valid_token = username and token and verify_token(username, token)

        if has_valid_token and (is_owner or is_authorized):
            decrypted_bytes = decrypt_image(post["image"], key_data["key"])
            watermarked_b64 = apply_watermark(decrypted_bytes, username)
            watermarked_bytes = base64.b64decode(watermarked_b64)

            # Enregistrement dans la table de traçabilité
            if username != key_data["owner_username"]:
                views_col.insert_one({
                    "image_id": image_id,
                    "viewer_username": username,
                    "owner_username": key_data["owner_username"],
                    "viewed_at": datetime.utcnow(),
                    "original_image": base64.b64encode(decrypted_bytes).decode(),
                    "watermarked_image": base64.b64encode(watermarked_bytes).decode(),
                })

            return {
                "image_id": image_id,
                "caption": post["caption"],
                "image": base64.b64encode(watermarked_bytes).decode(),
                "decrypted": True
            }
        else:
            return {
                "image_id": image_id,
                "caption": post["caption"],
                "image": post["image"],
                "decrypted": False
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/views/{image_id}")
def get_views(image_id: str):
    try:
        key_data = keys_col.find_one({"image_id": image_id})
        if not key_data:
            raise HTTPException(status_code=404, detail="Image non trouvée.")

        views = views_col.find(
            {"image_id": image_id},
            {"_id": 0, "viewer_username": 1, "viewed_at": 1}
        ).sort("viewed_at", -1)

        return {
            "image_id": image_id,
            "views": [
                {
                    "viewer_username": v["viewer_username"],
                    "viewed_at": v["viewed_at"].isoformat()
                }
                for v in views
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/views/verify/{image_id}/{viewer_username}")
def verify_view(image_id: str, viewer_username: str):
    try:
        view = views_col.find_one(
            {"image_id": image_id, "viewer_username": viewer_username},
            sort=[("viewed_at", -1)]
        )
        if not view:
            raise HTTPException(status_code=404, detail="Aucune vue trouvée pour cet utilisateur.")

        original_bytes = base64.b64decode(view["original_image"])
        watermarked_bytes = base64.b64decode(view["watermarked_image"])

        extracted = extract_watermark(original_bytes, watermarked_bytes)

        return {
            "image_id": image_id,
            "viewer_username": viewer_username,
            "viewed_at": view["viewed_at"].isoformat(),
            "extracted_watermark": extracted,
            "match": extracted == viewer_username
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))