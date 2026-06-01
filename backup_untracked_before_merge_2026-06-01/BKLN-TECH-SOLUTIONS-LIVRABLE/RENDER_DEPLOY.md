Déploiement Render — étapes finales

1) Vérifications locales
- Assure-toi que ton repo est poussé sur GitHub (tu l'as fait: ar34-nold/bkln-tech).
- Fichiers importants: `render.yaml`, `Procfile`, `requirements.txt`, `bkln_tech/settings.py`, `.env.example`, `.env` (local).

2) Créer le service Web sur Render
- Render → New → Web Service → Connect GitHub → choisis `ar34-nold/bkln-tech`.
- Branch: `main`.
- Build command:
  pip install -r requirements.txt && python manage.py collectstatic --noinput
- Start command:
  gunicorn bkln_tech.wsgi --log-file -
- Crée le service.

3) Variables d'environnement (Render → Service → Environment)
- Ajoute (Private):
  - SECRET_KEY : COPIER DE `.env` ou générer une nouvelle
  - DEBUG : False
  - ALLOWED_HOSTS : *
  - USE_S3 : False
- Si tu crées une base PostgreSQL gérée par Render, ajoute aussi:
  - DATABASE_URL : valeur fournie par Render

4) (Option recommandé) Créer PostgreSQL managé
- Render → New → PostgreSQL → choisis plan (free/test) → Create
- Copie la `DATABASE_URL` fournie et ajoute-la dans les variables d'environnement du service.

5) Déployer et exécuter les commandes post-déploiement
- Lance le déploiement (Render fait le build automatiquement).
- Une fois le service créé, ouvre Shell (Render → Service → Shell) et exécute :
  python manage.py migrate
  python manage.py collectstatic --noinput

6) Vérifier l'application
- Ouvre l'URL publique fournie par Render.
- Tester les pages principales.

7) Nom de domaine (achat + configuration)
- Acheter domaine chez un registrar (Namecheap, Gandi, OVH, etc.).
- Dans Render → Service → Settings → Custom Domains → Add Domain : ajoute `mondomaine.tld` et `www.mondomaine.tld`.
- Render fournira les enregistrements DNS à ajouter chez le registrar :
  - CNAME pour `www` pointant vers `bkln-tech-web.onrender.com` (ou cible fournie)
  - A/ALIAS pour apex selon instructions Render
- Après propagation DNS, Render génèrera automatiquement le certificat TLS.

8) Passage en production complet
- Optionnel : activer `USE_S3=True` et configurer `AWS_*` pour stocker les médias.
- Vérifier sauvegardes PostgreSQL et configuration de monitoring.

Commandes utiles locales
```powershell
# créer/activer venv (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Si tu veux que je crée le service Render automatiquement, fournis une clé API Render (README: https://render.com/docs/api) et j'expliquerai exactement comment procéder en sécurité. Sinon, dis-moi à quelle étape tu es sur Render et je te guide pas-à-pas.