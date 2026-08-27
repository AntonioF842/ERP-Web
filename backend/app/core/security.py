from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# Configuracion de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para firmar tokens
SECRET_KEY = "clasito"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

# Encriptar password en texto plano
def get_password_hash(passoword: str) -> str:
    return pwd_context.hash(passoword)

# Verificar si el password ingresasdo coincide
def verufy_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generar Token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt