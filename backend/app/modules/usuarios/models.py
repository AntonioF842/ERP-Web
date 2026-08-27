from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from backend.app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    hash_password = Column(String(105),nullable=False)
    rol = Column(String(50), nullable=False, default="usuario") # Admin, almacen, vendedor
    activo =Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)