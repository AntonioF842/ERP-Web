def test_endpoints_reportes(client, admin_user):
    login_res = client.post(
        "/api/v1/usuarios/login",
        data={"username": "admin@erp.com", "password": "admin123"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res_stock = client.get("/api/v1/reportes/stock-bajo", headers=headers)
    assert res_stock.status_code == 200
    assert isinstance(res_stock.json(), list)

    res_resumen = client.get("/api/v1/reportes/resumen", headers=headers)
    assert res_resumen.status_code == 200
    assert "total_ventas_realizadas" in res_resumen.json()

    res_top = client.get("/api/v1/reportes/top-productos", headers=headers)
    assert res_top.status_code == 200
    assert isinstance(res_top.json(), list)