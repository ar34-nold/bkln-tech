# Guide Complet de Déploiement Centrafrique Connect sur Render

## 1. Préparation du projet

### 1.1 Vérifications locales
```bash
# Vérifier que tout fonctionne localement
python manage.py check
python manage.py migrate
python manage.py runserver
```

### 1.2 Configuration Git
```bash
git init
git add .
git commit -m "Initial commit: Centrafrique Connect app"
git remote add origin https://github.com/YOUR_USERNAME/centrafrique-connect.git
git push -u origin main
```

## 2. Configuration Render

### 2.1 Prérequis
- Compte Render (render.com)
- Compte GitHub avec votre dépôt pushé
- Domaine personnalisé (optionnel)

### 2.2 Créer un Service Web sur Render

1. **Aller sur Dashboard Render**: https://dashboard.render.com
2. **Créer un nouveau Web Service**:
   - Cliquer "New +" → "Web Service"
   - Connecter votre compte GitHub
   - Sélectionner le dépôt `centrafrique-connect`
   - Configurer les paramètres:
     - **Name**: `centrafrique-connect`
     - **Region**: `frankfurt` (Europe, proche de la Centrafrique)
     - **Branch**: `main`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - **Start Command**: `gunicorn bkln_tech.wsgi`

### 2.3 Créer une Base de Données PostgreSQL

1. **Sur Render Dashboard**:
   - Cliquer "New +" → "PostgreSQL"
   - **Name**: `centrafrique-connect-db`
   - **Region**: `frankfurt`
   - **PostgreSQL Version**: 15
   - **Plan**: Free (ou Starter $15/mois)

2. **Copier la connection string** (elle apparaîtra après création)

### 2.4 Configurer les Variables d'Environnement

Sur la page du Web Service Render, aller à "Environment":

```
# Django
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=centrafrique-connect.onrender.com,www.centrafrique-connect.onrender.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email (optionnel, avec SendGrid)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@centrafrique-connect.com

# AWS S3 (optionnel, pour stockage média)
USE_S3=False
# Si True, ajouter:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# AWS_STORAGE_BUCKET_NAME=...
# AWS_S3_REGION_NAME=us-east-1
```

## 3. Déploiement

### 3.1 Déployer via Git Push
Après la configuration du service:
```bash
git push origin main
```
Render détectera les changements et lancera automatiquement le déploiement.

### 3.2 Suivre le déploiement
- Sur le Dashboard Render, accéder au service
- Voir la progression dans l'onglet "Logs"
- La URL sera: `https://centrafrique-connect.onrender.com`

## 4. Vérifications Post-Déploiement

### 4.1 Tests d'accès
```bash
# Vérifier que le site fonctionne
curl https://centrafrique-connect.onrender.com/

# Vérifier l'accès admin
https://centrafrique-connect.onrender.com/admin/
```

### 4.2 Créer un super utilisateur
```bash
# Via SSH sur Render (dans les logs ou via shell)
python manage.py createsuperuser
```

### 4.3 Tester les endpoints
- **Accueil**: https://centrafrique-connect.onrender.com/
- **Inscription**: https://centrafrique-connect.onrender.com/inscription/
- **Admin**: https://centrafrique-connect.onrender.com/admin/
- **API**: https://centrafrique-connect.onrender.com/api/

## 5. Configuration du Domaine Personnalisé

### 5.1 Sur Render
1. Aller à Settings du service
2. Custom Domain
3. Entrer votre domaine: `centrafrique-connect.com`
4. Copier les serveurs DNS Render

### 5.2 Chez votre registraire de domaine
1. Aller à la gestion DNS
2. Ajouter les enregistrements DNS fournis par Render
3. Attendre la propagation (jusqu'à 24h)

### 5.3 HTTPS automatique
- Render génère automatiquement un certificat SSL
- Le site sera accessible via `https://centrafrique-connect.com`

## 6. Maintenance

### 6.1 Logs en temps réel
```bash
# Via Render Dashboard
Services → centrafrique-connect → Logs
```

### 6.2 Mises à jour
```bash
# Faire les modifications localement
git add .
git commit -m "Update: description du changement"
git push origin main
# Render redéploiera automatiquement
```

### 6.3 Base de données
- **Backups**: Render propose des backups automatiques
- **Accès**: Télécharger les credentials PostgreSQL du Dashboard

### 6.4 Redémarrer le service
- Dashboard → Service → "Manual Deploy" (en haut à droite)

## 7. Dépannage Courant

### Erreur: ModuleNotFoundError
- Vérifier que tous les packages sont dans `requirements.txt`
- Relancer le déploiement

### Base de données vide après déploiement
- Les migrations s'exécutent automatiquement
- Si ce n'est pas le cas, exécuter manuellement via les logs

### Erreur 500
- Vérifier les logs Render
- Vérifier que SECRET_KEY et DATABASE_URL sont configurés
- S'assurer que DEBUG=False et ALLOWED_HOSTS contient le domaine

### Fichiers uploadés non persistants
- Render supprime les fichiers uploadés après redémarrage
- Utiliser AWS S3 (configure USE_S3=True) ou Render Disk (payant)

## 8. Sécurité

### 8.1 Avant la production
- [ ] SECRET_KEY: Générer une nouvelle clé forte
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS: Configurer le domaine réel
- [ ] HTTPS: Activé automatiquement par Render
- [ ] Database password: Changer le mot de passe PostgreSQL
- [ ] Email: Configurer un service (SendGrid, etc.)

### 8.2 Bonnes pratiques
- Jamais committer les secrets dans Git
- Utiliser les variables d'environnement Render
- Activer 2FA sur GitHub et Render
- Sauvegarder régulièrement la base de données

## 9. Support et Ressources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/6.0/howto/deployment/
- **PostgreSQL on Render**: https://render.com/docs/databases
- **Custom Domains**: https://render.com/docs/custom-domains

---

**Note**: Ce guide suppose que votre projet est commité sur GitHub et prêt pour le déploiement. Pour questions, consulter la documentation officielle de Render ou Django.
