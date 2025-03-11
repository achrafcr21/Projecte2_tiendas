from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import users as user

app = FastAPI()

# Crear las tablas en la base de datos (esto solo se ejecuta si las tablas aún no existen)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# Incluir la ruta de usuario
app.include_router(user.router)