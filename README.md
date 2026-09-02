#  ERP-Web API Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

Sistema ERP Backend de alto rendimiento para la gestión integral de inventarios, procesamiento de ventas con cálculo de impuestos, analítica de negocios y autenticación segura por roles.

---

##  Características Principales

*  **Autenticación & Seguridad:** Autenticación JWT y Hash Bcrypt. Control de acceso por roles (`admin`, `almacen`, `vendedor`).
*  **Gestión de Inventario:** CRUD de productos, trazabilidad de movimientos de almacén (Entradas, Salidas, Ajustes) y alertas de stock bajo.
*  **Procesamiento de Ventas:** Cálculo automático de impuestos (16% IVA), deducción inmediata de stock y flujo de cancelación con devolución de existencias.
*  **Reportes & Dashboard:** Métricas globales de ingresos, volumen de ventas y ranking de productos más vendidos.
*  **Testing Automatizado:** Pruebas unitarias e integración en SQLite en memoria (`StaticPool`) con cobertura total de endpoints.

---

##  Tecnologías Utilizadas

| Componente | Tecnología |
| :--- | :--- |
| **Framework Web** | FastAPI |
| **ORM** | SQLAlchemy 2.0+ |
| **Base de Datos** | SQLite (Persistente en Dev / In-Memory en Tests) |
| **Seguridad** | PyJWT & Passlib (Bcrypt) |
| **Testing** | Pytest & Starlette TestClient |
| **Validación de Datos** | Pydantic v2 |

---

##  Estructura del Proyecto

```text
ERP-Web/
├── backend/
│   ├── app/
│   │   ├── core/           # Seguridad (Tokens JWT, hashing)
│   │   ├── modules/        # Arquitectura modular por dominio
│   │   │   ├── inventario/ # Productos y almacén
│   │   │   ├── reportes/   # Dashboard y analítica
│   │   │   ├── usuarios/   # Autenticación y roles
│   │   │   └── ventas/     # Transacciones y cancelaciones
│   │   ├── config.py       # Configuración global
│   │   ├── database.py     # Conexión SQLAlchemy y Base
│   │   └── main.py         # Punto de entrada de la aplicación
│   └── tests/              # Suite de pruebas automatizadas
├── .env                    # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── erp_database.db         # Base de datos local SQLite
├── pytest.ini              # Configuración de pruebas
├── README.md               # Documentación
└── requirements.txt        # Dependencias del proyecto
```

---

##  Configuración e Instalación

### Requisitos Previos

* Python 3.10 o superior instalado.
* Git (opcional, para clonar el repositorio)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/ERP-Web.git
   cd ERP-Web
2. **Crear y activar el entorno virtual**
    ```bash
    # Crear el entorno virtual
    python -m venv .venv
    
    # Activar el entorno virtual (Windows)
    .venv\Scripts\activate
    
    # Activar el entorno virtual (Linux/Mac)
    source .venv/bin/activate
3. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
4. **Configurar variables de entorno**
   
    Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
   
    ```bash
    PROJECT_NAME="ERP Web API"
    VERSION="1.0.0"
    SECRET_KEY="tu_secret_key_super_segura_para_jwt"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    BACKEND_CORS_ORIGINS=["http://localhost:3000","[http://127.0.0.1:3000](http://127.0.0.1:3000)"]
  
---

## Ejecución de Pruebas Automatizadas

Para ejecutar toda la suite de pruebas unitarias y de integración con Pytest:

```bash
python -m pytest -v
```

---

## Ejecución del Servidor de Desarrollo

Inicia el servidor local con Uvicorn:

```bash
uvicorn backend.app.main:app --reload