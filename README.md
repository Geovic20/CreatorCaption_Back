# CreatorCaption – Backend API

Backend du SaaS *CreatorCaption*, une plateforme alimentée par l’IA qui aide les créateurs de contenu à générer des légendes optimisées et engageantes pour les réseaux sociaux.

---

## Fonctionnalités principales

* 🔐 Authentification JWT (login / register)
* 🤖 Génération de légendes via IA (multi-provider)
* 🧾 Historique des générations
* 📊 Dashboard utilisateur (statistiques)
* ⚡ Système de quotas (Free vs Pro)
* 💳 Upgrade mock (simulation d’abonnement)
* 🧠 Architecture multi-LLM (OpenAI + Gemini)

---

## 🏗️ Architecture

Projet basé sur un *monolith modulaire Django*, prêt pour une évolution vers micro-services.

```
apps/
├── users/
├── billing/
├── ai_engine/
├── content/
├── analytics/
├── notifications/
└── core/
```

### 🔹 Focus `ai_engine`

```
services/
├── providers/
│   ├── base.py
│   ├── openai_provider.py
│   └── gemini_provider.py
└── ai_router.py
```

👉 Permet de switcher facilement entre plusieurs modèles IA.

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Geovic20/CreatorCaption_Back
cd creatorcaption-backend
```

### 2. Créer l’environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement

Créer un fichier `.env` :

```
SECRET_KEY=your_secret_key

OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

AI_PROVIDER=gemini
```

---

### 5. Migrer la base de données

```bash
python manage.py migrate --settings=config.settings.local
```

---

### 6. Lancer le serveur

```bash
python manage.py runserver --settings=config.settings.local
```

---

## 🔌 Endpoints principaux

### Auth

```
POST /api/auth/login/
POST /api/auth/register/
```

---

### IA

```
POST /api/ai/captions/generate/
GET  /api/ai/history/
```

---

### Dashboard

```
GET /api/analytics/user/
```

---

### Billing (mock)

```
POST /api/billing/upgrade/
```

---

## Choix techniques

* Django + Django REST Framework
* Architecture modulaire (domain-driven)
* Multi-provider IA (OpenAI + Gemini)
* JSONField pour stockage flexible
* Environnement sécurisé via `.env`

---

## Sécurité

* Authentification JWT
* Protection des clés API
* Validation des données côté backend
* Gestion des erreurs sécurisée

---

## Améliorations futures

* Intégration Stripe / Mobile Money
* Génération de hashtags
* Planner éditorial
* Thumbnails YouTube
* Rate limiting avancé

---

## Auteur

Projet développé dans une optique **SaaS + portfolio**, mettant en avant des compétences fullstack, architecture et intégration IA.
