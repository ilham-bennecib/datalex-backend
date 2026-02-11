from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect, Document, StringField, ListField
import json

app = Flask(__name__)

# --- 1. CONFIGURATION DE LA SÉCURITÉ (CORS) ---
# On autorise le Front-end (même s'il vient d'un fichier local) à parler à l'API
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- 2. CONNEXION À LA BASE DE DONNÉES ---
# On utilise l'IP locale 127.0.0.1 (localhost).
# Le timeout est court (2s) pour éviter que l'API ne freeze si la BDD est éteinte.
try:
    connect(
        db="datalex",
        host="mongodb://127.0.0.1:27017/datalex",
        serverSelectionTimeoutMS=5000
    )
    print("✅ Connecté au port 27017 (Mapping Docker)")
except Exception as e:
    print(f"❌ Erreur : {e}")
# --- 3. MODÈLE DE DONNÉES (DOMAINE) ---
class Terme(Document):
    nom_technique = StringField(required=True, unique=True)
    nom_metier = StringField(required=True)
    definition = StringField()
    source = StringField()
    tags = ListField(StringField())

# --- 4. ROUTES DE L'API (PRÉSENTATION) ---

@app.route('/api/termes', methods=['POST'])
def ajouter_terme():
    try:
        data = request.json
        # On crée et on sauvegarde le document dans MongoDB
        nouveau = Terme(**data).save()
        return nouveau.to_json(), 201, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Erreur lors de l'ajout : {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def chercher():
    try:
        q = request.args.get('q', '')
        # Recherche insensible à la casse (icontains) sur le nom technique ou métier
        if q:
            resultats = Terme.objects(nom_technique__icontains=q) or Terme.objects(nom_metier__icontains=q)
        else:
            resultats = Terme.objects.all()
            
        return resultats.to_json(), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return jsonify({"error": str(e)}), 500

# --- 5. LANCEMENT DU SERVEUR ---
if __name__ == "__main__":
    # Debug=True permet de voir les erreurs en direct et de relancer auto le serveur
    app.run(debug=True, port=5000)