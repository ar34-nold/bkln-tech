# Centrafrique Connect - Plateforme Officielle de Services Gouvernementaux

**Légalisation, authentification de documents officiels et casier judiciaire en ligne pour la République Centrafricaine.**

## 📋 Vue d'ensemble

Centrafrique Connect est une application web Django moderne qui centralise les services de:
- **Légalisation** de documents officiels
- **Authentification** de documents avec QR code
- **Casier judiciaire** en ligne
- **Vérification publique** d'authenticité

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.10+
- Django 6.0+
- PostgreSQL 13+ (production) ou SQLite (développement)
- Git

### Installation locale

1. **Cloner le dépôt**
```bash
git clone https://github.com/YOUR_USERNAME/centrafrique-connect.git
cd centrafrique-connect
```

2. **Créer un environnement virtuel** (optionnel mais recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Créer un fichier .env (ou utiliser variables d'env système)
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Appliquer les migrations**
```bash
python manage.py migrate
```

6. **Créer un super utilisateur**
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

Accès: http://localhost:8000

## 📁 Structure du Projet

```
centrafrique-connect/
├── bkln_tech/                  # Configuration Django principale
│   ├── settings.py             # Paramètres globaux
│   ├── urls.py                 # Routes principales
│   ├── wsgi.py                 # Déploiement WSGI
│   └── asgi.py                 # Déploiement ASGI
├── connect/                    # Application Centrafrique Connect
│   ├── models.py              # Modèles (UserProfile, DocumentRequest, etc.)
│   ├── views.py               # Vues web
│   ├── api_views.py           # Endpoints API REST
│   ├── forms.py               # Formulaires
│   ├── serializers.py         # Sérialiseurs DRF
│   ├── urls.py                # Routes web
│   ├── api_urls.py            # Routes API
│   ├── admin.py               # Configuration admin
│   ├── models.py              # Modèles de données
│   └── migrations/            # Fichiers de migration
├── operations/                 # App existante (services IT)
├── templates/                  # Modèles HTML
│   ├── connect/
│   │   ├── base.html          # Template de base
│   │   ├── home.html          # Page d'accueil
│   │   ├── register.html      # Inscription
│   │   ├── login.html         # Connexion
│   │   ├── dashboard.html     # Tableau de bord
│   │   └── ...                # Autres templates
│   └── registration/          # Templates d'authentification
├── static/                     # Fichiers statiques
│   ├── css/
│   │   ├── app.css            # Styles principaux
│   │   └── centrafrique.css   # Styles personnalisés
│   └── img/
├── media/                      # Fichiers uploadés utilisateurs
├── requirements.txt            # Dépendances Python
├── manage.py                   # Outil de gestion Django
├── .env                        # Variables d'environnement (⚠️ non commité)
├── RENDER_DEPLOYMENT_FR.md    # Guide de déploiement sur Render
└── TEST_CHECKLIST_FR.md       # Checklist de test
```

## 🔑 Fonctionnalités Principales

### 1. Inscription et Authentification
- Inscription sécurisée avec validation d'email
- Profils utilisateur avec rôles (citoyen, agent, admin)
- Authentification JWT pour l'API
- Récupération de mot de passe

### 2. Demandes de Légalisation
- Soumission de documents avec description
- Génération automatique de QR codes
- Export PDF avec référence unique
- Suivi du statut (soumis, validé, traité)
- Historique des demandes

### 3. Casier Judiciaire
- Formulaire d'information personnelle
- Gestion de paiement (unpaid, pending, paid)
- Génération de document PDF
- Suivi d'état

### 4. Vérification Publique
- Vérification sans authentification
- Accès par code unique
- Confirmation d'authenticité

### 5. Admin Django
- Gestion complète des utilisateurs
- Modération des demandes
- Gestion des rôles et permissions
- Logs d'activité

### 6. API REST
- Endpoints JWT authentifiés
- Endpoints publics pour vérification
- Sérialisation JSON
- Documentation auto-générée

## 🛠️ Technologies

- **Backend**: Django 6.0+
- **API**: Django REST Framework + SimpleJWT
- **Frontend**: Bootstrap 5
- **Base de données**: SQLite (dev), PostgreSQL (prod)
- **Documents**: ReportLab (PDF), QRcode
- **Authentification**: JWT
- **Serveur**: Gunicorn (prod), Django dev (dev)
- **Static Files**: Whitenoise

## 📦 Dépendances Principales

```
Django>=5.0,<6.0
djangorestframework>=3.15.0
djangorestframework-simplejwt>=2.0.0
django-bootstrap5>=23.0
dj-database-url>=1.0
python-dotenv>=1.0
gunicorn>=20.0
whitenoise>=6.0
psycopg[binary]>=3.1
reportlab>=4.0
qrcode>=7.4
Pillow>=10.0
```

## 🚢 Déploiement

### Sur Render

Voir le fichier [RENDER_DEPLOYMENT_FR.md](RENDER_DEPLOYMENT_FR.md) pour le guide complet.

**Résumé**:
1. Pusher sur GitHub
2. Créer un service Web sur Render
3. Créer une base PostgreSQL
4. Configurer les variables d'environnement
5. Render déploie automatiquement

### Localement via Docker (optionnel)

```bash
# Créer image Docker
docker build -t centrafrique-connect .

# Lancer le conteneur
docker run -e DEBUG=False -p 8000:8000 centrafrique-connect
```

## 📝 Modèles de Données

### UserProfile
```python
user: OneToOneField(User)
role: Choix (citizen, agent, admin)
telephone: CharField
organisation: CharField
```

### DocumentRequest
```python
citizen: ForeignKey(User)
titre: CharField
description: TextField
fichier: FileField
statut: Choix (draft, submitted, validated, rejected, processed)
verification_code: CharField (généré automatiquement)
qr_code: ImageField
document_pdf: FileField
```

### CriminalRecordRequest
```python
citizen: ForeignKey(User)
date_naissance: DateField
lieu_naissance: CharField
motif: CharField
statut: Choix (new, review, approved, rejected)
paiement: Choix (unpaid, pending, paid)
```

## 🔒 Sécurité

- Passwords hashés avec PBKDF2
- CSRF protection activée
- SQL injection prévenue via ORM
- XSS protection via Django templates
- JWT tokens pour API
- HTTPS obligatoire en production
- Validation des uploads
- Gestion des permissions par rôle

## 📊 Admin Django

Accès: http://localhost:8000/admin/
- **Identifiants**: super utilisateur créé lors du `createsuperuser`

### Pages disponibles:
- Utilisateurs et Profils
- Demandes de Légalisation
- Demandes de Casier
- Logs d'activité

## 🧪 Tests

Voir [TEST_CHECKLIST_FR.md](TEST_CHECKLIST_FR.md) pour la checklist complète.

```bash
# Lancer les tests Django
python manage.py test

# Avec couverture
coverage run --source='.' manage.py test
coverage report
```

## 🐛 Dépannage

### Erreur: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Base de données vide
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Port 8000 déjà utilisé
```bash
python manage.py runserver 8001
```

### Problème d'authentification
- Vérifier que le JWT_SECRET_KEY est configuré
- Renouveler les tokens JWT

## 📚 Documentation

- [Django Docs](https://docs.djangoproject.com/en/6.0/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Render Docs](https://render.com/docs)

## 👥 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committer les changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

© 2026 Centrafrique Connect. Tous droits réservés.

## 📧 Support

Pour toute question ou problème:
- Email: support@centrafrique-connect.com
- Issues: GitHub Issues
- Documentation: Ce README + fichiers docs

---

**Version**: 1.0.0  
**Dernière mise à jour**: 2026-05-26  
**Status**: Production Ready
