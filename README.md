# Gestion des Factures

Ce projet est une application web de gestion des factures développée avec Django. Elle permet de créer, modifier, supprimer et lister des factures, ainsi que de gérer les catégories de factures. Un système de logs est également mis en place pour suivre les créations de factures.

## Fonctionnalités

- **Gestion des factures** : Créer, modifier, supprimer et lister des factures.
- **Gestion des catégories** : Lister les catégories et voir les factures par catégorie.
- **Système de logs** : Enregistrement des créations de factures avec détails (utilisateur, IP, etc.).
- **Authentification** : Inscription, connexion et déconnexion des utilisateurs.

## Utilisation

- Accéder à l'application à l'adresse : `http://127.0.0.1:8000/`
- Se connecter ou s'inscrire pour utiliser l'application.
- Accéder à l'interface d'administration à l'adresse : `http://127.0.0.1:8000/admin/` avec le superutilisateur créé.

## Structure du projet

- `factures/` : Application principale contenant les modèles, vues, formulaires et templates.
- `gestion_factures/` : Configuration du projet Django.
- `templates/` : Dossiers de templates pour les pages HTML.

## Contribution

Mehdi Harche-nif