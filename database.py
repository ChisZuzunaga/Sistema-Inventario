import sqlite3
import os
import shutil
import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar

DB_NAME = "productos.db"
CARPETA_BACKUP = "Copias-De-Seguridad"
DB_ORIGINAL = "productos.db"

conexion = sqlite3.connect(DB_NAME)
cursor = conexion.cursor()

def create_database():
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect(DB_NAME)
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

    # Confirmar cambios y cerrar conexión
    conn.commit()
    conn.close()

def limpiar_base_datos():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar todos los registros?")
        if not confirmacion:
            return  # Si el usuario cancela, no hacer nada

        # Eliminar datos de todas las tablas
        cursor.execute("DELETE FROM Transaccion;")
        cursor.execute("DELETE FROM Persona;")
        cursor.execute("DELETE FROM Productos;")
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Todos los registros han sido eliminados.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo limpiar la base de datos: {e}")

def hacer_copia_seguridad():
    try:
        # Nombre con fecha y hora
        from datetime import datetime   
        fecha_hora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        backup_path = os.path.join(CARPETA_BACKUP, f"backup_{fecha_hora}.db")

        # Copiar base de datos
        shutil.copy(DB_ORIGINAL, backup_path)

        messagebox.showinfo("Éxito", f"Copia de seguridad guardada en:\n{backup_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo hacer la copia de seguridad:\n{str(e)}")

# Función para restaurar copia de seguridad
def restaurar_copia_seguridad():
    def seleccionar_backup(event):
        seleccion = listbox.curselection()
        if seleccion:
            archivo_seleccionado = listbox.get(seleccion[0])
            backup_path = os.path.join(CARPETA_BACKUP, archivo_seleccionado)
            info = obtener_info_tablas(backup_path)

            # Mostrar información en el Label
            info_texto.set(f"Productos: {info.get('Productos', 'Error')}\n"
                           f"Ventas: {info.get('Ventas', 'Error')}\n"
                           f"Ventas [$]: {info.get('Ventas_Dinero', 'Error')}\n"
                           f"Compras: {info.get('Compras', 'Error')}\n"
                           f"Compras [$]: {info.get('Compras_Dinero', 'Error')}\n"
                           f"Personas: {info.get('Personas', 'Error')}\n"
                           f"Transacciones: {info.get('Transacciones', 'Error')}\n"
                           f"Utilidad [$]: {info.get('Utilidad', 'Error')}\n")

    def confirmar_restauracion():
        seleccion = listbox.curselection()
        if seleccion:
            archivo_seleccionado = listbox.get(seleccion[0])
            backup_path = os.path.join(CARPETA_BACKUP, archivo_seleccionado)

            # Confirmar
            if messagebox.askyesno("Restaurar", f"¿Deseas restaurar la base de datos desde {archivo_seleccionado}?"):
                shutil.copy(backup_path, DB_ORIGINAL)
                messagebox.showinfo("Éxito", "Base de datos restaurada correctamente.")

            ventana.destroy()

    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("Restaurar copia de seguridad")
    ventana.geometry("600x300")
    ventana.config(bg="#242224")

    # Lista de archivos de respaldo
    archivos = sorted(os.listdir(CARPETA_BACKUP), reverse=True)

    listbox = Listbox(ventana)
    for archivo in archivos:
        listbox.insert(tk.END, archivo)

    listbox.bind("<<ListboxSelect>>", seleccionar_backup)

    # Colocar Listbox con place()
    listbox.place(x=10, y=10, width=360, height=270)
    listbox.config(bg="#333538", fg="white")

    # Scrollbar
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=listbox.yview)
    scrollbar.place(x=370, y=10, height=270)  # Ajustamos la posición y la altura
    scrollbar.config(bg="#2A2B2A")

    # Vincular scrollbar con listbox
    listbox.config(yscrollcommand=scrollbar.set)

    # Información de la base de datos
    info_texto = tk.StringVar()
    label_info = tk.Label(ventana, textvariable=info_texto, justify=tk.LEFT)
    label_info.config(font=('Arial', 12),bg="#242224", fg="white")
    label_info.place(x=410, y=30)

    # Botones
    btn_aceptar = tk.Button(ventana, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=confirmar_restauracion)
    btn_aceptar.place(x=410, y=250, width=75, height=30)

    btn_cancelar = tk.Button(ventana, text="Cancelar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana.destroy)
    btn_cancelar.place(x=500, y=250, width=75, height=30)

    ventana.mainloop()

def obtener_info_tablas(db_path):
    """Get information about the tables in the database."""
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    info = {}
    try:
        cursor.execute("SELECT COUNT(*) FROM Productos")
        info["Productos"] = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Compra'")
        info["Compras"] = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(CASE WHEN Accion = 'Compra' THEN Precio ELSE 0 END) AS Compras FROM Transaccion")
        info["Compras_Dinero"] = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Venta'")
        info["Ventas"] = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(CASE WHEN Accion = 'Venta' THEN Precio ELSE 0 END) AS Ventas FROM Transaccion")
        info["Ventas_Dinero"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Persona")
        info["Personas"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Transaccion")
        info["Transacciones"] = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(CASE WHEN Accion = 'Venta' THEN Precio ELSE 0 END) - SUM(CASE WHEN Accion = 'Compra' THEN Precio ELSE 0 END) AS Utilidad FROM Transaccion")
        info["Utilidad"] = cursor.fetchone()[0]

    except sqlite3.Error as e:
        info["Error"] = str(e)

    conexion.close()
    return info

def exportar_bd_excel():
    try:
        conn = sqlite3.connect(DB_NAME)
        tablas = ["Productos", "Persona", "Transaccion"]

        # Generar un nombre de archivo predeterminado con la fecha actual
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        nombre_predeterminado = f"BD_INVENTARIO_{fecha_actual}.xlsx"

        archivo_destino = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Guardar base de datos como",
            initialfile=nombre_predeterminado  # Nombre por defecto
        )

        if not archivo_destino:
            return  # Si el usuario cancela, no hacer nada

        with pd.ExcelWriter(archivo_destino, engine="xlsxwriter") as writer:
            for tabla in tablas:
                df = pd.read_sql_query(f"SELECT * FROM {tabla}", conn)
                df.to_excel(writer, sheet_name=tabla, index=False)
        
        conn.close()
        messagebox.showinfo("Éxito", "Base de datos exportada correctamente a Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar la base de datos: {e}")

def importar_bd_excel():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        archivo_origen = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx")],
            title="Seleccionar archivo de base de datos"
        )

        if not archivo_origen:
            return  # Si el usuario cancela, no hacer nada

        xls = pd.ExcelFile(archivo_origen)
        tablas = ["Productos", "Persona", "Transaccion"]

        for tabla in tablas:
            if tabla in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=tabla)
                cursor.execute(f"DELETE FROM {tabla}")  # Limpiar tabla antes de importar
                df.to_sql(tabla, conn, if_exists="append", index=False)

        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Base de datos importada correctamente desde Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo importar la base de datos: {e}")
