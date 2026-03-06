from fastapi.testclient import TestClient
from app_api.main import app

client = TestClient(app)

CSV_PATH = "app_api/data/moncsv.csv"

def test_get_data():
    """Test GET /data route."""
    response = client.get("/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)

def test_post_data():
    """Test POST /data route."""
    response = client.post("/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "lignes sauvegardées" in json_data["message"]

def test_math_route():
    """Test GET /math route."""
    response = client.get("/math")
    assert response.status_code == 200
    json_data = response.json()
    # Vérifie les clés
    for key in ["add", "sub", "square", "rows_in_csv"]:
        assert key in json_data