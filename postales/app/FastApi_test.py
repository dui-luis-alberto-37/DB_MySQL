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
    print('loading form page')
    return template.TemplateResponse("index.html", {"request": request})

@app.post("/search/")
async def search(request: Request, filter: str = Form(...), search: str = Form(...)):
    print('serch done')
    connection = get_connection()
    results = []
    message = ""

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM cod_post WHERE {filter} LIKE %s;"
            cursor.execute(query, (f"%{search}%",))
            results = cursor.fetchall()
            if not results:
                message = "No se encontraron resultados."
        except Error as e:
            message = f"Error en la consulta: {e}"
        finally:
            connection.close()
            print("Conexión cerrada.")
    else:
        message = "No se pudo conectar a la base de datos."
    print(request, results, message)
    return template.TemplateResponse("response.html", {
        "request": request,
        "results": results,
        "message": message
    })


    

