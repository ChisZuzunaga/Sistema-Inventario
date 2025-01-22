import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os

# Ruta de la base de datos
basedir = os.path.dirname(__file__)  # Directorio del archivo actual
ruta_bd = os.path.join(basedir, "inventario.db")

# Función para inicializar la base de datos
def inicializar_bd():
    conexion = sqlite3.connect(ruta_bd)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Función para agregar un producto
def agregar_producto(nombre, precio, cantidad):
    if not nombre or precio <= 0 or cantidad <= 0:
        messagebox.showerror("Error", "Todos los campos deben ser válidos.")
        return

    conexion = sqlite3.connect(ruta_bd)
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
                   (nombre, precio, cantidad))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Producto agregado correctamente.")
    mostrar_productos()

# Función para mostrar productos
def mostrar_productos():
    conexion = sqlite3.connect(ruta_bd)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    for fila in tabla.get_children():
        tabla.delete(fila)

    for producto in productos:
        tabla.insert("", tk.END, values=producto)

# Inicializar la base de datos
inicializar_bd()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("600x400")

# Frame para agregar productos
frame_agregar = tk.Frame(ventana)
frame_agregar.pack(pady=10)

# Etiquetas y entradas
lbl_nombre = tk.Label(frame_agregar, text="Nombre del producto:")
lbl_nombre.grid(row=0, column=0, padx=5, pady=5)
entrada_nombre = tk.Entry(frame_agregar)
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

lbl_precio = tk.Label(frame_agregar, text="Precio:")
lbl_precio.grid(row=1, column=0, padx=5, pady=5)
entrada_precio = tk.Entry(frame_agregar)
entrada_precio.grid(row=1, column=1, padx=5, pady=5)

lbl_cantidad = tk.Label(frame_agregar, text="Cantidad:")
lbl_cantidad.grid(row=2, column=0, padx=5, pady=5)
entrada_cantidad = tk.Entry(frame_agregar)
entrada_cantidad.grid(row=2, column=1, padx=5, pady=5)

# Botón para agregar producto
btn_agregar = tk.Button(frame_agregar, text="Agregar Producto",
                        command=lambda: agregar_producto(
                            entrada_nombre.get(),
                            float(entrada_precio.get()),
                            int(entrada_cantidad.get())
                        ))
btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

# Tabla para mostrar productos
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Precio", "Cantidad"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")
tabla.heading("Cantidad", text="Cantidad")
tabla.pack(pady=20, fill=tk.BOTH, expand=True)

# Botón para cargar productos
btn_mostrar = tk.Button(ventana, text="Cargar Productos", command=mostrar_productos)
btn_mostrar.pack(pady=10)

# Mostrar productos al iniciar
mostrar_productos()

# Ejecutar la ventana
ventana.mainloop()