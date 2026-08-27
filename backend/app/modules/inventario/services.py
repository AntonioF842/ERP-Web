from sqlalchemy.orm import Session
from backend.app.modules.inventario.models import Producto
from backend.app.modules.inventario.shemas import ProductoCreate, ProductoUpdate

def get_producto_by_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def get_producto_by_sku(db: Session, sku: str):
    return db.query(Producto).filter(Producto.sku == sku).first()

def create_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(
        sku=producto.sku,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_venta=producto.precio_venta,
        costo_compra=producto.costo_compra,
        stock_actual=producto.stock_actual,
        stock_minimo=producto.stock_minimo
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto