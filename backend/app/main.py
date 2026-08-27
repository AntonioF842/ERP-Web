from fastapi import FastAPI
from backend.app.database import Base, engine

from backend.app.modules.inventario import models as inventario_models

Base.metadata.create_all(bind=engine)  # Crea las tablas en la base de datos

app = FastAPI(
    title="ERP Web API",
    description="Backend para el sistema ERP",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "API del ERP funcionando correctamente"}