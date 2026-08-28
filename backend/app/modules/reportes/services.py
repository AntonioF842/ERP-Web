from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime

from backend.app.modules.inventario.models import Producto
from backend.app.modules.ventas.models import Venta, DetalleVenta

# Alerta de Stock bajo
def get_productos_stock_bajo(db: Session):
    return db.query(Producto).filter(Producto.stock_actual <= Producto.stock_minimo).all()

# Resumen de ventas e ingresos
def get_resumen_ventas(db: Session):
    total_ventas = db.query(func.count(Venta.id)).filter(Venta.estado == "COMPLETADA").scalar() or 0
    ingresos_totales = db.query(func.sum(Venta.total)).filter(Venta.estado == "COMPLETADA").scalar or 0.0

    return {
        "total_ventas_realizadas": total_ventas,
        "ingresos_totales": round(ingresos_totales, 2)
    }

# Top productos mas vendidos 
def get_top_productos(db: Session, limit: int = 5):
    resultados = (
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
        .group_by(Producto.id)
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