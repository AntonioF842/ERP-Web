from sqlalchemy.orm import Session
from backend.app.modules.usuarios.models import Usuario
from backend.app.modules.usuarios.schemas import UsuarioCreate
from backend.app.core.security import get_password_hash, verify_password

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario_in: UsuarioCreate):
    # Encripta la contraseña con bcrypt antes de guardar
    hashed_pwd = get_password_hash(usuario_in.password)

    db_usuario = Usuario(
        email=usuario_in.email,
        nombre_completo=usuario_in.nombre_completo,
        hashed_password=hashed_pwd,
        rol=usuario_in.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def authenticate_usuario(db: Session, email: str, password: str):
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        return False
    if not verify_password(password, usuario.hash_password):
        return False
    return usuario
