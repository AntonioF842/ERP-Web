from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import Base, engine
from backend.app.core.config import settings

from backend.app.modules.inventario import models as inventario_models
from backend.app.modules.usuarios import models as usuarios_models
from backend.app.modules.ventas import models as ventas_models

from backend.app.modules.inventario.router import router as inventario_router
from backend.app.modules.usuarios.routes import router as usuarios_router
from backend.app.modules.ventas.router import router as ventas_router
from backend.app.modules.reportes.router import router as reportes_router


Base.metadata.create_all(bind=engine)  # Crea las tablas en la base de datos

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Configuración CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(inventario_router, prefix="/api/v1")
app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(ventas_router, prefix="/api/v1")
app.include_router(reportes_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": f"{settings.PROJECT_NAME} funciona correctamente"}