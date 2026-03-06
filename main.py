from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    instrumentator.expose(app)
    yield

app = FastAPI(title="Api de la Actividad 3 - DevOps", lifespan=lifespan)

instrumentator.instrument(app)

@app.get("/")
def read_root():
    return {"mensaje": "!Bienvenidos a la API optimizada para CI/CD - Prueba Despliegue Automatico"}

@app.get("/status")
def get_status():
    return {"estado":"Operativo", "entorno": "Contenedorizado"}