import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Conexión a la base de datos
conexion = sqlite3.connect("inventarioo.db")
cursor = conexion.cursor()

# Inicialización de las tablas (si no existen)
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
    ID_Persona INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR(20),
    Apellido VARCHAR(20),
    Rol VARCHAR(20)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transaccion (
    ID_Transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    Persona_ID INTEGER,
    Producto_ID INTEGER,
    Fecha DATE,
    Accion VARCHAR(20),
    Cantidad INTEGER,
    Precio INTEGER,
    FOREIGN KEY (Persona_ID) REFERENCES Persona(ID_Persona),
    FOREIGN KEY (Producto_ID) REFERENCES Productos(ID_Producto)
)
""")
conexion.commit()

def agregar_cliente():
    pass


# Función para agregar una transacción
def agregar_transaccion():
    persona_id = int(entrada_persona_id.get())
    producto_id = int(entrada_producto_id.get())
    accion = entrada_accion.get()
    cantidad = int(entrada_cantidad.get())
    precio = int(entrada_precio.get())
    fecha = datetime.date.today()
    
    # Validar cantidad disponible si es una venta
    if accion.lower() == "venta":
        cursor.execute("SELECT Cantidad FROM Productos WHERE ID_Producto = ?", (producto_id,))
        producto = cursor.fetchone()
        if producto is None:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        cantidad_disponible = producto[0]
        if cantidad > cantidad_disponible:
            messagebox.showerror("Error", "Cantidad insuficiente en inventario.")
            return
        cursor.execute("UPDATE Productos SET Cantidad = Cantidad - ? WHERE ID_Producto = ?", (cantidad, producto_id))
    
    # Insertar la transacción
    cursor.execute("""
    INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (persona_id, producto_id, fecha, accion, cantidad, precio))
    conexion.commit()
    messagebox.showinfo("Éxito", "Transacción registrada correctamente.")
    mostrar_transacciones()

def abrir_nueva_ventana():
    # Crear una nueva ventana secundaria
    nueva_ventana = tk.Toplevel(ventana)
    nueva_ventana.title("Nueva Ventana")
    nueva_ventana.geometry("300x200")
    
    # Agregar widgets a la nueva ventana
    etiqueta = tk.Label(nueva_ventana, text="¡Bienvenido a la nueva ventana!")
    etiqueta.pack(pady=20)
    
    boton_cerrar = tk.Button(nueva_ventana, text="Cerrar", command=nueva_ventana.destroy)
    boton_cerrar.pack(pady=10)

# Función para mostrar transacciones
def mostrar_transacciones():
    for fila in tabla.get_children():
        tabla.delete(fila)
    
    cursor.execute("""
    SELECT t.ID_Transaccion, p.Nombre, pr.Nombre, t.Fecha, t.Accion, t.Cantidad, t.Precio
    FROM Transaccion t
    JOIN Persona p ON t.Persona_ID = p.ID_Persona
    JOIN Productos pr ON t.Producto_ID = pr.ID_Producto
    """)
    transacciones = cursor.fetchall()
    for transaccion in transacciones:
        tabla.insert("", tk.END, values=transaccion)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Inventario - Transacciones")
ventana.geometry("800x400")

# Entradas para registrar transacción
frame_entrada = tk.Frame(ventana)
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Persona ID:").grid(row=0, column=0, padx=5, pady=5)
entrada_persona_id = tk.Entry(frame_entrada)
entrada_persona_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Producto ID:").grid(row=1, column=0, padx=5, pady=5)
entrada_producto_id = tk.Entry(frame_entrada)
entrada_producto_id.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Acción (compra/venta):").grid(row=2, column=0, padx=5, pady=5)
entrada_accion = tk.Entry(frame_entrada)
entrada_accion.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
entrada_cantidad = tk.Entry(frame_entrada)
entrada_cantidad.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Precio:").grid(row=4, column=0, padx=5, pady=5)
entrada_precio = tk.Entry(frame_entrada)
entrada_precio.grid(row=4, column=1, padx=5, pady=5)

# Botón para agregar transacción
btn_agregar = tk.Button(frame_entrada, text="Registrar Transacción", command=agregar_transaccion)
btn_agregar.grid(row=5, column=0, columnspan=2, pady=10)
boton_abrir = tk.Button(ventana, text="Abrir Nueva Ventana", command=abrir_nueva_ventana)
boton_abrir.pack(pady=20)

# Tabla para mostrar transacciones
tabla = ttk.Treeview(ventana, columns=("ID", "Persona", "Producto", "Fecha", "Acción", "Cantidad", "Precio"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Persona", text="Persona")
tabla.heading("Producto", text="Producto")
tabla.heading("Fecha", text="Fecha")
tabla.heading("Acción", text="Acción")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Precio", text="Precio")
tabla.pack(pady=20, fill=tk.BOTH, expand=True)

# Mostrar transacciones al iniciar
mostrar_transacciones()

# Ejecutar la ventana
ventana.mainloop()
