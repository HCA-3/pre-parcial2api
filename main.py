from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db
import uvicorn

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Operaciones de Usuario
@app.post("/usuarios/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=List[schemas.Usuario])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# Operaciones de Tarea
@app.post("/usuarios/{usuario_id}/tareas/", response_model=schemas.Tarea)
def crear_tarea_usuario(
    usuario_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)
):
    return crud.create_tarea_usuario(db=db, tarea=tarea)

@app.get("/tareas/", response_model=List[schemas.Tarea])
def leer_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tareas = crud.get_tareas(db, skip=skip, limit=limit)
    return tareas

@app.get("/usuarios/{usuario_id}/tareas/", response_model=List[schemas.Tarea])
def leer_tareas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return crud.get_tareas_usuario(db, usuario_id=usuario_id)

@app.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def actualizar_estado_tarea(
    tarea_id: int, estado: schemas.EstadoTarea, db: Session = Depends(get_db)
):
    db_tarea = crud.update_estado_tarea(db, tarea_id=tarea_id, nuevo_estado=estado)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Cambia 0.0.0.0 por 127.0.0.1