from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.modules.inventario import services, schemas
from backend.app.modules.usuarios.models import Usuario
from backend.app.core.security import get_current_user, require_roles
from backend.app.modules.usuarios.models import Usuario

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
    )

# Crear un nuevo producto
@router.post("/productos", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(
    producto: schemas.ProductoCreate, 
    db: Session = Depends(get_db),
    _user: Usuario = Depends(require_roles(["admin", "almacen"]))
):
    db_producto = services.get_producto_by_sku(db, sku=producto.sku)
    if db_producto:
        raise HTTPException(status_code=400, detail="El SKU del producto ya existe")
    return services.create_producto(db=db, producto=producto)

# Lista de productos
@router.get("/productos", response_model=List[schemas.ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_productos(db=db, skip=skip, limit=limit)

# Obterner un producto por ID
@router.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = services.get_producto_by_id(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Movimientos
@router.post("/movimientos", response_model=schemas.MovimientoResponse, status_code=status.HTTP_201_CREATED)
def crear_movimiento(movimiento: schemas.MovimientoCreate, db: Session = Depends(get_db)):
    try:
        db_movimiento = services.registrar_movimiento(db=db, movimiento_in=movimiento)
        if not db_movimiento:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_movimiento
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Actulizar Producto(PUT/PATCH)
@router.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoUpdate,
    db: Session = Depends(get_db)
):
    db_producto = services.update_producto(db=db, producto_id=producto_id, producto_in=producto)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Eliminar Producto(DELETE)
@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int, 
    db: Session = Depends(get_db), 
    _user: Usuario = Depends(require_roles(["admin"]))
):
    exito = services.delete_producto(db=db, producto_id=producto_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None