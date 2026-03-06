from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Despliegue Automatico"}

def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"estado": "Operativo", "entorno": "Contenedorizado"}

def test_metrics_endpoint():

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text