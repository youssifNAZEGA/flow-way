# 🚗 FlowWay Backend API

## 📌 Description

FlowWay est une plateforme intelligente de gestion de péage basée sur la reconnaissance automatique des plaques d’immatriculation.

Ce backend, développé avec FastAPI, permet de :

* gérer les utilisateurs (passagers, agents, admin)
* gérer les véhicules et leurs plaques
* traiter les passages aux péages
* gérer les comptes et transactions
* sécuriser l’accès via authentification JWT

---

## 🏗️ Architecture du projet

```
backendFlowWay/
│
├── api/                # Routes API
│   └── endpoints/
│
├── core/               # Sécurité, config
│
├── db/                 # Connexion base de données
│
├── models/             # Modèles SQLAlchemy
│
├── schemas/            # Schémas Pydantic
│
├── services/           # Logique métier
│
├── main.py             # Point d’entrée FastAPI
│
└── .env                # Variables d’environnement
```

---

## ⚙️ Technologies utilisées

* Python 3.10+
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT (authentification)
* Uvicorn

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <repo_url>
cd backendFlowWay
```

---

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 4. Configurer les variables d’environnement

Créer un fichier `.env` à la racine :

```
DATABASE_URL=postgresql://peage_user:peage_pass@localhost/peage_db
SECRET_KEY=supersecret
```

---

### 5. Lancer le serveur

```bash
uvicorn main:app --reload
```

---

## 📡 Documentation API

Une fois le serveur lancé :

👉 Swagger UI :

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentification

Le système utilise JWT.

### 🔑 Login

```
POST /auth/login
```

Retourne un token.

---

### 🔒 Routes protégées

Ajouter dans les headers :

```
Authorization: Bearer <token>
```

---

## 🧪 Exemple de test

### Login

```json
{
  "email": "test@test.com",
  "password": "1234"
}
```

---

## 📊 Modules principaux

* 👤 Utilisateurs
* 🚗 Véhicules
* 🚧 Passages
* 💳 Comptes
* 💰 Transactions
* 🛣️ Sites de péage
* 🔔 Notifications
* ⚖️ Litiges

---

## 👨‍💻 Contribution

1. Créer une branche :

```bash
git checkout -b feature/nom-feature
```

2. Commit :

```bash
git commit -m "feat: description"
```

3. Push :

```bash
git push origin feature/nom-feature
```

---

## ⚠️ Bonnes pratiques

* Ne pas push le fichier `.env`
* Utiliser des branches pour chaque fonctionnalité
* Respecter la structure du projet

---

## 📌 Auteur

Projet réalisé par l’équipe FlowWay 🚀

---

## 🔥 Statut du projet

🟢 En cours de développement

```
```
