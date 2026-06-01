# Guide: Préparation Git pour Déploiement Render

## 1️⃣ Initialiser Git (si pas déjà fait)

```bash
cd "c:\Users\Artemix\Documents\New project\BKLN-TECH-SOLUTIONS-LIVRABLE"

# Initialiser le dépôt
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "Initial commit: Centrafrique Connect - Production Ready"
```

## 2️⃣ Créer un dépôt GitHub

1. Aller sur https://github.com/new
2. Entrer le nom: `centrafrique-connect`
3. Description: "Plateforme officielle de services gouvernementaux - Légalisation et casier judiciaire en ligne"
4. Choisir visibilité (Public ou Private)
5. Cliquer "Create repository"

## 3️⃣ Connecter GitHub Local

Après création du repo GitHub, vous verrez une page avec les commandes. Exécuter:

```bash
# Ajouter l'origin distant
git remote add origin https://github.com/VOTRE_USERNAME/centrafrique-connect.git

# Renommer la branche si nécessaire (modern default)
git branch -M main

# Pousser le code
git push -u origin main
```

## 4️⃣ Vérifier la connexion

```bash
# Vérifier les remotes configurés
git remote -v

# Affichage attendu:
# origin  https://github.com/VOTRE_USERNAME/centrafrique-connect.git (fetch)
# origin  https://github.com/VOTRE_USERNAME/centrafrique-connect.git (push)
```

## 5️⃣ Fichiers importants pour Render

Render vérifie automatiquement:

✅ `requirements.txt` - Dépendances Python  
✅ `Procfile` - Commande de démarrage  
✅ `runtime.txt` - Version Python  
✅ `render.yaml` - Configuration CI/CD  

Tous ces fichiers sont présents dans le projet.

## 6️⃣ Variables d'environnement importantes

Lors de la création du service Render, configurer:

```
SECRET_KEY=votre-clé-secrète-générer-via
DEBUG=False
ALLOWED_HOSTS=centrafrique-connect.onrender.com,www.centrafrique-connect.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Pour générer une bonne SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 7️⃣ Build Command sur Render

Cette commande est déjà dans `render.yaml`:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

## 8️⃣ Start Command sur Render

Cette commande est dans `Procfile`:

```bash
gunicorn bkln_tech.wsgi
```

## 9️⃣ Vérification avant Push

```bash
# S'assurer que tout est propre
git status

# Devrait afficher:
# On branch main
# nothing to commit, working tree clean
```

## 🔟 Créer le service Render

### Via GitHub (Recommandé)

1. Aller sur https://dashboard.render.com
2. Cliquer "New +" → "Web Service"
3. Sélectionner "Connect" à côté de votre repo
4. Configurer:
   - **Name**: `centrafrique-connect`
   - **Region**: `frankfurt`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
5. Les commands build/start sont auto-détectées
6. Configurer les env vars
7. Cliquer "Deploy"

### Via Render.yaml (Optionnel)

Fichier `render.yaml` fourni, configure tout automatiquement.

## 1️⃣1️⃣ Créer la Base de Données PostgreSQL

```bash
# Sur Render Dashboard
1. Cliquer "New +" → "PostgreSQL"
2. Configurer:
   - Name: centrafrique-connect-db
   - Region: frankfurt
   - PostgreSQL Version: 15
   - Plan: Free (ou Starter)
3. Copier la connection string
4. Ajouter à render.yaml ou Web Service env vars
```

## 1️⃣2️⃣ Premier Déploiement

Après tout configurer:

```bash
# Pousser les changements
git push origin main

# Render détectera et commencera le build automatiquement
# Vérifier les logs sur dashboard.render.com
```

## 1️⃣3️⃣ Vérifier le Déploiement

```bash
# Attendre ~5-10 minutes
# Aller sur https://centrafrique-connect.onrender.com
# Vérifier la page d'accueil s'affiche
# Vérifier /admin est accessible
```

## 1️⃣4️⃣ Troubleshooting

### Erreur: Build failed
```
Vérifier les logs Render
Vérifier requirements.txt est correct
Vérifier Python version
```

### Erreur: Database connection
```
Vérifier DATABASE_URL env var
Vérifier PostgreSQL créée
Vérifier IP whitelist Render
```

### Erreur: Static files 500
```
Vérifier collectstatic dans build command
Vérifier STATIC_URL et STATIC_ROOT dans settings
```

### Page blanche
```
Vérifier DEBUG=False
Vérifier ALLOWED_HOSTS
Consulter les logs Render
```

## 1️⃣5️⃣ Mise à Jour du Code

Après chaque modification:

```bash
# Commit local
git add .
git commit -m "Description du changement"

# Push vers GitHub
git push origin main

# Render redéploiera automatiquement
# Voir le status sur https://dashboard.render.com
```

## 1️⃣6️⃣ Sauvegardes

```bash
# Télécharger les backups PostgreSQL
# Sur Render Dashboard → Database → Backups

# Exporter la base localement:
pg_dump postgresql://... > backup.sql
```

## 1️⃣7️⃣ Créer un Super Utilisateur en Production

Après déploiement:

```bash
# Via Render Dashboard "Shell"
python manage.py createsuperuser

# Ou via SSH si disponible
```

## 1️⃣8️⃣ Configuration Domaine Personnalisé

1. Sur Render Dashboard → Service → Settings
2. "Custom Domain"
3. Entrer: `centrafrique-connect.com`
4. Suivre les instructions DNS
5. Attendre propagation (24h max)

---

## ⚠️ Points Importants

- ✅ Ne JAMAIS committer `.env` ou secrets
- ✅ Utiliser Render Environment Variables
- ✅ Vérifier les logs après chaque déploiement
- ✅ Sauvegarder la DB régulièrement
- ✅ Tester localement avant de pousser
- ✅ Garder les dépendances à jour

---

**Vous êtes maintenant prêt à déployer sur Render!** 🚀
