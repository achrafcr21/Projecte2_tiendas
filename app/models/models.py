from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base  # Ahora sí importamos Base correctamente

class Usuario(Base):
    __tablename__ = "usuarios"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)  # Asegurar encriptación en producción
    rol = Column(String(50), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)