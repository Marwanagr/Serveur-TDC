# 🔐 Sovrizon V2 — Serveur Tiers de Confiance

Ce dépôt contient le code source du **serveur tiers de confiance** pour le projet **Sovrizon V2**, un système décentralisé de gestion et de partage sécurisé des données personnelles.

---

## 🎯 Objectif

Le tiers de confiance est un composant essentiel du système Sovrizon. Il est responsable de :

- 🔑 **Génération de clés de chiffrement** pour les images (AES-256-GCM)
- 💾 **Stockage sécurisé des clés** dans une base de données MongoDB
- 👤 **Gestion des utilisateurs** : inscription, connexion, authentification via tokens
- 🛡️ **Contrôle d'accès granulaire** : autorisation et révocation d'accès par utilisateur
- 🔄 **Chiffrement/Déchiffrement automatique** des images stockées
- 🎨 **Filigrane DCT** pour la traçabilité des images
- 📝 **Publication sécurisée de posts** avec autorisations conditionnelles

---

## 🧱 Technologies

| Catégorie | Technologies |
|---|---|
| **Backend** | Python, FastAPI |
| **Base de données** | MongoDB |
| **Sécurité** | AES-256-GCM (AEAD), JWT (24h), bcrypt, Filigrane DCT |
| **Traitement d'images** | OpenCV, NumPy |

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Marwanagr/Serveur-TDC.git
cd Serveur-TDC
```

### 2. Configuration de MongoDB

**Option A : MongoDB Atlas (Cloud) — Recommandé**

1. Créez un compte sur [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Créez un cluster gratuit
3. Copiez votre URI de connexion

**Option B : MongoDB Local**

Installation :

```bash
# Sur Windows
choco install mongodb

# Sur macOS
brew install mongodb-community

# Sur Linux (Ubuntu/Debian)
sudo apt-get install -y mongodb
```

Démarrer le service :

```bash
# Windows
mongod --dbpath "C:\data\db"

# macOS/Linux
mongod --dbpath /usr/local/var/mongodb
```

Créer un utilisateur (local) :

```bash
mongosh
use admin
db.createUser({ user: "admin", pwd: "password", roles: ["root"] })
```

### 3. Configuration du fichier `.env`

Créez un fichier `.env` à la racine du projet :

```env
# MongoDB Atlas (Cloud)
MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/tiers-de-confiance?retryWrites=true&w=majority"

# Ou MongoDB Local
# MONGO_URI="mongodb://admin:password@localhost:27017"

PORT=8300
```

### 4. Créer un environnement virtuel et lancer l'application

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
.\venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn main:app --reload --port 8300
```

L'application sera accessible sur : **http://localhost:8300**  
Interface interactive : **http://localhost:8300/docs** (Swagger UI)

---

## 📁 Structure du projet

```
Serveur-TDC/
├── main.py                  # Point d'entrée de l'application FastAPI
├── requirements.txt         # Dépendances Python
├── .env                     # Variables d'environnement (non versionné)
├── WatermarkingModule/      # Module de filigrane DCT
├── core/                    # Logique centrale (config, sécurité, JWT...)
├── db/                      # Connexion et modèles MongoDB
├── routers/                 # Routes FastAPI (endpoints)
└── services/                # Services métier (chiffrement, accès...)
```

---

## 👤 Auteur

**Marwan** — [@Marwanagr](https://github.com/Marwanagr)
