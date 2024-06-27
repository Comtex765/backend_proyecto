from sqlalchemy.orm import Session
from . import models
from . import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        usuario=usuario.usuario,
        contraseña=get_password_hash(usuario.contraseña),
        telefono=usuario.telefono,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuario_by_usuario(db: Session, usuario: str):
    return db.query(models.Usuario).filter(models.Usuario.usuario == usuario).first()


def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Usuario).offset(skip).limit(limit).all()


def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioUpdate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    if db_usuario:
        db_usuario.nombre = usuario.nombre
        db_usuario.apellido = usuario.apellido
        db_usuario.correo = usuario.correo
        db_usuario.usuario = usuario.usuario
        db_usuario.contraseña = get_password_hash(usuario.contraseña)
        db_usuario.telefono = usuario.telefono
        db.commit()
        db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario
