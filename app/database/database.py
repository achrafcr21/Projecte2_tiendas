import mysql.connector

# Configurar la conexión a MySQL manualmente
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "system",
    "database": "digitalizacion_tiendas"
}

# Función para obtener la conexión
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        return None