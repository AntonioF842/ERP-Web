import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, get_db
from backend.app.core.security import get_password_hash

# 1. IMPORTANTE: Importar todos los modelos para que se registren en Base.metadata
from backend.app.modules.usuarios.models import Usuario
from backend.app.modules.inventario.models import Producto, MovimientoInventario
from backend.app.modules.ventas.models import Venta, DetalleVenta

# 2. Configurar SQLite en memoria con StaticPool para compartir el mismo canal de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea la estructura de la base de datos limpia antes de cada prueba."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Importa FastAPI e inyecta la sesión de pruebas."""
    from backend.app.main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    """Crea el usuario administrador base para los tests de autorización."""
    usuario = Usuario(
        email="admin@erp.com",
        nombre_completo="Admin Pruebas",
        hashed_password=get_password_hash("admin123"),
        rol="admin",
        activo=True
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario