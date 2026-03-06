from fastapi.testclient import TestClient
from main import app

def test_read_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "mensaje" in response.json()

def test_get_status():
    with TestClient(app) as client:
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json()["estado"] == "Operativo"

def test_metrics_endpoint():
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "http_requests_total" in response.text