# OpenClassrooms Projet 7: Création de la platerforme EasyWod

Ce répertoire contiendra les développement du projet 13. L'objectif de ce projet est de créer une application Web permettant la gestion d'un club (ici de sport mais peut être un club de dance où autre).
Cette application doit être développée avec le framework Django.

## Fonctionnalités Attendues

- Développement avec le Framework Web Django
- Base de données PostgreSQL
- Authentification de l’utilisateur par son adresse mail
- Gestion des abonnement utilisateur (Activation/Désactivation d'un abonnement, changement d'abonnement).
- 2 types d'abonnements pour la v1.0:
  - Premium qui donne l'accès à un nombre de cours illimités.
  - Trial qui lui donne un nombre de cours d'essai à l'utilisateur.
- Une partie "Cours", permettant la création d'évènements pour les employés et l'inscription/désinscription à des évènements ainsi que le suivi des inscriptions en cours pour les membres.
- Un blog permettant de créer des Articles pour suivre l'actualité du club.
- Un envoi de Newsletter: Qui envoit la liste des Articles parus sur la semaine passée.
- Une gestion des demandes de contact centralisée sur le site: Les demandes saisies par le formulaire de contact sont accessible directement sur le site pour les employés, qui peuvent y répondre également depuis le site, un mail étant envoyé automatiquement à l'auteur de la demande.

## Structure du projet Django

- User: Gestion utilisateur.
- Membership: Gestion des abonnements utilisateur.
- Event: Gestion des évènements.
- Blog: Gestion des articles du blog.
- Newsletter: Gestion de l'envoi de la newsletter.
- Contact_us: Gestion des messages de demande.

## Déploiement et utilisation du site en local

Nécessite Python 3.8 et pipenv d'installés sur le poste, effectuer les manipulations suivantes dans l'ordre:

  1. Récupérer le projet Django depuis github.
  2. Installer l'environnement virtuel `pipenv install`
  3. Entrer dans l'environnement virtuel `pipenv shell`
  4. Récupérer la structure de la base de données avec `python manage.py migrate`
  5. Lancer la custom command fill_database, permettant de récupérer les données de l'API OpenFoodFacts `python manage.py fill_database`
  6. Lancer le serveur `python manage.py runserver`
  
Le projet est configuré de sorte à utiliser une base de données SQLite en local, PostgreSQL n'est mis en place et utilisé que sur le site en production à l'adresse https://easywod.angogg.com/
