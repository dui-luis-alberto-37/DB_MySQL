from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_ROOT_USER"),
    "password": os.getenv("DB_ROOT_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)



app = FastAPI(title="API de Códigos Postales")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeo de los nombres "bonitos" a los nombres de columna en la DB
FIELD_MAP = {
    'Codigo': 'd_codigo',
    'Asentamiento': 'd_asenta',
    'Tipo de asentamiento': 'd_tipo_asenta',
    'Municipio': 'D_mnpio',
    'Estado': 'd_estado',
    'Ciudad': 'd_ciudad',
    'CP de Administracion Postal': 'd_CP',
    'Clave Entidad': 'c_estado',
    'Clave tipo de asentamiento': 'c_tipo_asenta',
    'Clave del Municipio': 'c_mnpio',
    'Idientificador del asentamiento': 'id_asenta_cpcons',
    'Zona del asentamiento': 'd_zona',
    'Clave de la ciudad': 'c_cve_ciudad',
}

@app.get("/buscar/")
def buscar(campo: str = Query(..., description="Campo de búsqueda"), valor: str = Query(..., description="Valor a buscar")):
    if campo not in FIELD_MAP:
        return JSONResponse(status_code=400, content={"error": "Campo no válido"})

    column = FIELD_MAP[campo]

    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM cod_post WHERE {column} LIKE %s;"
    cursor.execute(query, (f"%{valor}%",))
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    # Convertir a lista de diccionarios
    data = [dict(zip(cols, row)) for row in rows]

    cursor.close()
    conn.close()
    
    return {"count": len(data), "results": data}

@app.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI en Docker (intento de actualizacion)!"}



@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"saludo": f"Hola, {nombre}!"}