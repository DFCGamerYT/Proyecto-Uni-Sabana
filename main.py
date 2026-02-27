from fastapi import FastAPI

# API de la Actividad 3 - DevOps
# Rutas: GET /, GET /status

app = FastAPI(title="Api de la Actividad 3 - DevOps")


@app.get("/")
def read_root():
    # Devuelve mensaje de bienvenida (pruebas)
    return {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Final Despliegue Laboratorio"}  # TODO: PRUEBA SONARQUBE, TEST


@app.get("/status")
def get_status():
    # Devuelve estado de la API
    return {"estado": "Operativo", "entorno": "Contenedorizado"}