from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, Tarea
from schemas import UsuarioCreate, TareaCreate
import logging

logger = logging.getLogger(__name__)

def create_usuario(db: Session, usuario: UsuarioCreate):
    try:
        db_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            premium=usuario.premium
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error al crear el usuario (¿email duplicado?)"
        )

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_tarea_usuario(db: Session, tarea: TareaCreate):
    try:
        # Verificar que el usuario existe
        if not db.query(Usuario).filter(Usuario.id == tarea.usuario_id).first():
            raise HTTPException(
                status_code=404,
                detail=f"Usuario con ID {tarea.usuario_id} no encontrado"
            )
            
        db_tarea = Tarea(
            nombre=tarea.nombre,
            descripcion=tarea.descripcion,
            usuario_id=tarea.usuario_id
        )
        db.add(db_tarea)
        db.commit()
        db.refresh(db_tarea)
        return db_tarea
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear tarea: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error al crear la tarea"
        )

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tarea).offset(skip).limit(limit).all()