from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class EstadoTarea(str, enum.Enum):
    PENDIENTE = "Pendiente"
    EN_EJECUCION = "En ejecución"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"

class EstadoUsuario(str, enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ELIMINADO = "Eliminado"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    estado = Column(Enum(EstadoUsuario), default=EstadoUsuario.ACTIVO)
    premium = Column(Boolean, default=False)
    tareas = relationship("Tarea", back_populates="usuario")

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())
    estado = Column(Enum(EstadoTarea), default=EstadoTarea.PENDIENTE)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="tareas")