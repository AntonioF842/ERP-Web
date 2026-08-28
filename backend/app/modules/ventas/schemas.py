from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Item de entrada
class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int

# Peticion de creacion venta
class VentaCreate(BaseModel):
    detalles: List[DetalleVentaCreate]

# Esquemas de respuesta
class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class VentaResponse(BaseModel):
    id: int
    usuario_id: int
    subtotal: float
    impuesto: float
    total: float
    estado: str
    fecha: datetime
    detalles: List[DetalleVentaResponse]

    model_config = ConfigDict(from_attributes=True)