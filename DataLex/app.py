from flask import Flask, request, jsonify
from mongoengine import connect, Document, StringField, ListField

app = Flask(__name__)

# --- CONFIGURATION CLUSTER ---
# On donne l'adresse du primaire et du secondaire. 
# Le paramètre replicaSet="rs0" permet de savoir qui est le chef.
# On définit l'URI qui pointe vers tes deux containers Docker
uri = "mongodb://localhost:27017,localhost:27018/datalex?replicaSet=rs0"

# On connecte MongoEngine à notre Replica Set
connect(host=uri)

# --- COUCHE DOMAINE (Modèle DDD) ---
class Terme(Document):
    """ Agrégat principal du domaine Glossaire """
    nom_technique = StringField(required=True, unique=True)
    nom_metier = StringField(required=True)
    definition = StringField()
    source = StringField()
    tags = ListField(StringField())

# --- COUCHE BUSINESS (Logique métier simple) ---
class GlossaireService:
    def rechercher_terme(self, query):
        # KISS : Recherche simple sur deux champs
        return Terme.objects(nom_technique__icontains=query) or Terme.objects(nom_metier__icontains=query)

service = GlossaireService()

# --- COUCHE PRÉSENTATION (API) ---
@app.route('/api/termes', methods=['POST'])
def ajouter_terme():
    data = request.json
    nouveau = Terme(**data).save()
    # On utilise .to_json() pour convertir l'objet MongoDB en texte JSON
    return nouveau.to_json(), 201, {'Content-Type': 'application/json'}

@app.route('/api/search', methods=['GET'])
def chercher():
    q = request.args.get('q', '')
    resultats = Terme.objects(nom_technique__icontains=q) # Ou ta logique de service
    return resultats.to_json(), 200, {'Content-Type': 'application/json'}

if __name__ == "__main__":
    app.run(debug=True, port=5000)