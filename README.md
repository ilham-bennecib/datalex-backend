# DataLex - Glossaire de Gouvernance de Données

DataLex est un outil de **Data Governance** conçu pour combler le fossé entre les définitions techniques (IT) et les besoins métiers (Finance/Gestion d'actifs).

## Architecture & Concepts
Ce projet met en œuvre des principes d'ingénierie logicielle avancés :
- **Architecture** : Monolithe Modulaire (KISS).
- **DDD (Domain-Driven Design)** : Approche centrée sur le métier avec un langage ubiquitaire.
- **SOLID** : Application des 5 principes pour un code maintenable et évolutif.
- **TDD** : Stratégie de tests via des tests d'acceptation et de contrat.

## Stack Technique
- **Backend** : Python 3 + Flask
- **Base de données** : MongoDB (NoSQL) via MongoEngine
- **API** : Interface RESTful

##  Installation et Utilisation
1. Clonez le projet : `git clone https://github.com/ilham-bennecib/datalex-backend.git`
2. Installez les dépendances : `pip install -r requirements.txt` (ou installez manuellement flask et mongoengine)
3. Lancez l'application : `python DataLex/app.py`

##  Exemple de requête (Recherche)
`GET /api/search?q=MKT` -> Retourne les définitions liées au marché.
