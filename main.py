from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db
import os
import uvicorn

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tareas", version="1.0.0")

# Configuración CORS para Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz para verificar que la API está funcionando
@app.get("/")
def read_root():
    return {
        "message": "API de Seguimiento de Tareas",
        "docs": "/docs",
        "status": "operativo"
    }

# Operaciones de Usuario
@app.post("/usuarios/", response_model=schemas.Usuario, status_code=201)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=List[schemas.Usuario])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip=skip, limit=limit)

# Operaciones de Tarea
@app.post("/tareas/", response_model=schemas.Tarea, status_code=201)
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    return crud.create_tarea_usuario(db=db, tarea=tarea)

@app.get("/tareas/", response_model=List[schemas.Tarea])
def leer_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tareas(db, skip=skip, limit=limit)

# Configuración para producción
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False, workers=2)