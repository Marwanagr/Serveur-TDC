# 🛡️ Serveur-TDC

Serveur backend Python pour la **protection de contenu numérique par tatouage (watermarking)**. Développé avec **FastAPI**, il expose une API REST permettant d'intégrer, détecter et vérifier des filigranes numériques dans des fichiers, avec gestion des utilisateurs et persistance via MongoDB.

---

## 📁 Structure du projet

```
Serveur-TDC/
├── main.py                  # Point d'entrée de l'application FastAPI
├── requirements.txt         # Dépendances Python
├── .env                     # Variables d'environnement (non versionné)
├── WatermarkingModule/      # Module de tatouage numérique
├── core/                    # Logique centrale (config, sécurité...)
├── db/                      # Connexion et modèles MongoDB
├── routers/                 # Routes FastAPI (endpoints)
└── services/                # Services métier
```

---

## 🚀 Installation

### Prérequis

- Python 3.9+
- MongoDB (local ou cloud)

### 1. Cloner le repo

```bash
git clone https://github.com/Marwanagr/Serveur-TDC.git
cd Serveur-TDC
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Crée un fichier `.env` à la racine du projet :

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=serveur_tdc
SECRET_KEY=your_secret_key
```

### 5. Lancer le serveur

```bash
uvicorn main:app --reload
```

L'API est accessible sur [http://localhost:8000](http://localhost:8000).  
La documentation interactive Swagger est disponible sur [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🔧 Technologies utilisées

| Technologie | Rôle |
|---|---|
| **FastAPI** | Framework web Python (API REST) |
| **MongoDB / PyMongo** | Base de données NoSQL |
| **OpenCV** | Traitement d'images pour le watermarking |
| **Reed-Solomon (reedsolo)** | Encodage robuste des données du filigrane |
| **NumPy / SciPy** | Calculs scientifiques pour le watermarking |
| **Cryptography / Passlib** | Sécurité et hachage des mots de passe |
| **python-dotenv** | Gestion des variables d'environnement |

---

## 📌 Fonctionnalités

- ✅ Intégration d'un tatouage numérique dans des fichiers
- ✅ Détection et extraction du filigrane
- ✅ Authentification des utilisateurs (JWT / bcrypt)
- ✅ Persistance des données via MongoDB
- ✅ API REST documentée (Swagger / ReDoc)

---

## 👤 Auteur

**Marwan** — [@Marwanagr](https://github.com/Marwanagr)
