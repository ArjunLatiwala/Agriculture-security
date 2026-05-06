from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["ready"] == True

def test_predict():
    response = client.post("/predict", json={"nitrogen": 100, "phosphorus": 50})
    assert response.status_code == 200
    assert "yield_prediction" in response.json()
    assert response.json()["yield_prediction"] == 50.0

def test_predict_validation():
    response = client.post("/predict", json={"nitrogen": -10, "phosphorus": 50})
    assert response.status_code == 422
