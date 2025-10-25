import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Leer las variables
DB_HOST = os.getenv("DB_HOST")
DB_ROOT_USER = os.getenv("DB_ROOT_USER")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

try:
    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_ROOT_USER,
        password=DB_ROOT_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

    if conn.is_connected():
        print("✅ Conexión exitosa a MySQL")
        cursor = conn.cursor()

        # Prueba simple
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("🕒 Hora actual del servidor:", result[0])

        cursor.close()

except Error as e:
    print(f"❌ Error al conectar a MySQL: {e}")

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔒 Conexión cerrada.")