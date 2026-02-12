import pytest
from app import app, Terme
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- 1. TESTS UNITAIRES  ---

def test_terme_model_validation():
    """Vérifie qu'on ne peut pas créer un terme sans nom technique (S de SOLID)"""
    terme = Terme(nom_metier="Prix de Marché")
    with pytest.raises(Exception):
        terme.save() # Doit échouer car nom_technique est 'required'

def test_terme_format_tags():
    """Vérifie que la liste des tags est bien gérée"""
    terme = Terme(nom_technique="UNIT_TEST", nom_metier="Test", tags=["finance", "data"])
    assert len(terme.tags) == 2
    assert "finance" in terme.tags

# --- 2. TESTS D'INTÉGRATION  ---

def test_api_create_terme(client):
    """Vérifie que la route POST fonctionne et répond 201"""
    payload = {
        "nom_technique": "TEST_AUTO_01",
        "nom_metier": "Test Automatisé",
        "definition": "Ceci est un test",
        "source": "Pytest"
    }
    response = client.post('/api/termes', 
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    assert b"TEST_AUTO_01" in response.data

def test_api_search_terme(client):
    """Vérifie que la recherche renvoie bien des résultats"""
    response = client.get('/api/search?q=TEST')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

# --- 3. TEST DE PREUVE RÉPLICA  ---

def test_replica_read_diagnostic(client):
    """Prouve que la route de diagnostic de lecture fonctionne"""
    response = client.get('/db/read-test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "source" in data
    assert data["source"] == "replica_set_query"