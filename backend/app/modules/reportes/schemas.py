from pydantic import BaseModel, ConfigDict
from typing import List

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