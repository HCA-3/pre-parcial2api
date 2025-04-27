from pydantic import BaseModel, EmailStr, Field
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
    nombre: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(..., example="usuario@example.com")

class UsuarioCreate(UsuarioBase):
    premium: bool = False

class Usuario(UsuarioBase):
    id: int
    estado: EstadoUsuario
    premium: bool
    
    class Config:
        from_attributes = True

class TareaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)

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