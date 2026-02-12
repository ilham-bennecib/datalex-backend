# DataLex - Glossaire de Gouvernance de Données

DataLex est un outil de **Data Governance** conçu pour combler le fossé entre les définitions techniques (IT) et les besoins métiers (Finance/Gestion d'actifs).

## Architecture & Concepts
Ce projet met en œuvre des principes d'ingénierie logicielle avancés :
- **Architecture** : Monolithe Modulaire (KISS) avec base de données distribuée.
- **DDD (Domain-Driven Design)** : Approche centrée sur le métier avec un langage ubiquitaire.
- **SOLID** : Application des 5 principes pour un code maintenable et évolutif.
- **TDD** : Stratégie validée par 5 tests automatisés (unitaires et intégration).

## Stack Technique
- **Backend** : Python 3 + Flask
- **Base de données** : Cluster MongoDB (1 Primary + 2 Replicas)
- **Conteneurisation** : Docker Compose

## Installation et Utilisation (Livrable 6)
1. **Lancement de l'infrastructure** :
   `docker-compose up -d --build`
2. **Initialisation du Cluster (Replica Set)** :
   `docker exec -it mongo-primary mongosh --eval "rs.initiate({_id:'rs0', members:[{_id:0,host:'mongo-primary:27017'},{_id:1,host:'mongo-secondary-1:27017'},{_id:2,host:'mongo-secondary-2:27017'}]})"`

## Diagnostics et Tests (Livrables 4 & 5)
- **Lancer les tests** : `pytest test_app.py`
- **Vérifier l'état de la base** : `GET /db/status`
- **Tester la lecture replica** : `GET /db/read-test`
- **Tester l'écriture primary** : `POST /db/write-test`

## Preuves Techniques (Livrable 7)
- **Réplication** : Les données insérées sur le Primary sont automatiquement copiées sur les deux Replicas.
- **Failover** : En cas d'arrêt du Primary (`docker stop mongo-primary`), le cluster élit un nouveau chef automatiquement, garantissant la disponibilité du service.

## Exemple de requête (Recherche)
`GET /api/search?q=MKT` -> Retourne les définitions liées au marché.
