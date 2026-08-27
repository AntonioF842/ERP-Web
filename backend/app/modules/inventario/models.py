from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    precio_venta = Column(Float, nullable=False, default=0.0)
    costo_compra = Column(Float, nullable=False, default=0.0)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)

    # Auditorioa
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relacion uno a muchos con los movimientos de inventario
    movimientos = relationship("MovimientoInventario", back_populates="producto", cascade="all, delete-orphan")

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_movimiento = Column(String(50), nullable=False)  # "entrada", "salida", "ajuste"
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String(255), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relacion con el producto
    producto = relationship("Producto", back_populates="movimientos")
    