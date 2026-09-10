# ERP-Web API & Frontend System

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js_3-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PrimeVue](https://img.shields.io/badge/PrimeVue-41B883?style=for-the-badge&logo=primevue&logoColor=white)](https://primevue.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

Sistema ERP Full-Stack de alto rendimiento para la gestión integral de inventarios, terminal de ventas (POS), procesamiento de transacciones con IVA, analítica ejecutable de negocios (BI) y control de acceso por roles.

---

##  Características Principales

###  Backend (FastAPI & SQLAlchemy)
*  **Autenticación & Seguridad:** Autenticación JWT y Hash Bcrypt. Control de acceso restringido por roles (`admin`, `almacen`, `vendedor`).
*  **Gestión de Inventario:** CRUD de productos, trazabilidad completa de movimientos de almacén (Entradas, Salidas, Ajustes) y alertas automáticas de stock crítico.
*  **Procesamiento de Ventas:** Cálculo automático de subtotal e impuestos (16% IVA), deducción inmediata de existencias y flujo de cancelación con reingreso automático al inventario.
*  **Reportes & Business Intelligence:** Endpoints para agregación de métricas financieras y ranking de productos más vendidos por período (Día, Semana, Mes, Año, Todo).
*  **Testing Automatizado:** Pruebas unitarias e integración en SQLite en memoria (`StaticPool`) con cobertura total de endpoints.

###  Frontend (Vue 3, Tailwind CSS & PrimeVue)
*  **UI/UX Limpia y Profesional:** Interfaz adaptativa construida con un sistema de diseño slate/blanco, componentes de PrimeVue (Preset Aura) y clases utilitarias de Tailwind CSS.
*  **Dashboard Interactivo:** Panel de control principal con tarjetas de métricas globales (KPIs), accesos directos a operaciones y vista resumida de stock crítico.
*  **Terminal POS de Ventas:** Sistema de caja con buscador rápido de catálogo, botones compactos de incremento/decremento (`+`/`-`), cálculo transparente de subtotal y total, e historial con detalles.
*  **Gestión de Inventario Avanzada:** Catálogo interactivo con filtrado dinámico, modal para movimientos manuales de almacén (Entradas, Salidas, Ajustes) y exportación de datos a CSV.
*  **Módulo de Reportes & Business Intelligence:** Métricas ejecutivas, visualización gráfica con Chart.js (Barras y Dona), auditoría de movimientos de inventario y exportación a PDF vectorizado estructurado con `jsPDF` / `jspdf-autotable`.

---

##  Tecnologías Utilizadas

| Capa | Tecnología / Herramienta |
| :--- | :--- |
| **Backend Framework** | FastAPI |
| **ORM & Base de Datos** | SQLAlchemy 2.0+ & SQLite (Persistente / In-Memory en Tests) |
| **Seguridad & Auth** | PyJWT, Passlib (Bcrypt) & CORS Middleware |
| **Testing Backend** | Pytest & Starlette TestClient |
| **Frontend Framework** | Vue 3 (Composition API `<script setup>`) |
| **Herramienta de Build** | Vite & `@tailwindcss/vite` |
| **Diseño & Componentes** | Tailwind CSS v4 & PrimeVue (Aura Theme) |
| **Gestión de Estado** | Pinia |
| **Cliente HTTP** | Axios con Interceptores |
| **Visualización & PDF** | Chart.js, PrimeVue Chart, jsPDF & jspdf-autotable |

---

##  Estructura del Proyecto

```text
ERP-Web/
├── backend/
│   ├── app/
│   │   ├── core/           # Seguridad (Tokens JWT, hashing, roles)
│   │   ├── modules/        # Arquitectura modular por dominio
│   │   │   ├── inventario/ # Productos y movimientos de almacén
│   │   │   ├── reportes/   # Dashboard y analítica financiera
│   │   │   ├── usuarios/   # Autenticación, usuarios y roles
│   │   │   └── ventas/     # Transacciones, detalles y cancelaciones
│   │   ├── config.py       # Configuración global
│   │   ├── database.py     # Conexión SQLAlchemy y Base
│   │   └── main.py         # Punto de entrada de la API FastAPI
│   └── tests/              # Suite de pruebas automatizadas
├── frontend/
│   ├── src/
│   │   ├── api/            # Configuración de Axios
│   │   ├── assets/         # Recursos estáticos
│   │   ├── components/     # Componentes UI reutilizables (MetricCard, QuickAccessCard)
│   │   ├── layouts/        # Layout principal con Sidebar responsivo (AppLayout.vue)
│   │   ├── router/         # Rutas de Vue Router con guardias de navegación
│   │   ├── stores/         # Estados globales de Pinia (auth.js)
│   │   ├── views/          # Vistas principales (Dashboard, Inventario, Ventas, Reportes, Login)
│   │   ├── App.vue         # Componente raíz
│   │   ├── main.js         # Inicialización de Vue, PrimeVue y Pinia
│   │   └── style.css       # Configuración global e importación de Tailwind CSS
│   ├── index.html          # Entry point HTML
│   ├── package.json        # Dependencias de Node.js
│   └── vite.config.js      # Configuración de Vite y plugins
├── .env                    # Variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── erp_database.db         # Base de datos local SQLite
├── pytest.ini              # Configuración de pruebas
└── README.md               # Documentación general
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
2. **Configurar el Backend (FastAPI)**
    ```bash
    # Crear el entorno virtual
    python -m venv .venv
    
    # Activar el entorno virtual (Windows)
    .venv\Scripts\activate
    
    # Activar el entorno virtual (Linux/Mac)
    source .venv/bin/activate
    
    # Instalar dependencias del backend
    pip install -r requirements.txt
   
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

    PROJECT_NAME="ERP Web API"
    VERSION="1.0.0"
    SECRET_KEY="tu_secret_key_super_segura_para_jwt"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    BACKEND_CORS_ORIGINS=["http://localhost:3000","[http://127.0.0.1:3000](http://127.0.0.1:3000)"]

3. Configurar el Frontend (Vue 3 + Vite)
Abre una nueva terminal en la carpeta `fronted`:

    ```bash
    cd fonted

    # Instalar dependencias de Node.js
    npm install
    
---

## Ejecución de Sistema 

1. Ejecutar Pruebas Automatizadas (Backend)

   ```bash
   python -m pytest -v

2. Iniciar el Backend (Servidor FastAPI)

   ```bash
   uvicorn backend.app.main:app --reload
 > La API estará disponible en http://127.0.0.1:8000 y la documentación Swagger interactiva en http://127.0.0.1:8000/docs.

3. Iniciar el Frontend (Vite Dev Server)
En la carpeta `frontend`:
   ```bash
   npm run dev
 > La aplicación web estará accesible en http://localhost:5173.

---

## Flujo de Trabajo del ERP

1. **Autenticación:** Inicia sesión con credenciales de usuario para obtener el JWT token y cargar el rol correspondiente.
2. **Dashboard:** Visualiza las métricas clave del día, productos destacados y alertas rápidas de reabastecimiento.
3. **Inventario:** Agrega o edita productos del catálogo, realiza movimientos manuales (Entradas/Salidas/Ajustes) y exporta registros a CSV.
4. **Ventas (POS):** Agrega items al carrito, ajusta cantidades con controles de existencias, calcula subtotal e IVA, procesa transacciones y consulta el historial con opción de cancelación o generación de recibo digital en PDF.
5. **Reportes & BI:** Filtra la información financiera por Día, Semana, Mes o Año, analiza visualmente con gráficos de barras/dona, revisa la auditoría de stock y exporta informes ejecutivos en PDF estructurado o CSV.

   
