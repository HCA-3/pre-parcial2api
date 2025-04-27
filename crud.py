from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Usuario, Tarea
from schemas import UsuarioCreate, TareaCreate

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        premium=usuario.premium
    )
    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        return get_usuario_by_email(db, usuario.email)

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tarea).offset(skip).limit(limit).all()

def get_tareas_usuario(db: Session, usuario_id: int):
    return db.query(Tarea).filter(Tarea.usuario_id == usuario_id).all()

def create_tarea_usuario(db: Session, tarea: TareaCreate):
    db_tarea = Tarea(
        nombre=tarea.nombre,
        descripcion=tarea.descripcion,
        usuario_id=tarea.usuario_id
    )
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def update_estado_tarea(db: Session, tarea_id: int, nuevo_estado: str):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not db_tarea:
        return None
    db_tarea.estado = nuevo_estado
    db.commit()
    db.refresh(db_tarea)
    return db_tarea