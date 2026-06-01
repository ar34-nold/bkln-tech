# BKLN-TECH

Application web Django 5 pour BKLN-TECH : site vitrine, boutique, maintenance informatique, location de materiel, legalisation de documents, casier judiciaire en ligne, academy, blog, support, notifications et tableau de bord.

## Installation locale

1. Creer un environnement virtuel Python 3.
2. Installer les dependances : `pip install -r requirements.txt`.
3. Appliquer les migrations : `python manage.py migrate`.
4. Charger les donnees de demonstration : `python manage.py seed_demo`.
5. Demarrer : `python manage.py runserver`.

Compte demo : `admin` / `admin12345`.

## Variables utiles

Copier `.env.example` puis definir `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL` et `REDIS_URL`.

## Deploiement Render

Le fichier `render.yaml` cree un service web et une base PostgreSQL. Sur Render, connecter le depot GitHub, choisir Blueprint, puis deployer. Le build installe les dependances, collecte les fichiers statiques et applique les migrations.

## API

Endpoints JSON disponibles :

- `/api/`
- `/api/products/`
- `/api/courses/`
- `/api/articles/`

## Modules

Applications Django incluses : `accounts`, `website`, `products`, `orders`, `inventory`, `maintenance`, `rentals`, `documents`, `legalization`, `criminal_records`, `academy`, `courses`, `lessons`, `quizzes`, `certificates`, `payments`, `blog`, `support`, `dashboard`, `notifications`.
