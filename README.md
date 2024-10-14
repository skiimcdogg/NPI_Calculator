# Calculatrice Infix/Postfix avec FastAPI et MongoDB

Ce projet implémente une calculatrice capable de traiter des expressions en notation infix et postfix, utilisant FastAPI pour le backend et MongoDB pour le stockage des données.

## Prérequis

- Docker
- Docker Compose

## Installation et démarrage

1. Clonez le dépôt.

2. Créez un fichier `.env` à la racine du projet et configurez les variables d'environnement nécessaires.
  ```bash
  MONGO_INITDB_ROOT_USERNAME=root
  MONGO_INITDB_ROOT_PASSWORD=root
  MONGO_HOST=mongo
  MONGO_PORT=27017
  MONGO_DB_NAME=calculations
  ```

4. Lancez Docker Compose pour construire et démarrer les conteneurs :
   ```bash
   docker-compose build
   docker-compose up
   ```

5. Accédez à l'application

   L'application sera accessible à l'adresse suivante :
   ```
   http://localhost:8000/interface/
   ```

## Structure du projet

- **Routes** : Gèrent les requêtes HTTP (POST pour les calculs et GET pour l'export CSV).
- **Services** : Contiennent la logique métier, comme l'évaluation des calculs et la gestion des erreurs.
- **Repositories** : S'occupent de l'interaction avec MongoDB (insertion et récupération des données).

Structurce ici simplifiée qui permet d'avoir une application scalable et testable.

## Fonctionnalités

### Interface web

L'interface vous permet de :
- Entrer des calculs en notation infix ou postfix via un formulaire.
- Exporter les résultats sous forme de fichier CSV via un bouton dans l'interface.

### Export des résultats

Une fois les calculs effectués, vous pouvez exporter les résultats sous forme de CSV en cliquant sur un bouton dans l'interface web.

## Dépendances

### MongoDB

Le fichier `docker-compose.yml` inclut une image MongoDB. Le conteneur MongoDB sera automatiquement démarré lors de l'exécution du projet.

Si vous avez déjà une instance MongoDB locale, assurez-vous de mettre à jour le fichier `.env` en conséquence.

## Support

Pour toute question ou problème, veuillez ouvrir une issue dans le dépôt du projet.
