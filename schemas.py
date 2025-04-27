from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class EstadoTarea(str, Enum):
    PENDIENTE = "Pendiente"
    EN_EJECUCION = "En ejecución"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"

class EstadoUsuario(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ELIMINADO = "Eliminado"

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    premium: bool = False

class Usuario(UsuarioBase):
    id: int
    estado: EstadoUsuario
    premium: bool
    
    class Config:
        from_attributes = True

class TareaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TareaCreate(TareaBase):
    usuario_id: int

class Tarea(TareaBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    estado: EstadoTarea
    usuario_id: int
    
    class Config:
        from_attributes = True