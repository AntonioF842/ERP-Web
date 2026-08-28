from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.app.modules.ventas.models import Venta, DetalleVenta
from backend.app.modules.ventas.schemas import VentaCreate
from backend.app.modules.inventario.models import Producto
from backend.app.modules.inventario.services import registrar_movimento
from backend.app.modules.inventario.schemas import MovimientoCreate

def procesar_venta(db: Session, venta_in: VentaCreate, usuario_id: int):
    subtotal_acumulado = 0.0
    detalles_db = []

    # 1. Validar produtos y calcular importes
    for item in venta_in.detalles:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto ID {item.producto_id} no encontrado")

        if producto.stock_actual < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock_actual}"
            )

        linea_subtotal = producto.precio_venta * item.cantidad
        subtotal_acumulado += linea_subtotal

        # Crear objeto de detalle
        detalle = DetalleVenta(
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.procesar_venta,
            subtotal=linea_subtotal
        )
        detalles_db.append((detalle, producto))
    # 2,  Calcular impuestos y total 
    impusto_total = subtotal_acumulado * 0.16
    total_final = subtotal_acumulado + impusto_total

    # 3. Crear cabecera de la venta
    db_venta = Venta(
        usuario_id=usuario_id,
        subtotal=subtotal_acumulado,
        impuesto=impusto_total,
        total=total_final,
        estado="COMPLETADO"
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    # 4. Asignar los detalles y descontar del inventario
    for detalle, producto in detalles_db:
        detalle.venta_id = db_venta.id
        db.add(detalle)

        # Descontar existencias reutilizando la funciond movimiento de inventario
        mov_in = MovimientoCreate(
            producto_id=producto.id,
            tipo_movimiento="SALIDA",
            cantidad=detalle.catidad,
            motivo=f"Venta registrada ID {db_venta.id}"
        )
        registrar_movimento(db=db, movimiento_in=mov_in)

    db.commit()
    db.refresh(db_venta)
    return db_venta

# Obtener todas las ventas con paginación
def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Venta).offset(skip).limit(limit).all()

# Obtener venta por ID
def get_venta_by_id(db: Session, venta_id: int):
    return db.query(Venta).filter(Venta.id == venta_id).first()

# Cancelar venta(Devuelve el stock al inventario)
def cancelar_venta(db: Session, venta_id: int):
    venta = get_venta_by_id(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )
    if venta.estado == "CANCELADA":
        raise HTTPException(
            status_code=400,
            detail="La venta ya esta cancelada"
        )
    # Marca venta cancelada
    venta.estado = "CANCELADA"

    # reingresa las existencias al inventario
    for detalle in venta.detalles:
        mov_in = MovimientoCreate(
            producto_id=detalle.producto_id,
            tipo_movimiento="ENTRADA",
            cantidad=detalle.cantidad,
            motivo=f"Cancelación de Venta ID #{venta.id}"
        )
        registrar_movimento(db=db, movimineto_in=mov_in)

    db.commit()
    db.refresh(venta)
    return venta