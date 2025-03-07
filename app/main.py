from fastapi import FastAPI
from app.database.database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    connection = get_db_connection()
    if connection:
        return {"message": "¡Conexión con MySQL establecida correctamente!"}
    else:
        return {"error": "No se pudo conectar a MySQL"}