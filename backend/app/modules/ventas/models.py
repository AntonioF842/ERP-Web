from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.app.database import Base

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id =  Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    impuesto = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(String(20), default="COMPLETADA") # Completada Cancelada
    fecha =  Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones 
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relacion cruzada
    venta = relationship("Venta", back_populates="detalles")