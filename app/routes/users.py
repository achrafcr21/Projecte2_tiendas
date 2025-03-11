from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioResponse

router = APIRouter()

# Crear usuario
@router.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Crear usuario en la base de datos
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña=usuario.contraseña,  # En producción, hay que encriptar esto
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario