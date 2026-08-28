from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.modules.ventas import service, schemas
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
    return service.procesar_venta(db=db, venta_in=venta, usuario_id=current_user.id)