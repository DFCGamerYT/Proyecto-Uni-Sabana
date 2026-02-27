from fastapi.testclient import TestClient
from main import app

# Cliente de pruebas para la aplicación FastAPI
client = TestClient(app)


def test_read_main():
    # Comprueba que GET / devuelve 200 y el mensaje esperado
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Final Despliegue Laboratorio"}