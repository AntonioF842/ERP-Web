from fastapi import FastAPI
from backend.app.database import Base, engine
from backend.app.modules.inventario import models as inventario_models
from backend.app.modules.usuarios import models as usuarios_models
from backend.app.modules.ventas import models as ventas_models
from backend.app.modules.inventario.router import router as inventario_router
from backend.app.modules.usuarios.routes import router as usuarios_router
from backend.app.modules.ventas.router import router as ventas_router


Base.metadata.create_all(bind=engine)  # Crea las tablas en la base de datos

app = FastAPI(
    title="ERP Web API",
    description="Backend para el sistema ERP",
    version="0.1.0"
)

app.include_router(inventario_router, prefix="/api/v1")
app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(ventas_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "API del ERP funcionando correctamente"}