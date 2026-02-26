from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Despliegue Automatico 2"}