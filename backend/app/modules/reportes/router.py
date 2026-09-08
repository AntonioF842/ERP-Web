from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.modules.reportes import services, schemas
from backend.app.core.security import require_roles
from backend.app.modules.usuarios.models import Usuario

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes y Dashboard"]
)

# Stock bajo
@router.get("/stock-bajo", response_model=List[schemas.ProductosStockBajoReponse])
def obtener_alertas_stock(
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin", "almacen"]))
):
    return services.get_productos_stock_bajo(db=db)

# Resumen Financiero
@router.get("/resumen", response_model=schemas.ResumenVentasResponse)
def obterner_resumen_general(
    periodo: str = "todos",
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin"]))
):
    return services.get_resumen_ventas(db=db, periodo=periodo)

# Top Productos
@router.get("/top-productos", response_model=List[schemas.ProductoTopResponse])
def obtener_top_productos(
    limit: int = 5,
    periodo: str = "todos",
    db: Session = Depends(get_db),
    _user: Usuario =  Depends(require_roles(["admin"]))
):
    return services.get_top_productos(db=db, limit=limit, periodo=periodo)