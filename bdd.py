import sqlite3
import tkinter as tk
from tkinter import messagebox

def create_database():
    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect("productos.db")
        cursor = conn.cursor()

        # Crear tabla Productos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Productos (
            ID_Producto INTEGER PRIMARY KEY,
            Nombre VARCHAR(20) NOT NULL,
            Cantidad INTEGER NOT NULL,
            Estado VARCHAR(20) NOT NULL,
            Tipo VARCHAR(20) NOT NULL
        )''')

        # Crear tabla Persona
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Persona (
            Rut_Persona VARCHAR(20) PRIMARY KEY,
            Nombre VARCHAR(20),
            Apellido VARCHAR(20),
            Rol VARCHAR(20)
        )''')

        # Crear tabla Transaccion
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transaccion (
            ID_Transaccion INTEGER PRIMARY KEY,
            Persona_ID INTEGER,
            Producto_ID INTEGER,
            Fecha DATE,
            Accion VARCHAR(20),
            Cantidad INTEGER,
            Precio SMALLMONEY,
            FOREIGN KEY (Persona_ID) REFERENCES Persona(Rut_Persona),
            FOREIGN KEY (Producto_ID) REFERENCES Productos(ID_Producto)
        )''')

        # Insertar datos en Productos
        cursor.executemany('''
        INSERT OR IGNORE INTO Productos (ID_Producto, Nombre, Cantidad, Estado, Tipo) 
        VALUES (?, ?, ?, ?, ?)''', [
            (1, 'Dorado', 50, 'Disponible', 'Pescado'),
            (2, 'Billagay', 100, 'Disponible', 'Pescado'),
            (3, 'Lapa', 30, 'Disponible', 'Marisco'),
            (4, 'Erizo', 20, 'Disponible', 'Marisco')
        ])

        # Insertar datos en Persona
        cursor.executemany('''
        INSERT OR IGNORE INTO Persona (Rut_Persona, Nombre, Apellido, Rol) 
        VALUES (?, ?, ?, ?)''', [
            ('1.234.567-8', 'Juan', 'Pérez', 'Cliente'),
            ('1.234.567-9', 'Ana', 'Gómez', 'Proveedor'),
            ('2.134.567-8', 'Carlos', 'Ruiz', 'Cliente'),
            ('2.134.567-9', 'María', 'López', 'Proveedor'),
            ('3.134.567-8', 'Hernesto', 'López', 'Proveedor')
        ])

        # Insertar datos en Transaccion
        cursor.executemany('''
        INSERT OR IGNORE INTO Transaccion (ID_Transaccion, Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio) 
        VALUES (?, ?, ?, ?, ?, ?, ?)''', [
            (1, '1.234.567-8', 1, '2025-01-28', 'Compra', 2, 1000),
            (2, '1.234.567-8', 2, '2025-01-28', 'Compra', 6, 2000),
            (3, '1.234.567-8', 3, '2025-01-28', 'Venta', 10, 5000),
            (4, '1.234.567-8', 4, '2025-01-28', 'Venta', 25, 8000)
        ])

        # Confirmar cambios y cerrar conexión
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Base de datos creada y datos insertados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear interfaz con Tkinter
root = tk.Tk()
root.title("Crear Base de Datos")
root.geometry("300x200")

label = tk.Label(root, text="Crear Base de Datos SQLite", font=("Arial", 14))
label.pack(pady=20)

button = tk.Button(root, text="Crear Base de Datos", command=create_database, font=("Arial", 12), bg="blue", fg="white")
button.pack(pady=10)

root.mainloop()