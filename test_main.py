import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_get_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["estado"] == "Operativo"

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text