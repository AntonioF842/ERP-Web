def test_procesar_y_cancelar_venta(client, admin_user):
    login_res = client.post(
        "/api/v1/usuarios/login",
        data={"username": "admin@erp.com", "password": "admin123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    prod_res = client.post(
        "/api/v1/inventario/productos",
        headers=headers,
        json={
            "sku": "TECLADO-01",
            "nombre": "Teclado RGB",
            "costo_compra": 200.0,
            "precio_venta": 500.0,
            "stock_actual": 20,
            "stock_minimo": 2
        },
    )
    producto_id = prod_res.json()["id"]

    venta_res = client.post(
        "/api/v1/ventas",
        headers=headers,
        json={
            "detalles": [
                {"producto_id": producto_id, "cantidad": 5}
            ]
        }
    )
    assert venta_res.status_code == 201
    datos_venta = venta_res.json()
    assert datos_venta["subtotal"] == 2500.0
    assert datos_venta["total"] == 2900.0
    assert datos_venta["estado"] == "COMPLETADA"

    prod_check = client.get(f"/api/v1/inventario/productos/{producto_id}")
    assert prod_check.json()["stock_actual"] == 15

    cancel_res = client.patch(
        f"/api/v1/ventas/{datos_venta['id']}/cancelar",
        headers=headers
    )
    assert cancel_res.status_code == 200
    assert cancel_res.json()["estado"] == "CANCELADA"

    prod_check_after_cancel = client.get(f"/api/v1/inventario/productos/{producto_id}")
    assert prod_check_after_cancel.json()["stock_actual"] == 20
