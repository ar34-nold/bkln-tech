# BKLN-TECH SOLUTIONS

Application web Django pour la gestion des ventes, locations, maintenances, installations systeme, antivirus et reseaux informatiques.

## Installation

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Ouvrir ensuite: http://127.0.0.1:8000/

## Execution rapide sur Windows

1. Double-cliquer sur `install.bat`
2. Double-cliquer sur `run.bat`
3. Ouvrir: http://localhost:8000/

Identifiants de test inclus dans la base SQLite livree:

```text
Utilisateur: admin
Mot de passe: admin12345
```

## Modules inclus

- Clients
- Produits et stock
- Ventes avec facture PDF
- Locations avec calcul automatique du cout
- Maintenance et fiches techniques
- Installations de systemes d'exploitation
- Antivirus et suivi des licences
- Interventions reseau
