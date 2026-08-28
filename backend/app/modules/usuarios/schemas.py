from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# Esquema para registrar un nuevo usaurio
class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre_completo: str
    password: str
    rol: Optional[str] = "usuario"

# Esquema de respuesta para el ususro (omite la contraseña)
class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr
    nombre_completo: str
    rol: str
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Esquema de respues al hacer login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
