from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Esquemas base
class ProductoBase(BaseModel):
    sku: str
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    costo_compra: float
    stock_actual: int
    stock_minimo: int

# Esquem de entrda para crear un producto
class ProductoCreate(ProductoBase):
    pass

# Esquema de actualización de un producto
class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = None
    costo_compra: Optional[float] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None

# Esquema de salida para un producto
class ProductoResponse(ProductoBase):
    id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)