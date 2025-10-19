import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# Función para mostrar detalle al hacer doble clic
# -----------------------
def ver_detalle(event):
    seleccionado = tabla.focus()
    if not seleccionado:
        return
    valores = tabla.item(seleccionado, "values")
    titulo, descripcion = valores
    messagebox.showinfo(f"Detalle de {titulo}", descripcion)

# -----------------------
# Ventana principal
# -----------------------
ventana = tk.Tk()
ventana.title("Tabla con texto largo y detalles")
ventana.geometry("700x300")

# -----------------------
# Estilo visual de la tabla
# -----------------------
style = ttk.Style()
style.configure("Treeview", font=("Arial", 11), rowheight=40)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# -----------------------
# Creación de la tabla
# -----------------------
tabla = ttk.Treeview(
    ventana,
    columns=("titulo", "descripcion"),
    show="headings"
)

tabla.heading("titulo", text="Título")
tabla.heading("descripcion", text="Descripción")
tabla.column("titulo", width=150, anchor="center")
tabla.column("descripcion", width=500, anchor="w")

# -----------------------
# Scrollbar vertical
# -----------------------
scroll = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
tabla.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# -----------------------
# Insertar datos
# -----------------------
datos = [
    (
        "Registro 1",
        "Este es un texto largo que describe información detallada del registro 1. "
        "Puedes hacer doble clic para ver el texto completo sin que se corte."
    ),
    (
        "Registro 2",
        "Otro texto aún más largo que podría ocupar varias líneas. "
        "Como el Treeview no ajusta automáticamente la altura, usamos un rowheight mayor y "
        "mostramos los detalles en una ventana emergente al hacer doble clic."
    ),
    (
        "Registro 3",
        "Breve descripción sin problema de longitud."
    )
]

for fila in datos:
    # se insertan con saltos manuales para mejor presentación visual
    descripcion_envuelta = '\n'.join([fila[1][i:i+60] for i in range(0, len(fila[1]), 60)])
    tabla.insert("", "end", values=(fila[0], descripcion_envuelta))

# -----------------------
# Vincular evento de doble clic
# -----------------------
tabla.bind("<Double-1>", ver_detalle)

ventana.mainloop()
