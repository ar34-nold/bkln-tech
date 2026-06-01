# Checklist de Test - Centrafrique Connect

## Test de Fonctionnalités Locales

### 1. Accueil et Navigation
- [ ] Accès à la page d'accueil: http://localhost:8000/
- [ ] Affichage correct du logo et de la navbar
- [ ] Trois cartes de service visibles
- [ ] Liens de navigation accessibles

### 2. Authentification
- [ ] Accès à la page d'inscription
- [ ] Création d'un nouveau compte avec email
- [ ] Vérification de la création de UserProfile
- [ ] Connexion avec le compte créé
- [ ] Déconnexion fonctionne
- [ ] Login requis pour le dashboard

### 3. Dashboard Utilisateur
- [ ] Dashboard accessible après connexion
- [ ] Affichage de l'email dans la navbar
- [ ] Section "Mes demandes de légalisation" visible
- [ ] Section "Mes demandes de casier" visible
- [ ] Actions rapides accessibles

### 4. Demandes de Légalisation
- [ ] Accès à "Nouvelle légalisation"
- [ ] Formulaire avec champs (titre, description, fichier)
- [ ] Upload d'un fichier test
- [ ] Soumission de la demande
- [ ] Redirection vers le détail
- [ ] Génération du code QR
- [ ] Génération du PDF

### 5. Demandes de Casier Judiciaire
- [ ] Accès à "Demande de casier"
- [ ] Formulaire avec champs (date de naissance, lieu, motif)
- [ ] Validation des champs
- [ ] Soumission réussie

### 6. Vérification Publique
- [ ] Accès à "Vérifier un document"
- [ ] Formulaire de saisie du code
- [ ] Résultat positif avec un code valide
- [ ] Résultat négatif avec un code invalide

### 7. Admin Django
- [ ] Accès à /admin/
- [ ] Authentification admin
- [ ] Gestion des utilisateurs
- [ ] Gestion des demandes de documents
- [ ] Gestion des demandes de casier

### 8. API REST
- [ ] POST /api/auth/register/ → crée un utilisateur
- [ ] POST /api/auth/login/ → retourne un JWT token
- [ ] GET /api/auth/me/ → retourne le profil utilisateur
- [ ] GET /api/documents/ → liste les documents (avec authentification)
- [ ] POST /api/documents/ → crée une nouvelle demande

### 9. Erreurs et Validation
- [ ] Champs requis non vides
- [ ] Email format valide
- [ ] Mot de passe suffisamment fort
- [ ] Messages d'erreur affichés correctement
- [ ] Messages de succès affichés

### 10. Base de Données
- [ ] Tables créées: userprofile, documentrequest, criminalrecordrequest, activitylog
- [ ] Relations correctes entre les tables
- [ ] Données persistantes après rafraîchissement

## Test de Performance

- [ ] Temps de réponse < 2s pour les pages
- [ ] Pas d'erreur 500 en usage normal
- [ ] Pas de fuite mémoire lors de requêtes multiples

## Test de Sécurité

- [ ] CSRF protection active
- [ ] Passwords hashés en base
- [ ] Pas d'information sensible en logs
- [ ] Accès non autorisé bloqué

---

### Exécution du test

```bash
# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000

# Dans un autre terminal
python manage.py test connect.tests  # si tests unitaires présentes

# Ou tester manuellement via http://localhost:8000
```

### Problèmes à reporter
- Chaque problème identifié doit être noté avec:
  - Étapes pour reproduire
  - Comportement attendu vs actuel
  - Environnement (navigateur, OS, etc.)
