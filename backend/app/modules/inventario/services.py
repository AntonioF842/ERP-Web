from sqlalchemy.orm import Session
from backend.app.modules.inventario.models import Producto, MovimientoInventario
from backend.app.modules.inventario.schemas import ProductoCreate, ProductoUpdate, MovimientoCreate


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

def registrar_movimento(db: Session, movimiento_in: MovimientoCreate):
    producto = db.query(Producto).filter(Producto.id == movimiento_in.producto_id).first()
    # Buscar Producto
    if not producto:
        return None
    # Actulizar stock segun el movimiento
    if movimiento_in.tipo_movimiento == "ENTRADA":
        producto.stock_actual += movimiento_in.cantidad
    elif movimiento_in.tipo_movimiento == "SALIDA":
        if producto.stock_actual < movimiento_in.cantidad:
            raise ValueError("Stock insuficiente para realizar salida")
        producto.stock_actual -= movimiento_in.cantidad
    elif movimiento_in.tipo_movimiento == "AJUSTE":
        producto.stock_actual = movimiento_in.cantidad

    #Guardar el movimiento en el historial 
    db_movimiento = MovimientoInventario(
        producto_id = movimiento_in.producto_id,
        tipo_movimiento = movimiento_in.tipo_movimiento,
        cantidad =  movimiento_in.cantidad,
        motivo = movimiento_in.motivo
    )
    db.add(db_movimiento)
    db.commit()
    db.refresh(producto)
    return db_movimiento

def update_producto(db: Session, producto_id: int, producto_in: ProductoUpdate):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None

    update_data = producto_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return False

    db.delete(db_producto)
    db.commit()
    return True
    