import mysql.connector
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkinter import ttk

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)

print('Conexión exitosa a la base de datos')


def line_break(text, length = 10):
    if isinstance(text, str) == False:
        return text
    
    
    return '\n'.join([text[i:i+length] for i in range(0, len(text), lengtCodigoh)])



def Search():
    dic = {
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
    cursor = connection.cursor()
    filter_ = filter.get(tk.ACTIVE)
    search_ = search.get()
    filter_ =  dic[filter_] 
    cursor.execute(f"SELECT * FROM cod_post WHERE {filter_} LIKE '%{search_}%';")
    cols = [desc[0] for desc in cursor.description]
    l_cursor = list(cursor)
    presentar(l_cursor, titles = cols)
    return True

def presentar(output, titles):
    nueva_v = tk.Toplevel(ventana)
    nueva_v.title('Resultados')
    nueva_v.geometry("1100x400")
    
    tabla_df(output, titles, ventana=nueva_v)
    
    tk.Button(nueva_v, text="Nueva busqueda", command=nueva_v.destroy).pack(pady=10)
    boton_close = tk.Button(nueva_v, text="Cerrar conexión", command=ventana.destroy)
    boton_close.pack()
    return True

def tabla1(data, titles, ventana):
    tabla = ttk.Treeview(ventana, columns=titles, show="headings")
    for title in titles:
        tabla.heading(title, text=title)
        tabla.column(title, width=50)
    tabla.pack(fill="both", expand=True)
    datos = data
    
    for d in datos:
        tabla.insert("", tk.END, values=d)
    
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

def tabla_df(data,titles, ventana):
    df = pd.DataFrame(data, columns=titles)
    df = df.map(line_break)
    print(df.head(5))
    tabla = ttk.Treeview(ventana, columns=list(df.columns), show="headings")
    for col in df.columns:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(fill="both", expand=True)
    
    for index, row in df.iterrows():
        tabla.insert("", tk.END, values=list(row), )
    
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
    scrollbar_h = ttk.Scrollbar(ventana, orient="horizontal", command=tabla.xview)
    tabla.configure(yscroll=scrollbar.set)
    tabla.configure(xscroll=scrollbar_h.set)
    scrollbar.pack(side="right", fill="y")
    scrollbar_h.pack(side="top", fill="x")


ventana = tk.Tk()
ventana.title("Tables")
ventana.geometry("300x500")

tk.Label(ventana, text="Buscar por:").pack()
filter = tk.Listbox(ventana, width=10, height=2,)

options = ['Codigo', 'Asentamiento', 'Tipo de asentamiento', 'Municipio',
            'Estado', 'Ciudad', 'CP de Administracion Postal', 'Clave Entidad',
            'Clave tipo de asentamiento', 'Clave del Municipio',
            'Idientificador del asentamiento', 'Zona del asentamiento',
            'Clave de la ciudad']


for option in options:
    filter.insert(tk.END, option)
filter.pack()

tk.Label(ventana, text="Inserte nombre").pack()
search = tk.Entry(ventana)
search.pack()

boton_search = tk.Button(ventana, text="Buscar", command=Search)
boton_search.pack(pady=10)

boton_close = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
boton_close.pack()


# texto = tk.Text(ventana,  width=50, height=5)
# texto.insert("2.0", "Este es un texto largo que se ajusta automáticamente al ancho del widget.")
# # texto.config(state="disabled")  # solo lectura
# texto.pack(padx=10, pady=10)


ventana.mainloop()

if 'connection' in locals() and connection.is_connected():
    connection.close()
    print("Conexión cerrada.")
