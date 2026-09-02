def test_crear_producto_sin_autenticacion(client):
    response = client.post(
        "/api/v1/inventario/productos",
        json={
            "sku": "PROD-001",
            "nombre": "Producto Prueba",
            "precio_venta": 150.0,
            "stock_actual": 10
        }
    )
    assert response.status_code == 401

def test_crear_producto_con_admin(client, admin_user):
    login_res = client.post(
        "/api/v1/usuarios/login",
        data={"username": "admin@erp.com", "password": "admin123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    respnse = client.post(
        "/api/v1/inventario/productos",
        headers=headers,
        json={
            "sku": "PROD-001",
            "nombre": "Teclado Mecánico",
            "costo_compra": 800.0,
            "precio_venta": 1200.0,
            "stock_actual": 25,
            "stock_minimo": 5,
        }
    )
    assert respnse.status_code == 201
    data = respnse.json()
    assert data["sku"] == "PROD-001"
    assert data["stock_actual"] == 25