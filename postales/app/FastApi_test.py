from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_ROOT_USER = os.getenv("DB_ROOT_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def get_connection():
    print('getting conexion')
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_ROOT_USER,
            password=DB_ROOT_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        
        print('Conexión exitosa a la base de datos')
        return conn
    except Error as e:
        print("Error conectando a MySQL:", e)
        return None


template = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="statics"), name="static")


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.post("/search/")
async def search(request: Request, filter: str = Form(...), search: str = Form(...)):
    dic = {
        'codigo': 'd_codigo',
        'asentamiento': 'd_asenta',
        'tipo_asentamiento': 'd_tipo_asenta',
        'municipio': 'D_mnpio',
        'estado': 'd_estado',
        'ciudad': 'd_ciudad',
        'cp_admin_postal': 'd_CP',
        'clave_entidad': 'c_estado',
        'clave_tipo_asentamiento': 'c_tipo_asenta',
        'clave_municipio': 'c_mnpio',
        'id_asentamiento': 'id_asenta_cpcons',
        'zona_asentamiento': 'd_zona',
        'clave_ciudad': 'c_cve_ciudad',
    }
    filter = dic[filter]
    connection = get_connection()
    results = []
    message = ""
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM cod_post WHERE {filter} LIKE '%{search}%';"
            print(f"Executing query: {query}")
            cursor.execute(query)
            results = cursor.fetchall()
            if not results:
                message = "No se encontraron resultados."
                return template.TemplateResponse("no_res.html", {
                    "request": request,
                    "message": message})
            else:
                columns = list(results[0].keys()) if results else []
                
        except Error as e:
            message = f"Error en la consulta '{e}'"
            return template.TemplateResponse("no_res.html", {
                    "request": request,
                    "message": message})
        finally:
            connection.close()
            print("Conexión cerrada.")
    else:
        message = "No se pudo conectar a la base de datos."
    return template.TemplateResponse("response.html", {
        "request": request,
        "results": results,
        "message": message,
        "columns": columns
    })


    

