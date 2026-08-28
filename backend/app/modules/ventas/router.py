from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from backend.app.database import get_db
from backend.app.modules.ventas import services, schemas
from backend.app.core.security import get_current_user, require_roles
from backend.app.modules.usuarios.models import Usuario

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

@router.post("", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
def realizar_venta(
    venta: schemas.VentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin", "vendedor"]))
):
    return services.procesar_venta(db=db, venta_in=venta, usuario_id=current_user.id)

# Listar ventas
@router.get("", response_model=List[schemas.VentaResponse])
def listar_venta(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin", "vendedor"]))
):
    return services.get_ventas(db=db, skip=skip, limit=limit)

# Obtener detalles de venta
@router.get("/{venta_id}", response_model=schemas.VentaResponse)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin", "vendedor"]))
):
    venta = services.get_venta_by_id(db=db, venta_id=venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

# Cancelar Venta (Solo admin)
@router.patch("/{venta_id}/cancelar", response_model=schemas.VentaResponse)
def cancelar_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin"]))
):
    return services.cancelar_venta(db=db, venta_id=venta_id)