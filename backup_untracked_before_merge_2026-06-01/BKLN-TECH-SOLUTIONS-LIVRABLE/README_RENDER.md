Déploiement sur Render

1) Créer un repo GitHub et push du projet.

2) Sur Render, créer un nouveau Web Service -> connecter au repo.

3) Dans l'onglet `Environment` ajouter les secrets (Private):
- `SECRET_KEY` : valeur forte
- `DEBUG` : `False`
- `ALLOWED_HOSTS` : `your-app.onrender.com`
- `USE_S3` : `True` si vous utilisez S3
- si `USE_S3=True`, ajouter : `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME` (optionnel)
- (optionnel) `DATABASE_URL` si vous utilisez une base distante

4) Déployer : Render exécutera `pip install -r requirements.txt` puis `python manage.py collectstatic --noinput` et `gunicorn bkln_tech.wsgi`.

5) Exécuter migrations via Shell → `python manage.py migrate`.

Remarque: pour de petits projets, l'utilisation de SQLite est acceptée mais non recommandée en production partagée.
