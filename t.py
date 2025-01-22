import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Conexión a la base de datos
conexion = sqlite3.connect("inventarioo.db")
cursor = conexion.cursor()

# Inicialización de las tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Productos (
    ID_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(20) NOT NULL,
    Cantidad INTEGER NOT NULL,
    Estado VARCHAR(20) NOT NULL,
    Tipo VARCHAR(20) NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Persona (
    Rut VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(20),
    Apellido VARCHAR(20),
    Rol VARCHAR(20)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transaccion (
    ID_Transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    Rut INTEGER,
    Producto_ID INTEGER,
    Fecha DATE,
    Accion VARCHAR(20),
    Cantidad INTEGER,
    Precio INTEGER,
    FOREIGN KEY (Rut) REFERENCES Persona(Rut),
    FOREIGN KEY (Producto_ID) REFERENCES Productos(ID_Producto)
)
""")
conexion.commit()

# Función para agregar producto
def agregar_producto(campos):
    try:
        # Obtener valores desde los campos
        Nombre = campos['nombre'].get()
        Cantidad = int(campos['cantidad'].get())
        Estado = campos['estado'].get()
        Tipo = campos['tipo'].get()

        # Insertar en la base de datos
        cursor.execute("INSERT INTO Productos (Nombre, Cantidad, Estado, Tipo) VALUES (?, ?, ?, ?)",
                       (Nombre, Cantidad, Estado, Tipo))
        conexion.commit()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

# Función para abrir la ventana de productos
def abrir_ventana_productos():
    ventana_productos = tk.Toplevel(ventana)
    ventana_productos.title("Agregar Producto")
    ventana_productos.geometry("400x300")

    # Diccionario para almacenar los campos de entrada
    campos = {}

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_productos)
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    campos['nombre'] = tk.Entry(frame_entrada)
    campos['nombre'].grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
    campos['cantidad'] = tk.Entry(frame_entrada)
    campos['cantidad'].grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Estado:").grid(row=2, column=0, padx=5, pady=5)
    campos['estado'] = tk.Entry(frame_entrada)
    campos['estado'].grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Tipo:").grid(row=3, column=0, padx=5, pady=5)
    campos['tipo'] = tk.Entry(frame_entrada)
    campos['tipo'].grid(row=3, column=1, padx=5, pady=5)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Producto", command=lambda: agregar_producto(campos))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_productos, text="Cerrar", command=ventana_productos.destroy)
    btn_cerrar.pack(pady=10)

# Función para ver todos los productos
def ver_productos():
    ventana_productos = tk.Toplevel(ventana)
    ventana_productos.title("Lista de Productos")
    ventana_productos.geometry("600x400")

    # Tabla para mostrar productos
    tabla = ttk.Treeview(ventana_productos, columns=("Nombre", "Cantidad", "Estado", "Tipo"), show="headings")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Estado", text="Estado")
    tabla.heading("Tipo", text="Tipo")

    tabla.column("Nombre", width=150, anchor="w")  # Ancho razonable para nombres
    tabla.column("Cantidad", width=100, anchor="center")
    tabla.column("Estado", width=100, anchor="center")
    tabla.column("Tipo", width=100, anchor="center")

    tabla.pack(fill=tk.BOTH, expand=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT productos.Nombre, productos.Cantidad, productos.Estado, productos.Tipo FROM Productos")
    productos = cursor.fetchall()

    # Insertar datos en la tabla
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_productos, text="Cerrar", command=ventana_productos.destroy)
    btn_cerrar.pack(pady=10)

# Función para agregar producto
def agregar_personas(campos):
    try:
        # Obtener valores desde los campos
        Rut = campos['rut'].get()
        Nombre = campos['nombre'].get()
        Apellido = campos['apellido'].get()
        Rol = campos['rol'].get()

        # Insertar en la base de datos
        cursor.execute("INSERT INTO Persona (Rut, Nombre, Apellido, Rol) VALUES (?, ?, ?, ?)",
                       (Rut, Nombre, Apellido, Rol))
        conexion.commit()

        messagebox.showinfo("Éxito", "Persona agregado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar a la persona: {e}")


def abrir_ventana_personas():
    ventana_personas = tk.Toplevel(ventana)
    ventana_personas.title("Agregar Personas")
    ventana_personas.geometry("400x300")

    # Diccionario para almacenar los campos de entrada
    campos = {}

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_personas)
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Rut:").grid(row=0, column=0, padx=5, pady=5)
    campos['rut'] = tk.Entry(frame_entrada)
    campos['rut'].grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
    campos['nombre'] = tk.Entry(frame_entrada)
    campos['nombre'].grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Apellido:").grid(row=2, column=0, padx=5, pady=5)
    campos['apellido'] = tk.Entry(frame_entrada)
    campos['apellido'].grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Rol:").grid(row=3, column=0, padx=5, pady=5)
    campos['rol'] = tk.Entry(frame_entrada)
    campos['rol'].grid(row=3, column=1, padx=5, pady=5)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Persona", command=lambda: agregar_personas(campos))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", command=ventana_personas.destroy)
    btn_cerrar.pack(pady=10)


def ver_personas():
    ventana_personas = tk.Toplevel(ventana)
    ventana_personas.title("Lista de Productos")
    ventana_personas.geometry("600x400")

    # Tabla para mostrar productos
    tabla = ttk.Treeview(ventana_personas, columns=("Rut", "Nombre", "Apellido", "Rol"), show="headings")
    tabla.heading("Rut", text="Rut")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("Rol", text="Rol")

    tabla.column("Rut", width=150, anchor="w")  # Ancho razonable para nombres
    tabla.column("Nombre", width=100, anchor="center")
    tabla.column("Apellido", width=100, anchor="center")
    tabla.column("Rol", width=100, anchor="center")

    tabla.pack(fill=tk.BOTH, expand=True)

    # Obtener los datos de la base de datos
    cursor.execute("SELECT * FROM Persona")
    productos = cursor.fetchall()

    # Insertar datos en la tabla
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", command=ventana_personas.destroy)
    btn_cerrar.pack(pady=10)

# Ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("800x400")

# Botón para abrir la ventana de productos
btn_abrir_productos = tk.Button(ventana, text="Agregar Producto", command=abrir_ventana_productos)
btn_abrir_productos.pack(pady=20)

btn_abrir_personas = tk.Button(ventana, text="Agregar Persona", command=abrir_ventana_personas)
btn_abrir_personas.pack(pady=20)

btn_ver_productos = tk.Button(ventana, text="Ver Productos", command=ver_productos)
btn_ver_productos.pack(pady=10)

btn_ver_personas = tk.Button(ventana, text="Ver Personas", command=ver_personas)
btn_ver_personas.pack(pady=10)

# Ejecutar la ventana principal
ventana.mainloop()
