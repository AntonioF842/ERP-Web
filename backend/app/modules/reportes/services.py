from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.app.modules.inventario.models import Producto, MovimientoInventario
from backend.app.modules.ventas.models import Venta, DetalleVenta

# Alerta de Stock bajo
def get_productos_stock_bajo(db: Session):
    return db.query(Producto).filter(Producto.stock_actual <= Producto.stock_minimo).all()

def _obtener_fecha_inicio(periodo: str):
    ahora = datetime.now(timezone.utc)
    if periodo == "semana":
        return ahora - timedelta(days=7)
    elif periodo == "mes":
        return ahora - timedelta(days=30)
    elif periodo == "anio":
        return ahora - timedelta(days=365)
    return None

# Resumen de ventas e ingresos
def get_resumen_ventas(db: Session, periodo: str = "todos"):
    query = db.query(
        func.count(Venta.id).label("total_ventas"),
        func.sum(Venta.total).label("ingresos")
    ).filter(Venta.estado == "COMPLETADA")

    fecha_inicio = _obtener_fecha_inicio(periodo)
    if fecha_inicio:
        query = query.filter(Venta.fecha >= fecha_inicio)

    resultado = query.first()
    total_ventas = resultado.total_ventas or 0
    ingresos_total = resultado.ingresos or 0.0

    return {
        "total_ventas_realizadas": total_ventas,
        "ingresos_totales": round(ingresos_total, 2)
    }

# Top productos mas vendidos 
def get_top_productos(db: Session, limit: int = 5, periodo: str = "todos"):
    query = (
        db.query(
            Producto.id,
            Producto.nombre,
            Producto.sku,
            func.sum(DetalleVenta.cantidad).label("total_vendido"),
            func.sum(DetalleVenta.subtotal).label("total_recaudado")
        )
        .join(DetalleVenta, Producto.id == DetalleVenta.producto_id)
        .join(Venta, DetalleVenta.venta_id == Venta.id)
        .filter(Venta.estado == "COMPLETADA")
    )

    fecha_inicio = _obtener_fecha_inicio(periodo)
    if fecha_inicio:
        query = query.filter(Venta.fecha >= fecha_inicio)

    resultados = (
        query.group_by(Producto.id)
        .order_by(desc("total_vendido"))
        .limit(limit)
        .all()
    )

    return [
        {
            "producto_id": r.id,
            "nombre": r.nombre,
            "sku": r.sku,
            "total_vendido": r.total_vendido,
            "total_recaudado": round(r.total_recaudado, 2)
        }
        for r in resultados
    ]

def _obtener_fecha_inicio(periodo: str):
    ahora = datetime.now(timezone.utc)
    if periodo == "dia":
        return ahora - timedelta(days=1)
    elif periodo == "semana":
        return ahora - timedelta(days=7)
    elif periodo == "mes":
        return ahora - timedelta(days=30)
    elif periodo == "anio":
        return ahora - timedelta(days=365)
    return None

def get_movimientos_stock(db: Session, periodo: str = "todos"):
    query = db.query(
        MovimientoInventario.id,
        Producto.nombre.label("producto_nombre"),
        Producto.sku,
        MovimientoInventario.tipo_movimiento,
        MovimientoInventario.cantidad,
        MovimientoInventario.motivo,
        MovimientoInventario.fecha
    ).join(Producto, MovimientoInventario.producto_id == Producto.id)

    fecha_inicio =  _obtener_fecha_inicio(periodo)
    if fecha_inicio:
        query = query.filter(MovimientoInventario.fecha >= fecha_inicio)

    return query.order_by(desc(MovimientoInventario.fecha)).limit(50).all()