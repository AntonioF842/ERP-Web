from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.modules.usuarios import services, schemas
from backend.app.core import security
from backend.app.modules.usuarios.models import Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios & Autentificación"]
)

# Registro de usuarios
@router.post("/registro", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuarios(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = services.get_usuarios_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo electrónico ya se encuentra registrado")
    return services.create_usuario(db=db, usuario_in=usuario)

# Login (Token JWT)
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = services.authenticate_usuario(db, email=form_data.username, password=form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    # Genera Token firmado
    access_token = security.create_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Obtener mi perfil(Ruta protegida)
@router.get("/me", response_model=schemas.UsuarioResponse)
def obtener_perfil_actual(current_user: Usuario = Depends(security.get_current_user)):
    return current_user