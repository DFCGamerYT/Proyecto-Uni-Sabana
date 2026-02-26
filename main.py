from fastapi import FastAPI

app = FastAPI(title="Api de la Actividad 3 - DevOps")

@app.get("/")
def read_root():
    return {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Despliegue Automatico 2"} #TODO PRUEBA SONARQUBE, TEST

@app.get("/status")
def get_status():
    return {"estado":"Operativo", "entorno": "Contenedorizado"}