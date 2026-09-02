def test_registro_ususario(client):
    response = client.post(
        "/api/v1/usuarios/registro",
        json={
            "email": "nuevo@erp.com",
            "nombre_completo": "Nuevo Usuario",
            "password": "password123",
            "rol": "vendedor",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "nuevo@erp.com"
    assert "id" in data

def test_login_exitoso(client, admin_user):
    renseponse = client.post(
        "/api/v1/usuarios/login",
        data={"username": "admin@erp.com", "password": "admin123"}
    )
    assert renseponse.status_code == 200
    data = renseponse.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fallido(client, admin_user):
    response = client.post(
        "/api/v1/usuarios/login",
        data={"username": "admin@erp.com", "password": "clave_incorrecta"}
    )
    assert response.status_code == 401