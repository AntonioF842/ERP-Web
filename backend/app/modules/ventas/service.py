from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.app.modules.ventas.models import Venta, DetalleVenta
from backend.app.modules.ventas.schemas import VentaCreate
from backend.app.modules.inventario.models import Producto
from backend.app.modules.inventario.services import registar_movimento
from backend.app.modules.inventario.schemas import MovimientoCreate

def procesar_venta(db: Session, venta_in: VentaCreate, usuario_id: int):
    subtotal_acumulado: 0.0
    detalles_db: []

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
        registar_movimento(db=db, movimiento_in=mov_in)

    db.commit()
    db.refresh(db_venta)
    return db_venta