from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class ProductosStockBajoReponse(BaseModel):
    id: int
    sku: str
    nombre: str
    stock_actual: int
    stock_minimo: int

    model_config = ConfigDict(from_attributes=True)

class ResumenVentasResponse(BaseModel):
        total_ventas_realizadas: int
        ingresos_totales: float

class ProductoTopResponse(BaseModel):
    producto_id: int
    nombre: str
    sku: str
    total_vendido: int
    total_recaudado: float

class MoviminetoReporteResponse(BaseModel):
    id: int
    producto_nombre: str
    sku: str
    tipo_movimiento: str
    cantidad: int
    motivo: Optional[str] =None
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)