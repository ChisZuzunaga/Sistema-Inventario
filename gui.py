import tkinter as tk
import sqlite3
import os
import shutil
import pandas as pd
from tkinter import ttk, messagebox, filedialog, Listbox, Scrollbar
from datetime import datetime
from PIL import Image, ImageTk  # Usado para cargar imágenes JPG/PNG

root = tk.Tk()
root.title("Sistema de Inventario")
root.geometry("1340x630")
root.configure(bg="#232323")
root.resizable(False, False)

# Carpeta de copias de seguridad
CARPETA_BACKUP = "Copias-De-Seguridad"

# Nombre de la base de datos original
DB_ORIGINAL = "productos.db"

# Conectar con la base de datos
DB_NAME = "productos.db"

conexion = sqlite3.connect(DB_NAME)
cursor = conexion.cursor()

# Crear los frames (simulando pestañas)
main_page = tk.Frame(root, bg="#232323")  # Pestaña 1
clientes_page = tk.Frame(root, bg="#232323")  # Pestaña 2
productos_page = tk.Frame(root, bg="#232323")  # Pestaña 3
transac_page = tk.Frame(root, bg="#232323")  # Pestaña 4
reports_page = tk.Frame(root, bg="#AAAAAA")  # Pestaña 5
config_page = tk.Frame(root, bg="#232323")  # Pestaña 6

frames = [main_page, clientes_page, productos_page, transac_page, reports_page, config_page]

# Crear carpeta si no existe
if not os.path.exists(CARPETA_BACKUP):
    os.makedirs(CARPETA_BACKUP)

# Diccionario para asociar pestañas con imágenes y texto
tabs = {
    "dashboard": {
        "frame": main_page,
        "image_tag": "dashboard_img",  # Identificador de la imagen
        "text_tag": "dashboard_text",  # Identificador del texto
        "image_default": "Img/Dash-Default.png",
        "image_active": "Img/Dash-Active.png",
    },
    "personas": {
        "frame": clientes_page,
        "image_tag": "personas_img",
        "text_tag": "personas_text",
        "image_default": "Img/People-Default.png",
        "image_active": "Img/People-Active.png",
    },
    "productos": {
        "frame": productos_page,
        "image_tag": "productos_img",
        "text_tag": "productos_text",
        "image_default": "Img/Products-Default.png",
        "image_active": "Img/Products-Active.png",
    },
    "transacciones": {
        "frame": transac_page,
        "image_tag": "transac_img",
        "text_tag": "transac_text",
        "image_default": "Img/Transac-Default.png",
        "image_active": "Img/Transac-Active.png",
    },
    "reportes": {
        "frame": reports_page,
        "image_tag": "report_img",
        "text_tag": "report_text",
        "image_default": "Img/Report-Default.png",
        "image_active": "Img/Report-Active.png",
    },
    "configuracion": {
        "frame": config_page,
        "image_tag": "config_img",
        "text_tag": "config_text",
        "image_default": "Img/Config-Default.png",
        "image_active": "Img/Config-Active.png",
    },
}

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

def actualizar_contenido():
    main_page.after(100, get_clientes)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_proveedor)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_productos)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_compras)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_ventas)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_transacciones)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_utilidad)  # Ejecuta la función 100ms después de iniciar la main_page
    mostrar_productos()
    mostrar_personas()
    mostrar_transacciones()
    main_page.after(100, actualizar_menu)

def actualizar_menu():
    opciones = obtenerProductos_informe()  # Obtener productos actualizados
    menu_opcion_producto_informe["menu"].delete(0, "end")  # Borrar opciones anteriores

    # Agregar las nuevas opciones
    for opcion in opciones:
        menu_opcion_producto_informe["menu"].add_command(
            label=opcion, command=lambda value=opcion: opcion_producto_informe.set(value)
        )
    
    # Restablecer el texto inicial del menú después de actualizar
    opcion_producto_informe.set("Seleccione un producto")

# Función para hacer una copia de seguridad
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

# Función para contar registros en las tablas
def obtener_info_tablas(db_path):
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
        
        actualizar_contenido()
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

        actualizar_contenido()
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Base de datos importada correctamente desde Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo importar la base de datos: {e}")

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
        
        actualizar_contenido()
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Todos los registros han sido eliminados.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo limpiar la base de datos: {e}")

def mostrar_pestaña(selected_tab):
    # Ocultar todos los frames
    for tab in tabs.values():
        tab["frame"].pack_forget()

    # Mostrar el frame seleccionado
    tabs[selected_tab]["frame"].pack(fill="both", expand=True)

    # Actualizar imágenes y texto
    for tab_name, tab_info in tabs.items():
        if tab_name == selected_tab:
            # Cambiar a la imagen activa
            active_image = ImageTk.PhotoImage(Image.open(tab_info["image_active"]))
            canvas2.itemconfig(tab_info["image_tag"], image=active_image)
            canvas2.itemconfig(tab_info["text_tag"], fill="#1F68A3")  # Texto activo
            tabs[tab_name]["active_image"] = active_image  # Mantener referencia
            actualizar_contenido()
        else:
            # Cambiar a la imagen por defecto
            default_image = ImageTk.PhotoImage(Image.open(tab_info["image_default"]))
            canvas2.itemconfig(tab_info["image_tag"], image=default_image)
            canvas2.itemconfig(tab_info["text_tag"], fill="white")  # Texto inactivo
            tabs[tab_name]["default_image"] = default_image  # Mantener referencia
            actualizar_contenido()

def validar_numero(event, campo, label_error):
    """Valida que solo se ingresen números en el campo."""
    entrada = campo.get()
    if not entrada.isdigit():
        campo.config(bg="#FFCCCC")  # Fondo rojo si no es válido
        label_error.config(text="Solo se permiten números.", fg="red")
    else:
        campo.config(bg="#333538")  # Fondo normal si es válido
        label_error.config(text="")  # Limpia el mensaje de error

def get_clientes():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Persona WHERE rol = 'Cliente'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_clientes = resultado[0]

        # Actualizar el texto del canvas
        client_btn.itemconfig(texto_canvas, text=f"{conteo_clientes}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        client_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_proveedor():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Persona WHERE rol = 'Proveedor'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_proveedor = resultado[0]

        # Actualizar el texto del canvas
        proveedores_btn.itemconfig(texto_canvas, text=f"{conteo_proveedor}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        proveedores_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_productos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Productos")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_productos = resultado[0]

        # Actualizar el texto del canvas
        products_btn.itemconfig(texto_canvas, text=f"{conteo_productos}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        products_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_compras():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Compra'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_compras = resultado[0]

        # Actualizar el texto del canvas
        shop_btn.itemconfig(texto_canvas, text=f"{conteo_compras}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        shop_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_ventas():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Venta'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_ventas = resultado[0]

        # Actualizar el texto del canvas
        sells_btn.itemconfig(texto_canvas, text=f"{conteo_ventas}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        sells_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_transacciones():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_transacciones = resultado[0]

        # Actualizar el texto del canvas
        transacciones_btn.itemconfig(texto_canvas, text=f" {conteo_transacciones}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        transacciones_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def get_utilidad():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_NAME)  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT SUM(CASE WHEN Accion = 'Venta' THEN Precio ELSE 0 END) - SUM(CASE WHEN Accion = 'Compra' THEN Precio ELSE 0 END) AS Utilidad FROM Transaccion")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_utilidad = resultado[0]

        # Actualizar el texto del canvas
        utility_btn.itemconfig(texto_canvas, text=f"${conteo_utilidad}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        utility_btn.itemconfig(texto_canvas, text="Error al cargar datos")

def actualizar_reloj(canvas, texto_id):
    # Obtener fecha y hora actuales
    ahora = datetime.now()
    fecha_hora = ahora.strftime("Fecha: %d/%m/%Y            Hora: %I:%M:%S %p")  # Formato día/mes/año hora:minuto:segundo am/pm
    
    # Actualizar el texto del Canvas
    canvas.itemconfig(texto_id, text=fecha_hora)
    
    # Volver a llamar esta función después de 1000 ms (1 segundo)
    canvas.after(1000, actualizar_reloj, canvas, texto_id)

def dibujar_rectangulo_redondeado(canvas, x1, y1, x2, y2, r, color):
    """Simplifica el proceso de dibujar un rectángulo redondeado."""
    canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill=color, outline=color)
    canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline=color)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=color, outline=color)
    return canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=0)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_click():
    print("¡Botón presionado!")

def on_rectangle_click1(event):
    # Verifica si el clic fue dentro del área del rectángulo
    if 0 <= event.x <= 280 and 0 <= event.y <= 100:
        on_click()

def agregar_personas(campos_compras):
    try:
        # Obtener valores desde los campos_compras
        Rut = campos_compras['rut'].get()
        Nombre = campos_compras['nombre'].get()
        Apellido = campos_compras['apellido'].get()
        Rol = campos_compras['rol'].get()

        # Insertar en la base de datos
        cursor.execute("INSERT INTO Persona (Rut_Persona, Nombre, Apellido, Rol) VALUES (?, ?, ?, ?)",
                       (Rut, Nombre, Apellido, Rol))
        conexion.commit()

        messagebox.showinfo("Éxito", "Persona agregado correctamente.")
        actualizar_contenido()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar a la persona: {e}")

def abrir_ventana_personas_proveedor():
    ventana_personas_prov = tk.Toplevel(root)
    ventana_personas_prov.title("Agregar Proveedor")
    ventana_personas_prov.geometry("400x300")
    ventana_personas_prov.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Etiqueta y campo para Cantidad

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_personas_prov)
    frame_entrada.pack(pady=10)
    frame_entrada.configure(bg="#2A2B2A")

    tk.Label(frame_entrada, text="Rut:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=0, column=0, padx=5, pady=5)
    campos_compras['rut'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['rut'].grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Nombre:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=1, column=0, padx=5, pady=5)
    campos_compras['nombre'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['nombre'].grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Apellido:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=2, column=0, padx=5, pady=5)
    campos_compras['apellido'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['apellido'].grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Rol:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=5)
    campos_compras['rol'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['rol'].insert(0, "Proveedor")  # Valor por defecto
    campos_compras['rol'].config(state=tk.DISABLED, disabledbackground="#AAAAAA", disabledforeground="#7A7A7A")
    campos_compras['rol'].grid(row=3, column=1, padx=5, pady=5)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Proveedor", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: (agregar_personas(campos_compras), ventana_personas_prov.destroy()))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas_prov, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas_prov.destroy)
    btn_cerrar.pack(pady=0)

def abrir_ventana_personas_cliente():
    ventana_personas_clie = tk.Toplevel(root)
    ventana_personas_clie.title("Agregar Cliente")
    ventana_personas_clie.geometry("400x300")
    ventana_personas_clie.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Etiqueta y campo para Cantidad

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_personas_clie)
    frame_entrada.pack(pady=10)
    frame_entrada.configure(bg="#2A2B2A")

    tk.Label(frame_entrada, text="Rut:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=0, column=0, padx=5, pady=5)
    campos_compras['rut'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['rut'].grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Nombre:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=1, column=0, padx=5, pady=5)
    campos_compras['nombre'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['nombre'].grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Apellido:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=2, column=0, padx=5, pady=5)
    campos_compras['apellido'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['apellido'].grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_entrada, text="Rol:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=5)
    campos_compras['rol'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['rol'].insert(0, "Cliente")  # Valor por defecto
    campos_compras['rol'].config(state=tk.DISABLED, disabledbackground="#AAAAAA", disabledforeground="#7A7A7A")
    campos_compras['rol'].grid(row=3, column=1, padx=5, pady=5)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Cliente", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: (agregar_personas(campos_compras), ventana_personas_clie.destroy()))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas_clie, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas_clie.destroy)
    btn_cerrar.pack(pady=0)

def agregar_transaccion_compras(campos_compras, productos_dict, proveedores_dict):
    try:
        # Obtener valores desde los campos_compras
        producto_nombre = campos_compras['producto'].get()
        cantidad = int(campos_compras['cantidad'].get())
        accion = campos_compras['accion'].get()
        precio = float(campos_compras['precio'].get())
        proveedor_nombre = campos_compras['proveedor'].get()

        # Validar selección
        if producto_nombre not in productos_dict or proveedor_nombre not in proveedores_dict:
            raise ValueError("Debe seleccionar un producto y un proveedor válidos.")

        # Obtener IDs correspondientes
        producto_id = productos_dict[producto_nombre]
        proveedor_rut = proveedores_dict[proveedor_nombre]

        # Insertar en la base de datos
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obtener stock actual del producto
        cursor.execute("SELECT Cantidad FROM Productos WHERE ID_Producto = ?", (producto_id,))
        resultado = cursor.fetchone()
        
        stock_actual = resultado[0]
        nuevo_stock = stock_actual + cantidad

        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, strftime('%d-%m-%Y', datetime('now', 'localtime')), ?, ?, ?)
        """, (proveedor_rut, producto_id, accion, cantidad, precio))

        # Actualizar el stock en la tabla Producto
        cursor.execute("UPDATE Productos SET Cantidad = ? WHERE ID_Producto = ?", (nuevo_stock, producto_id))
        
        # Guardar cambios y cerrar conexión
        conn.commit()
        conn.close()
        actualizar_contenido()
        messagebox.showinfo("Éxito", "Transacción registrada exitosamente y stock actualizado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la transacción: {e}")

def agregar_transaccion_ventas(campos_compras, productos_dict, clientes_dict):
    try:
        # Obtener valores desde los campos_compras
        producto_nombre = campos_compras['producto'].get()
        cantidad = int(campos_compras['cantidad'].get())
        accion = campos_compras['accion'].get()
        precio = float(campos_compras['precio'].get())
        cliente_nombre = campos_compras['cliente'].get()

        # Validar selección
        if producto_nombre not in productos_dict or cliente_nombre not in clientes_dict:
            raise ValueError("Debe seleccionar un producto y un cliente válidos.")

        # Obtener IDs correspondientes
        producto_id = productos_dict[producto_nombre]
        cliente_rut = clientes_dict[cliente_nombre]

        # Insertar en la base de datos
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

         # Obtener stock actual del producto
        cursor.execute("SELECT Cantidad FROM Productos WHERE ID_Producto = ?", (producto_id,))
        resultado = cursor.fetchone()
        
        stock_actual = resultado[0]

        # Verificar que haya suficiente stock para la venta
        if stock_actual < cantidad:
            raise ValueError("No hay suficiente stock para realizar la venta.")

        # Calcular nuevo stock
        nuevo_stock = stock_actual - cantidad

        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, strftime('%d-%m-%Y', datetime('now', 'localtime')), ?, ?, ?)
        """, (cliente_rut, producto_id, accion, cantidad, precio))
        
        # Actualizar stock del producto
        cursor.execute("UPDATE Productos SET Cantidad = ? WHERE ID_Producto = ?", (nuevo_stock, producto_id))

        # Guardar cambios y cerrar conexión
        conn.commit()
        conn.close()
        actualizar_contenido()
        messagebox.showinfo("Éxito", "Venta registrada y stock actualizado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la transacción: {e}")

def abrir_ventana_compras():
    ventana_compras = tk.Toplevel(root)
    ventana_compras.title("Registrar Compra")
    ventana_compras.geometry("400x450")
    ventana_compras.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Frame para las entradas
    frame_entrada = tk.Frame(ventana_compras)
    frame_entrada.pack(pady=10)
    frame_entrada.configure(bg="#2A2B2A")

    # Obtener productos y proveedores desde la base de datos
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obtener productos
        cursor.execute("SELECT ID_Producto, Nombre FROM Productos")
        productos = cursor.fetchall()
        productos_dict = {f"{nombre}": id_producto for id_producto, nombre in productos}

        # Obtener proveedores
        cursor.execute("SELECT Rut_Persona, Nombre FROM Persona WHERE Rol = 'Proveedor'")
        proveedores = cursor.fetchall()
        proveedores_dict = {f"{nombre}": rut for rut, nombre in proveedores}

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")
        return

    tk.Label(frame_entrada, text="Compra", font=('Arial', 20, "bold"), anchor="w", bg="#2A2B2A", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    canvas = tk.Canvas(frame_entrada, height=5, bg='white', bd=0, highlightthickness=0)
    canvas.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)  # Usa columnspan para que ocupe toda la fila

    # Menú desplegable para seleccionar producto
    tk.Label(frame_entrada, text="Producto:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    producto_seleccionado = tk.StringVar()
    producto_seleccionado.set("Seleccionar producto")
    campos_compras['producto'] = producto_seleccionado
    menu_productos = tk.OptionMenu(frame_entrada, producto_seleccionado, *productos_dict.keys())
    menu_productos.grid(row=2, column=1, padx=5, pady=5)

    # Cambiar el tamaño de la fuente, el color de fondo y el color de texto del OptionMenu
    menu_productos.config(font=('Arial', 12), bg='#333538', fg='white', width=18, anchor='w', highlightthickness=0)
    # Modificar el color de las opciones del menú desplegable
    menu_productos['menu'].config(font=('Arial', 12), bg='#2A2B2A', fg='white')
    menu_productos.grid(row=2, column=1, padx=5, pady=5)

    # Etiqueta y campo para Cantidad
    tk.Label(frame_entrada, text="Cantidad [KG]:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=(10,0), sticky="w")
    campos_compras['cantidad'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['cantidad'].grid(row=3, column=1, padx=5, pady=(10,0))
    
    # Etiqueta para mensajes de error (con espacio reservado)
    label_error_cantidad = tk.Label(frame_entrada, text="", font=('Arial', 10), bg="#2A2B2A", fg="red", height=1, anchor="w")
    label_error_cantidad.grid(row=4, column=1, padx=5, pady=0, sticky="w")

    # Vincular validación al campo "Cantidad"
    campos_compras['cantidad'].bind("<KeyRelease>", lambda event: validar_numero(event, campos_compras['cantidad'], label_error_cantidad))
    # Acción predefinida como "Compra" (Entry deshabilitado)
    tk.Label(frame_entrada, text="Acción:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=5, column=0, padx=5, pady=(0,10), sticky="w")
    campos_compras['accion'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), fg="#7A7A7A")
    campos_compras['accion'].insert(0, "Compra")  # Valor por defecto
    campos_compras['accion'].config(state=tk.DISABLED, disabledbackground="#AAAAAA", disabledforeground="#7A7A7A")
    campos_compras['accion'].grid(row=5, column=1, padx=5, pady=(0,10))
    
    # Etiqueta y campo para Precio
    tk.Label(frame_entrada, text="Precio [$]:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=6, column=0, padx=5, pady=(10,0), sticky="w")
    campos_compras['precio'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['precio'].grid(row=6, column=1, padx=5, pady=(10,0))
    
    # Etiqueta para mensajes de error (con espacio reservado)
    label_error_precio = tk.Label(frame_entrada, text="", font=('Arial', 10), bg="#2A2B2A", fg="red", height=1, anchor="w")
    label_error_precio.grid(row=7, column=1, padx=5, pady=0, sticky="w")

    # Vincular validación al campo "Precio"
    campos_compras['precio'].bind("<KeyRelease>", lambda event: validar_numero(event, campos_compras['precio'], label_error_precio))

    # Menú desplegable para seleccionar proveedor
    tk.Label(frame_entrada, text="Proveedor:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=8, column=0, padx=5, pady=5, sticky="w")
    proveedor_seleccionado = tk.StringVar()
    proveedor_seleccionado.set("Seleccionar proveedor")
    campos_compras['proveedor'] = proveedor_seleccionado
    menu_proveedores = tk.OptionMenu(frame_entrada, proveedor_seleccionado, *proveedores_dict.keys())
    menu_proveedores.grid(row=8, column=1, padx=5, pady=0)
    # Cambiar el tamaño de la fuente, el color de fondo y el color de texto del OptionMenu
    menu_proveedores.config(font=('Arial', 12), bg='#333538', fg='white', width=18, anchor='w', highlightthickness=0)
    # Modificar el color de las opciones del menú desplegable
    menu_proveedores['menu'].config(font=('Arial', 12), bg='#2A2B2A', fg='white')
    menu_proveedores.grid(row=8, column=1, padx=5, pady=0)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Proveedor", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: abrir_ventana_personas_proveedor())
    btn_agregar.grid(row=9, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_compras, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: (agregar_transaccion_compras(campos_compras, productos_dict, proveedores_dict), ventana_compras.destroy()))
    btn_cerrar.pack()

def abrir_ventana_ventas():
    ventana_ventas = tk.Toplevel(root)
    ventana_ventas.title("Registrar Venta")
    ventana_ventas.geometry("400x450")
    ventana_ventas.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Frame para las entradas
    frame_entrada = tk.Frame(ventana_ventas)
    frame_entrada.pack(pady=10)
    frame_entrada.configure(bg="#2A2B2A")

    # Obtener productos y clientes desde la base de datos
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obtener productos
        cursor.execute("SELECT ID_Producto, Nombre FROM Productos")
        productos = cursor.fetchall()
        productos_dict = {f"{nombre}": id_producto for id_producto, nombre in productos}

        # Obtener clientes
        cursor.execute("SELECT Rut_Persona, Nombre FROM Persona WHERE Rol = 'Cliente'")
        clientes = cursor.fetchall()
        clientes_dict = {f"{nombre}": rut for rut, nombre in clientes}

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")
        return

    tk.Label(frame_entrada, text="Ventas", font=('Arial', 20, "bold"), anchor="w", bg="#2A2B2A", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    canvas = tk.Canvas(frame_entrada, height=5, bg='white', bd=0, highlightthickness=0)
    canvas.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)  # Usa columnspan para que ocupe toda la fila

    # Menú desplegable para seleccionar producto
    tk.Label(frame_entrada, text="Producto:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    producto_seleccionado = tk.StringVar()
    producto_seleccionado.set("Seleccionar producto")
    campos_compras['producto'] = producto_seleccionado
    menu_productos = tk.OptionMenu(frame_entrada, producto_seleccionado, *productos_dict.keys())
    menu_productos.grid(row=2, column=1, padx=5, pady=5)

    # Cambiar el tamaño de la fuente, el color de fondo y el color de texto del OptionMenu
    menu_productos.config(font=('Arial', 12), bg='#333538', fg='white', width=18, anchor='w', highlightthickness=0)
    # Modificar el color de las opciones del menú desplegable
    menu_productos['menu'].config(font=('Arial', 12), bg='#2A2B2A', fg='white')
    menu_productos.grid(row=2, column=1, padx=5, pady=5)

    # Etiqueta y campo para Cantidad
    tk.Label(frame_entrada, text="Cantidad [KG]:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=(10,0), sticky="w")
    campos_compras['cantidad'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['cantidad'].grid(row=3, column=1, padx=5, pady=(10,0))
    
    # Etiqueta para mensajes de error (con espacio reservado)
    label_error_cantidad = tk.Label(frame_entrada, text="", font=('Arial', 10), bg="#2A2B2A", fg="red", height=1, anchor="w")
    label_error_cantidad.grid(row=4, column=1, padx=5, pady=0, sticky="w")

    # Vincular validación al campo "Cantidad"
    campos_compras['cantidad'].bind("<KeyRelease>", lambda event: validar_numero(event, campos_compras['cantidad'], label_error_cantidad))
    # Acción predefinida como "Compra" (Entry deshabilitado)
    tk.Label(frame_entrada, text="Acción:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=5, column=0, padx=5, pady=(0,10), sticky="w")
    campos_compras['accion'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), fg="#7A7A7A")
    campos_compras['accion'].insert(0, "Venta")  # Valor por defecto
    campos_compras['accion'].config(state=tk.DISABLED, disabledbackground="#AAAAAA", disabledforeground="#7A7A7A")
    campos_compras['accion'].grid(row=5, column=1, padx=5, pady=(0,10))
    
    # Etiqueta y campo para Precio
    tk.Label(frame_entrada, text="Precio [$]:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=6, column=0, padx=5, pady=(10,0), sticky="w")
    campos_compras['precio'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), bg="#333538", fg="white")
    campos_compras['precio'].grid(row=6, column=1, padx=5, pady=(10,0))
    
    # Etiqueta para mensajes de error (con espacio reservado)
    label_error_precio = tk.Label(frame_entrada, text="", font=('Arial', 10), bg="#2A2B2A", fg="red", height=1, anchor="w")
    label_error_precio.grid(row=7, column=1, padx=5, pady=0, sticky="w")

    # Vincular validación al campo "Precio"
    campos_compras['precio'].bind("<KeyRelease>", lambda event: validar_numero(event, campos_compras['precio'], label_error_precio))

    # Menú desplegable para seleccionar cliente
    tk.Label(frame_entrada, text="Cliente:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=8, column=0, padx=5, pady=5, sticky="w")
    cliente_seleccionado = tk.StringVar()
    cliente_seleccionado.set("Seleccionar cliente")
    campos_compras['cliente'] = cliente_seleccionado
    menu_clientes = tk.OptionMenu(frame_entrada, cliente_seleccionado, *clientes_dict.keys())
    menu_clientes.grid(row=8, column=1, padx=5, pady=0)
    # Cambiar el tamaño de la fuente, el color de fondo y el color de texto del OptionMenu
    menu_clientes.config(font=('Arial', 12), bg='#333538', fg='white', width=18, anchor='w', highlightthickness=0)
    # Modificar el color de las opciones del menú desplegable
    menu_clientes['menu'].config(font=('Arial', 12), bg='#2A2B2A', fg='white')
    menu_clientes.grid(row=8, column=1, padx=5, pady=0)

    # Botón para agregar producto
    btn_agregar = tk.Button(frame_entrada, text="Agregar Cliente", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: abrir_ventana_personas_cliente())
    btn_agregar.grid(row=9, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_ventas, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: (agregar_transaccion_ventas(campos_compras, productos_dict, clientes_dict), ventana_ventas.destroy()))
    btn_cerrar.pack()

def mostrar_productos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    conexion.close()

    # Limpiar la tabla antes de agregar los nuevos productos
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Insertar los productos
    for producto in productos:
        item = tabla.insert("", tk.END, values=producto)
        if producto[3] == "No Disponible":
            tabla.item(item, tags=("highlight",))
    
def mostrar_personas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Persona")
    personas = cursor.fetchall()
    conexion.close()

    # Limpiar la tabla antes de agregar los nuevos productos
    for fila in tabla_personas.get_children():
        tabla_personas.delete(fila)

    # Insertar los productos
    for persona in personas:
        tabla_personas.insert("", tk.END, values=persona)

def mostrar_transacciones():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Transaccion")
    transacciones = cursor.fetchall()
    conexion.close()

    # Limpiar la tabla antes de agregar los nuevos productos
    for fila in tabla_transacciones.get_children():
        tabla_transacciones.delete(fila)

    # Insertar los productos
    for transaccion in transacciones:
        tabla_transacciones.insert("", tk.END, values=transaccion)

def obtener_productos_filtrados(filtro, busqueda):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verificar el filtro y crear la consulta SQL correspondiente
    if filtro == "ID":
        cursor.execute("SELECT * FROM Productos WHERE ID_Producto LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Nombre":
        cursor.execute("SELECT * FROM Productos WHERE Nombre LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Cantidad":
        cursor.execute("SELECT * FROM Productos WHERE Cantidad LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Estado":
        cursor.execute("SELECT * FROM Productos WHERE Estado = ?", (f'{busqueda}',))
    elif filtro == "Tipo":
        cursor.execute("SELECT * FROM Productos WHERE Tipo LIKE ?", (f"%{busqueda}%",))

    # Recuperar los resultados
    productos = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    # Limpiar la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Insertar los productos filtrados
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

def cargar_registro_seleccionado(event):
    
    # Obtener el ID del producto seleccionado en la tabla
    item = tabla.selection()[0]  # Obtener la primera selección
    producto = tabla.item(item)['values']  # Obtener los valores de la fila seleccionada

    # Rellenar los campos con los valores del producto seleccionado
    input_productos_id.delete(0, tk.END)
    input_productos_id.insert(0, producto[0])  # ID_Producto

    input_productos_nombre.delete(0, tk.END)
    input_productos_nombre.insert(0, producto[1])  # Nombre

    input_productos_tipo.delete(0, tk.END)
    input_productos_tipo.insert(0, producto[4])  # Tipo

    input_productos_cantidad.delete(0, tk.END)
    input_productos_cantidad.insert(0, producto[2])  # Cantidad

    option_productos_estado.set(producto[3])  # Estado

def agregar_nuevo():
    # Verificar que todos los campos estén completos antes de agregar el producto
    id_producto = input_productos_id.get()
    nombre = input_productos_nombre.get()
    tipo = input_productos_tipo.get()
    cantidad = input_productos_cantidad.get()
    estado = option_productos_estado.get()

    if not nombre or not tipo or not cantidad or estado == "Seleccione un Estado":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío

    # Generar una nueva ID única para el producto
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(ID_Producto) FROM Productos")
    max_id = cursor.fetchone()[0] or 0  # Si no hay productos, max_id será 0
    new_id = max_id + 1
    conexion.close()

    # Insertar el nuevo registro
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Verificar si la ID ya existe en la tabla Transaccion
    cursor.execute("SELECT ID_Producto FROM Productos WHERE ID_Producto = ?", (id_producto,))
    existe = cursor.fetchone()  # Obtener el resultado de la consulta

    if existe:
        tk.messagebox.showerror("Error", "La ID del Producto ya existe. Introduzca uno diferente.")
        conexion.close()
        return  # No proceder con la inserción si la ID ya existe

    cursor.execute("INSERT INTO Productos (ID_Producto, Nombre, Cantidad, Estado, Tipo) VALUES (?, ?, ?, ?, ?)",
                   (new_id, nombre, cantidad, estado, tipo))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de agregar
    limpiar_campos()
    mostrar_productos()
    actualizar_contenido()

def actualizar_registro():
    # Obtener los datos del formulario
    id_producto = input_productos_id.get()
    nombre = input_productos_nombre.get()
    tipo = input_productos_tipo.get()
    cantidad = input_productos_cantidad.get()
    estado = option_productos_estado.get()

    # Verificar que todos los campos estén completos antes de actualizar el registro
    if not nombre or not tipo or not cantidad or estado == "Seleccione un Estado":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío

    # Actualizar el registro correspondiente en la base de datos
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Productos SET Nombre = ?, Cantidad = ?, Estado = ?, Tipo = ? WHERE ID_Producto = ?
    """, (nombre, cantidad, estado, tipo, id_producto))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de actualizar
    limpiar_campos()
    mostrar_productos()
    actualizar_contenido()

def eliminar_registro():
    # Obtener la ID del producto que se va a eliminar
    id_producto = input_productos_id.get()

    # Cambiar el estado de disponible a no disponible
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Productos SET Estado = ? WHERE ID_Producto = ?
    """, ("No Disponible", id_producto))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de eliminar
    limpiar_campos()
    mostrar_productos()
    actualizar_contenido()

def limpiar_campos():
    # Limpiar todos los campos de entrada
    input_productos_id.config(state="normal")  # Habilitar el campo ID
    input_productos_id.delete(0, tk.END)

    input_productos_nombre.delete(0, tk.END)
    input_productos_tipo.delete(0, tk.END)
    input_productos_cantidad.delete(0, tk.END)
    option_productos_estado.set("Seleccione un Estado")
    mostrar_productos()
    actualizar_contenido()

def obtener_personas_filtrados(filtro, busqueda):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verificar el filtro y crear la consulta SQL correspondiente
    if filtro == "Rut":
        cursor.execute("SELECT * FROM Persona WHERE Rut_Persona LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Nombre":
        cursor.execute("SELECT * FROM Persona WHERE Nombre LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Apellido":
        cursor.execute("SELECT * FROM Persona WHERE Apellido LIKE ?", (f"%{busqueda}%",))
    elif filtro == "Rol":
        cursor.execute("SELECT * FROM Persona WHERE Rol = ?", (f'{busqueda}',))

    # Recuperar los resultados
    personas = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    # Limpiar la tabla
    for fila in tabla_personas.get_children():
        tabla_personas.delete(fila)

    # Insertar los productos filtrados
    for persona in personas:
        tabla_personas.insert("", tk.END, values=persona)

def cargar_registro_seleccionado_persona(event):
    
    # Obtener el ID del producto seleccionado en la tabla
    item = tabla_personas.selection()[0]  # Obtener la primera selección
    personas = tabla_personas.item(item)['values']  # Obtener los valores de la fila seleccionada

    # Rellenar los campos con los valores del producto seleccionado
    input_personas_rut.delete(0, tk.END)
    input_personas_rut.insert(0, personas[0])  # Rut

    input_personas_nombre.delete(0, tk.END)
    input_personas_nombre.insert(0, personas[1])  # Nombre

    input_personas_apellido.delete(0, tk.END)
    input_personas_apellido.insert(0, personas[2])  # Apellido

    option_personas_estado.set(personas[3])  # Rol
    actualizar_contenido()

def agregar_nueva_persona():
    # Verificar que todos los campos estén completos antes de agregar el producto
    rut = input_personas_rut.get()
    nombre = input_personas_nombre.get()
    apellido = input_personas_apellido.get()
    rol = option_personas_estado.get()

    if not nombre or not rut or not apellido or rol == "Elige un Rol":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío


    # Insertar el nuevo registro
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Verificar si la ID ya existe en la tabla Persona
    cursor.execute("SELECT Rut_Persona FROM Persona WHERE Rut_Persona = ?", (rut,))
    existe = cursor.fetchone()  # Obtener el resultado de la consulta

    if existe:
        tk.messagebox.showerror("Error", "El Rut de la persona ya existe. Introduzca uno diferente.")
        conexion.close()
        return  # No proceder con la inserción si la ID ya existe

    cursor.execute("INSERT INTO Persona (Rut_Persona, Nombre, Apellido, Rol) VALUES (?, ?, ?, ?)",
                   (rut, nombre, apellido, rol))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de agregar
    limpiar_campos_persona()
    mostrar_personas()
    actualizar_contenido()

def actualizar_registro_persona():
    # Obtener los datos del formulario
    rut = input_personas_rut.get()
    nombre = input_personas_nombre.get()
    apellido = input_personas_apellido.get()
    rol = option_personas_estado.get()

    if not nombre or not rut or not apellido or rol == "Seleccione un Rol":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío

    # Actualizar el registro correspondiente en la base de datos
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Persona SET Nombre = ?, Apellido = ?, Rol = ? WHERE Rut_Persona = ?
    """, (nombre, apellido, rol, rut))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de actualizar
    limpiar_campos_persona()
    mostrar_personas()
    actualizar_contenido()

def eliminar_registro_persona():
    # Obtener la ID del producto que se va a eliminar
    rut = input_personas_rut.get()

    # Cambiar el estado de disponible a no disponible
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM Persona WHERE Persona.Rut_Persona = ? 
    """, (rut,))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de eliminar
    limpiar_campos_persona()
    mostrar_personas()
    actualizar_contenido()

def limpiar_campos_persona():
    # Limpiar todos los campos de entrada
    input_personas_rut.config(state="normal")  # Habilitar el campo ID
    input_personas_rut.delete(0, tk.END)

    input_personas_nombre.delete(0, tk.END)
    input_personas_apellido.delete(0, tk.END)
    option_personas_estado.set("Elegir un Rol")
    mostrar_personas()
    actualizar_contenido()

def obtener_transacciones_filtrados(filtro, busqueda):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verificar el filtro y crear la consulta SQL correspondiente
    if filtro == "ID":
        cursor.execute("SELECT * FROM Transaccion WHERE ID_Transaccion = ?", (f'{busqueda}',))
    elif filtro == "Rut_Persona":
        cursor.execute("SELECT * FROM Transaccion WHERE Persona_ID = ?", (f"{busqueda}",))
    elif filtro == "ID_Producto":
        cursor.execute("SELECT * FROM Transaccion WHERE Producto_ID = ?", (f"{busqueda}",))
    elif filtro == "Fecha":
        cursor.execute("SELECT * FROM Transaccion WHERE Fecha = ?", (f'{busqueda}',))
    elif filtro == "Accion":
        cursor.execute("SELECT * FROM Transaccion WHERE Accion = ?", (f'{busqueda}',))
    elif filtro == "Cantidad":
        cursor.execute("SELECT * FROM Transaccion WHERE Cantidad = ?", (f'{busqueda}',))
    elif filtro == "Precio":
        cursor.execute("SELECT * FROM Transaccion WHERE Precio = ?", (f'{busqueda}',))
    # Recuperar los resultados
    transacciones = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    # Limpiar la tabla
    for fila in tabla_transacciones.get_children():
        tabla_transacciones.delete(fila)

    # Insertar los productos filtrados
    for transaccion in transacciones:
        tabla_transacciones.insert("", tk.END, values=transaccion)

def cargar_registro_seleccionado_transaccion(event):
    # Obtener el ID del producto seleccionado en la tabla
    item = tabla_transacciones.selection()[0]  # Obtener la primera selección
    transaccion = tabla_transacciones.item(item)['values']  # Obtener los valores de la fila seleccionada

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""SELECT Persona.Nombre as Nombre, Persona.Apellido as Apellido, Productos.Nombre as NombreProducto FROM Transaccion INNER JOIN Persona ON Transaccion.Persona_ID = Persona.Rut_Persona INNER join Productos on Productos.ID_Producto = Transaccion.Producto_ID WHERE Transaccion.ID_Transaccion = ?
    """, (transaccion[0],))

    transaccion_consulta = cursor.fetchone()
    if transaccion_consulta:  # Verifica que haya resultados
        nombre_transaccion, apellido_transaccion, producto_nombre_transaccion = transaccion_consulta
    else:
        nombre_transaccion, apellido_transaccion, producto_nombre_transaccion = None, None, None

    conexion.close()

    # Rellenar los campos con los valores del producto seleccionado
    input_transacciones_id.delete(0, tk.END)
    input_transacciones_id.insert(0, transaccion[0])  # ID

    input_transacciones_id_persona.delete(0, tk.END)
    input_transacciones_id_persona.insert(0, transaccion[1])  # Rut

    input_transacciones_id_producto.delete(0, tk.END)
    input_transacciones_id_producto.insert(0, transaccion[2])  # ID Producto

    input_transacciones_fecha.delete(0, tk.END)
    input_transacciones_fecha.insert(0, transaccion[3])  # Fecha

    option_transacciones_estado.set(transaccion[4])  # Accion

    input_transacciones_cantidad.delete(0, tk.END)
    input_transacciones_cantidad.insert(0, transaccion[5])  # Cantidad

    input_transacciones_precio.delete(0, tk.END)
    input_transacciones_precio.insert(0, transaccion[6])  # Precio
    
    input_transacciones_nombre_persona.delete(0, tk.END)
    input_transacciones_nombre_persona.insert(0, nombre_transaccion)  # Nombre Persona Transaccion
    
    input_transacciones_apellido_persona.delete(0, tk.END)
    input_transacciones_apellido_persona.insert(0, apellido_transaccion)  # Apellido Persona Transaccion

    input_transacciones_nombre_producto.delete(0, tk.END)
    input_transacciones_nombre_producto.insert(0, producto_nombre_transaccion)  # Nombre Producto Transaccion
    actualizar_contenido()

def agregar_nueva_transaccion():
    # Verificar que todos los campos estén completos antes de agregar el producto
    id_transaccion = input_transacciones_id.get()
    id_persona = input_transacciones_id_persona.get()
    id_producto = input_transacciones_id_producto.get()
    fecha = input_transacciones_fecha.get()
    accion = option_transacciones_estado.get()
    cantidad = int(input_transacciones_cantidad.get())
    precio = input_transacciones_precio.get()


    if not id_transaccion or not id_persona or not id_producto or not fecha or not accion or not cantidad or precio == "Elige una Acción":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío


    # Insertar el nuevo registro
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Verificar si la ID de la transacción ya existe
    cursor.execute("SELECT ID_Transaccion FROM Transaccion WHERE ID_Transaccion = ?", (id_transaccion,))
    existe = cursor.fetchone()

    if existe:
        tk.messagebox.showerror("Error", "La ID de la transacción ya existe. Introduzca una diferente.")
        conexion.close()
        return  # No proceder con la inserción si la ID ya existe

    # Obtener el estado y stock actual del producto
    cursor.execute("SELECT Cantidad, Estado FROM Productos WHERE ID_Producto = ?", (id_producto,))
    resultado = cursor.fetchone()

    if not resultado:
        tk.messagebox.showerror("Error", "El producto no existe en la base de datos.")
        conexion.close()
        return
    
    stock_actual, estado_producto = resultado

    # Verificar si el producto está disponible antes de proceder con la venta
    if accion == "Venta":
        if estado_producto.lower() == "no disponible":
            tk.messagebox.showerror("Error", "No se puede realizar la transacción. El producto está 'No Disponible'.")
            conexion.close()
            return
        
        if stock_actual < cantidad:
            tk.messagebox.showerror("Error", "No se puede realizar la venta. El stock es insuficiente.")
            conexion.close()
            return

        if stock_actual == cantidad:
                cursor.execute("UPDATE Productos SET Estado = ? WHERE ID_Producto = ?", ("No Disponible", id_producto))

        # Actualizar stock del producto después de validar la venta
        nuevo_stock = stock_actual - cantidad
        cursor.execute("UPDATE Productos SET Cantidad = ? WHERE ID_Producto = ?", (nuevo_stock, id_producto))

    elif accion == "Compra":
        # Aumentar stock al realizar una compra
        nuevo_stock = stock_actual + cantidad
        cursor.execute("UPDATE Productos SET Cantidad = ? WHERE ID_Producto = ?", (nuevo_stock, id_producto))

    # Insertar la transacción solo si pasa las validaciones
    cursor.execute("INSERT INTO Transaccion (ID_Transaccion, Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (id_transaccion, id_persona, id_producto, fecha, accion, cantidad, precio))

    # Confirmar los cambios
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de agregar
    limpiar_campos_transacciones()
    mostrar_transacciones()
    actualizar_contenido()

def actualizar_registro_transaccion():
    # Obtener los datos del formulario
    id_transaccion = input_transacciones_id.get()
    id_persona = input_transacciones_id_persona.get()
    id_producto = input_transacciones_id_producto.get()
    fecha = input_transacciones_fecha.get()
    estado = option_transacciones_estado.get()
    cantidad = input_transacciones_cantidad.get()
    precio = input_transacciones_precio.get()

    if not id_transaccion or not id_persona or not id_producto or not fecha or not estado or not cantidad or precio == "Elige una Acción":
        tk.messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")
        return  # No proceder si algún campo está vacío

    # Actualizar el registro correspondiente en la base de datos
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Transaccion SET Persona_ID = ?, Producto_ID = ?, Fecha = ?, Accion = ?, Cantidad = ?, Precio = ? WHERE ID_Transaccion = ?
    """, (id_persona, id_producto, fecha, estado, cantidad, precio, id_transaccion))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de actualizar
    limpiar_campos_transacciones()
    mostrar_transacciones()
    actualizar_contenido()

def eliminar_registro_transaccion():
    # Obtener la ID del producto que se va a eliminar
    id_transaccion = input_transacciones_id.get()

    # Cambiar el estado de disponible a no disponible
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM Transaccion WHERE Transaccion.ID_Transaccion = ? 
    """, (id_transaccion,))
    conexion.commit()
    conexion.close()

    # Limpiar los campos después de eliminar
    limpiar_campos_transacciones()
    mostrar_transacciones()
    actualizar_contenido()

def limpiar_campos_transacciones():
    # Limpiar todos los campos de entrada
    input_transacciones_id.delete(0, tk.END)
    input_transacciones_id_persona.delete(0, tk.END)
    input_transacciones_id_producto.delete(0, tk.END)
    input_transacciones_fecha.delete(0, tk.END)
    option_transacciones_estado.set("Elegir una Acción")  # Accion
    input_transacciones_cantidad.delete(0, tk.END)
    input_transacciones_precio.delete(0, tk.END)
    input_transacciones_nombre_persona.delete(0, tk.END)
    input_transacciones_apellido_persona.delete(0, tk.END)
    input_transacciones_nombre_producto.delete(0, tk.END)

    mostrar_transacciones()
    actualizar_contenido()

def obtenerProductos_informe():
        # Obtener productos y clientes desde la base de datos
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obtener productos
        cursor.execute("SELECT ID_Producto, Nombre FROM Productos")
        productos = cursor.fetchall()
        productos_dict_informe = {f"{nombre}": id_producto for id_producto, nombre in productos}
        conn.close()

        return productos_dict_informe.keys()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")
        return

def ejecutar_consulta(*args):
    DB_NAME = "productos.db"

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    mes = opcion_mes_informe.get()
    producto = opcion_producto_informe.get()
    if mes in meses_dict:
        mes_numero = meses_dict[mes]
    else:
        return  # Salir de la función si el mes no es válido
    mes_str = f"{mes_numero:02d}"
    # Verificar si ambos valores han sido seleccionados
    if mes != "Seleccione un filtro" and producto != "Seleccione un producto":
        print(f"Ejecutando consulta para el mes: {mes_str}, producto: {producto}")
        
        query = """
        SELECT 
            SUM(CASE WHEN Accion = 'Venta' THEN Precio ELSE 0 END) AS Venta,
            SUM(CASE WHEN Accion = 'Venta' THEN Transaccion.Cantidad ELSE 0 END) AS Peso_Ventas,
            SUM(CASE WHEN Accion = 'Compra' THEN Precio ELSE 0 END) AS Compras,
            SUM(CASE WHEN Accion = 'Compra' THEN Transaccion.Cantidad ELSE 0 END) AS Peso_Compras,
            Productos.Cantidad
        FROM Transaccion 
        INNER JOIN Productos ON Transaccion.Producto_ID = Productos.ID_Producto
        WHERE 
            (substr(Transaccion.Fecha, 4, 2) = ?)
            AND (Productos.Nombre = ?)
        GROUP BY Productos.ID_Producto;
        """

        # Actualizar el texto del canvas
        #client_btn.itemconfig(texto_canvas, text=f"{conteo_clientes}")

        # Ejecutar la consulta con los parámetros
        cursor.execute(query, (mes_str, producto))
        resultado = cursor.fetchone()
        
        Precio_Ventas = resultado[0]
        Peso_Ventas = resultado[1]
        Precio_Compras = resultado[2]
        Peso_Compras = resultado[3]
        Stock = resultado[4]

        # Cerrar conexión
        cursor.close()
        conexion.close()



# Canvas 1: Barra superior
canvas1 = tk.Canvas(root, width=1340, height=70, highlightthickness=0, bg="#292B2B")
canvas1.place(x=0, y=0)
canvas1.create_rectangle(0, 0, 1340, 70, fill="#292B2B", outline="#292B2B")
# Agregar texto dentro del rectángulo
texto = canvas1.create_text(80, 35, text="Inventario", fill="white", font=("Arial", 16, "bold"))
client_imgA = Image.open("Img/Img-8.png")  # Cambia la ruta por la de tu imagen
client_photoA = ImageTk.PhotoImage(client_imgA)
canvas1.create_image(170, 35, image=client_photoA)
canvas1.image = client_photoA

# Canvas 2: Panel lateral izquierdo
canvas2 = tk.Canvas(root, width=300, height=560, highlightthickness=0, bg="#292B2B")
canvas2.place(x=0, y=70)  # Colocado justo debajo del canvas1
canvas2.create_rectangle(0, 0, 300, 560, fill="#292B2B", outline="#292B2B")

canvas21 = tk.Canvas(clientes_page, width=300, height=560, highlightthickness=0, bg="#292B2B")
canvas21.place(x=0, y=70)  # Colocado justo debajo del canvas1
canvas21.create_rectangle(0, 0, 300, 560, fill="#292B2B", outline="#292B2B")


# Cargar la imagen
dashboard_img_original = Image.open("Img/Dash-Active.png")  # Cambia la ruta por la de tu imagen
dashboard_img = ImageTk.PhotoImage(dashboard_img_original)
# Agregar la imagen al Canvas con un tag
dashboard_image_item = canvas2.create_image(20, 220, image=dashboard_img, anchor="nw", tags=("dashboard_img","dashboard_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_dashboard = canvas2.create_text(70, 240, text="Dashboard", anchor="w", fill="#1F68A3", font=("Arial", 18, "bold"), tags=("dashboard_text","dashboard_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("dashboard_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("dashboard_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("dashboard_clickable", "<Button-1>", lambda e: mostrar_pestaña("dashboard"))

# Cargar la imagen
people_img_original = Image.open("Img/People-Default.png")  # Cambia la ruta por la de tu imagen
people_img = ImageTk.PhotoImage(people_img_original)
# Agregar la imagen al Canvas con un tag
people_image_item = canvas2.create_image(20, 270, image=people_img, anchor="nw", tags=("personas_img","personas_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_people = canvas2.create_text(70, 290, text="Personas", anchor="w", fill="white", font=("Arial", 18, "bold"), tags=("personas_text","personas_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("personas_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("personas_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("personas_clickable", "<Button-1>", lambda e: mostrar_pestaña("personas"))

# Cargar la imagen
products_img_original = Image.open("Img/Products-Default.png")  # Cambia la ruta por la de tu imagen
products_imgs = ImageTk.PhotoImage(products_img_original)
# Agregar la imagen al Canvas con un tag
products_image_item = canvas2.create_image(20, 320, image=products_imgs, anchor="nw", tags=("productos_img","productos_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_products = canvas2.create_text(70, 340, text="Productos", anchor="w", fill="white", font=("Arial", 18, "bold"), tags=("productos_text","productos_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("productos_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("productos_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("productos_clickable", "<Button-1>", lambda e: mostrar_pestaña("productos"))

# Cargar la imagen
transac_img_original = Image.open("Img/Transac-Default.png")  # Cambia la ruta por la de tu imagen
transac_imgs = ImageTk.PhotoImage(transac_img_original)
# Agregar la imagen al Canvas con un tag
transac_image_item = canvas2.create_image(20, 370, image=transac_imgs, anchor="nw", tags=("transac_img","transacc_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_transac = canvas2.create_text(70, 390, text="Transacciones", anchor="w", fill="white", font=("Arial", 18, "bold"), tags=("transac_text","transacc_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("transacc_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("transacc_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("transacc_clickable", "<Button-1>", lambda e: mostrar_pestaña("transacciones"))

# Cargar la imagen
report_img_original = Image.open("Img/Report-Default.png")  # Cambia la ruta por la de tu imagen
report_imgs = ImageTk.PhotoImage(report_img_original)
# Agregar la imagen al Canvas con un tag
report_image_item = canvas2.create_image(20, 420, image=report_imgs, anchor="nw", tags=("report_img","report_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_report = canvas2.create_text(70, 440, text="Reportes", anchor="w", fill="white", font=("Arial", 18, "bold"), tags=("report_text","report_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("report_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("report_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("report_clickable", "<Button-1>", lambda e: mostrar_pestaña("reportes"))

# Cargar la imagen
config_img_original = Image.open("Img/Config-Default.png")  # Cambia la ruta por la de tu imagen
config_imgs = ImageTk.PhotoImage(config_img_original)
# Agregar la imagen al Canvas con un tag
config_image_item = canvas2.create_image(20, 470, image=config_imgs, anchor="nw", tags=("config_img","config_clickable"))
# Agregar el texto al Canvas con el mismo tag
texto_canvas_config = canvas2.create_text(70, 490, text="Configuración", anchor="w", fill="white", font=("Arial", 18, "bold"), tags=("config_text","config_clickable"))
# Establecer cursor tipo "manito" al pasar sobre los elementos con el tag
canvas2.tag_bind("config_clickable", "<Enter>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("config_clickable", "<Leave>", lambda e: canvas2.config(cursor="hand2"))
canvas2.tag_bind("config_clickable", "<Button-1>", lambda e: mostrar_pestaña("configuracion"))


proveedores_imgA = Image.open("Img/Img-9.png")  # Cambia la ruta por la de tu imagen
proveedores_photoA = ImageTk.PhotoImage(proveedores_imgA)
canva2_logo = canvas2.create_image(150, 80, image=proveedores_photoA)
canvas2.image = proveedores_photoA
canvas2.create_text(70, 180, text="Menú", fill="white", font=("Helvetica", 30, "bold"))
canvas2.create_rectangle(20, 200, 275, 203, fill="#FFFFFF", outline="#FFFFFF")
# Canvas 3: Contenido principal
canvas3 = tk.Canvas(root, width=1000, height=35, highlightthickness=0, bg="#292B2B")
canvas3.place(x=312, y=17)  # Coordenadas específicas dentro de la main_page
dibujar_rectangulo_redondeado(canvas3, 0, 0, 1000, 35, r=10, color="#3A3939")

canvas2.tag_bind(canva2_logo, "<Button-1>", lambda e: mostrar_pestaña("dashboard"))

# Texto inicial en el centro del Canvas
texto_id = canvas3.create_text(500, 17.5, text="", fill="white", font=("Helvetica", 16, "bold"))

# Canvas 4: Botoneras
client_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
client_btn.place(x=360, y=170)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(client_btn, 0, 0, 280, 100, r=20, color="#8B51F5")
client_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#6334E3")
client_btn1.place(x=360, y=170)  # Colocado justo debajo del canvas1
client_btn1.create_rectangle(0, 0, 100, 100, fill="#6334E3", outline="#6334E3")

# Agregar texto dentro del rectángulo

texto_canvas = client_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = client_btn.create_text(108, 30, text="Clientes", fill="white", font=("Arial", 18, "bold"), anchor="w")

client_img = Image.open("Img/Img-1.png")  # Cambia la ruta por la de tu imagen
client_photo = ImageTk.PhotoImage(client_img)
client_btn1.create_image(50, 50, image=client_photo)
client_btn1.image = client_photo

# Canvas 5: Botoneras
proveedores_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
proveedores_btn.place(x=680, y=170)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(proveedores_btn, 0, 0, 280, 100, r=20, color="#C0C0C0")
proveedores_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#AAAAAA")
proveedores_btn1.place(x=680, y=170)  # Colocado justo debajo del canvas1
proveedores_btn1.create_rectangle(0, 0, 100, 100, fill="#AAAAAA", outline="#AAAAAA")

# Agregar texto dentro del rectángulo
texto_canvas = proveedores_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = proveedores_btn.create_text(108, 30, text="Proveedores", fill="white", font=("Arial", 18, "bold"), anchor="w")

proveedores_img = Image.open("Img/Img-2.png")  # Cambia la ruta por la de tu imagen
proveedores_photo = ImageTk.PhotoImage(proveedores_img)
proveedores_btn1.create_image(50, 50, image=proveedores_photo)
proveedores_btn1.image = proveedores_photo

# Canvas 6: Botoneras
products_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
products_btn.place(x=1000, y=170)  # Colocado justo debajo del canvas1
products_rectangulo = dibujar_rectangulo_redondeado(products_btn, 0, 0, 280, 100, r=20, color="#F06E9C")
products_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#E93578")
products_btn1.place(x=1000, y=170)  # Colocado justo debajo del canvas1
products_rectangulo1 = products_btn1.create_rectangle(0, 0, 100, 100, fill="#E93578", outline="#E93578")

# Agregar texto dentro del rectángulo
texto_canvas = products_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = products_btn.create_text(108, 30, text="Productos", fill="white", font=("Arial", 18, "bold"), anchor="w")

products_img = Image.open("Img/Img-3.png")  # Cambia la ruta por la de tu imagen
products_photo = ImageTk.PhotoImage(products_img)
products_img1 = products_btn1.create_image(50, 50, image=products_photo)
products_btn1.image = products_photo

products_btn.config(cursor="hand2")  # Cursor estilo "manito"
products_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
products_btn.tag_bind(products_rectangulo, "<Button-1>", lambda e: mostrar_pestaña("productos"))
products_btn1.tag_bind(products_rectangulo1, "<Button-1>", lambda e: mostrar_pestaña("productos"))
products_btn1.tag_bind(products_img1, "<Button-1>", lambda e: mostrar_pestaña("productos"))
products_btn.tag_bind(texto_canvas, "<Button-1>", lambda e: mostrar_pestaña("productos"))
products_btn.tag_bind(titulo_canvas, "<Button-1>", lambda e: mostrar_pestaña("productos"))

# Canvas 7: Botoneras
utility_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
utility_btn.place(x=360, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(utility_btn, 0, 0, 280, 100, r=20, color="#3D8AF7")
utility_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#3D8AF7")
utility_btn1.place(x=360, y=300)  # Colocado justo debajo del canvas1
utility_btn1.create_rectangle(0, 0, 100, 100, fill="#1464F6", outline="#1464F6")

# Agregar texto dentro del rectángulo
texto_canvas = utility_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = utility_btn.create_text(108, 30, text="Utilidad", fill="white", font=("Arial", 18, "bold"), anchor="w")

utility_img = Image.open("Img/Img-4.png")  # Cambia la ruta por la de tu imagen
utility_photo = ImageTk.PhotoImage(utility_img)
utility_btn1.create_image(50, 50, image=utility_photo)
utility_btn1.image = utility_photo


# Canvas 8: Botoneras
shop_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
shop_btn.place(x=680, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(shop_btn, 0, 0, 280, 100, r=20, color="#92D36E")
shop_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#72BB53")
shop_btn1.place(x=680, y=300)  # Colocado justo debajo del canvas1
shop_btn1.create_rectangle(0, 0, 100, 100, fill="#72BB53", outline="#72BB53")

# Agregar texto dentro del rectángulo
texto_canvas = shop_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = shop_btn.create_text(108, 30, text="Compras", fill="white", font=("Arial", 18, "bold"), anchor="w")

shop_img = Image.open("Img/Img-5.png")  # Cambia la ruta por la de tu imagen
shop_photo = ImageTk.PhotoImage(shop_img)
shop_btn1.create_image(50, 50, image=shop_photo)
shop_btn1.image = shop_photo

# Canvas 9: Botoneras
sells_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
sells_btn.place(x=1000, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(sells_btn, 0, 0, 280, 100, r=20, color="#FF5D55")
sells_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#FF3823")
sells_btn1.place(x=1000, y=300)  # Colocado justo debajo del canvas1
sells_btn1.create_rectangle(0, 0, 100, 100, fill="#FF3823", outline="#FF3823")

# Agregar texto dentro del rectángulo
texto_canvas = sells_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = sells_btn.create_text(108, 30, text="Ventas", fill="white", font=("Arial", 18, "bold"), anchor="w")

sells_img = Image.open("Img/Img-6.png")  # Cambia la ruta por la de tu imagen
sells_photo = ImageTk.PhotoImage(sells_img)
sells_btn1.create_image(50, 50, image=sells_photo)
sells_btn1.image = sells_photo


# Canvas 10: Botoneras
transacciones_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
transacciones_btn.place(x=360, y=430)  # Colocado justo debajo del canvas1
transacciones_rectangulo = dibujar_rectangulo_redondeado(transacciones_btn, 0, 0, 280, 100, r=20, color="#4DD7FA")
transacciones_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#00C8F8")
transacciones_btn1.place(x=360, y=430)  # Colocado justo debajo del canvas1
transacciones_rectangulo1 = transacciones_btn1.create_rectangle(0, 0, 100, 100, fill="#00C8F8", outline="#00C8F8")

# Agregar texto dentro del rectángulo
texto_canvas = transacciones_btn.create_text(108, 55, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"), anchor="w")
titulo_canvas = transacciones_btn.create_text(108, 30, text="Transacciones", fill="white", font=("Arial", 18, "bold"), anchor="w")

transacciones_img = Image.open("Img/Img-7.png")  # Cambia la ruta por la de tu imagen
transacciones_photo = ImageTk.PhotoImage(transacciones_img)
transacciones_img1 = transacciones_btn1.create_image(50, 50, image=transacciones_photo)
transacciones_btn1.image = transacciones_photo

transacciones_btn.config(cursor="hand2")  # Cursor estilo "manito"
transacciones_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
transacciones_btn.tag_bind(transacciones_rectangulo, "<Button-1>", lambda e: mostrar_pestaña("transacciones"))
transacciones_btn1.tag_bind(transacciones_rectangulo1, "<Button-1>", lambda e: mostrar_pestaña("transacciones"))
transacciones_btn1.tag_bind(transacciones_img1, "<Button-1>", lambda e: mostrar_pestaña("transacciones"))
transacciones_btn.tag_bind(texto_canvas, "<Button-1>", lambda e: mostrar_pestaña("transacciones"))
transacciones_btn.tag_bind(titulo_canvas, "<Button-1>", lambda e: mostrar_pestaña("transacciones"))

# Canvas 11: Botoneras
reg_shop_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
reg_shop_btn.place(x=680, y=430)  # Colocado justo debajo del canvas1
reg_shop_rectangulo = dibujar_rectangulo_redondeado(reg_shop_btn, 0, 0, 280, 100, r=20, color="#FFD783")
reg_shop_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#FFC957")
reg_shop_btn1.place(x=680, y=430)  # Colocado justo debajo del canvas1
reg_shop_rectangulo1 = reg_shop_btn1.create_rectangle(0, 0, 100, 100, fill="#FFC957", outline="#FFC957")

# Agregar texto dentro del rectángulo
texto1_reg_shop = reg_shop_btn.create_text(108, 30, text="Registrar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto2_reg_shop = reg_shop_btn.create_text(108, 55, text="Compra", fill="white", font=("Arial", 18, "bold"), anchor="w")

reg_shop_img = Image.open("Img/Img-5.png")  # Cambia la ruta por la de tu imagen
reg_shop_photo = ImageTk.PhotoImage(reg_shop_img)
reg_shop_img1 = reg_shop_btn1.create_image(50, 50, image=reg_shop_photo)
reg_shop_btn1.image = reg_shop_photo

reg_shop_btn.config(cursor="hand2")  # Cursor estilo "manito"
reg_shop_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
reg_shop_btn.tag_bind(reg_shop_rectangulo, "<Button-1>", lambda e: abrir_ventana_compras())
reg_shop_btn1.tag_bind(reg_shop_rectangulo1, "<Button-1>", lambda e: abrir_ventana_compras())
reg_shop_btn1.tag_bind(reg_shop_img1, "<Button-1>", lambda e: abrir_ventana_compras())
reg_shop_btn.tag_bind(texto1_reg_shop, "<Button-1>", lambda e: abrir_ventana_compras())
reg_shop_btn.tag_bind(texto2_reg_shop, "<Button-1>", lambda e: abrir_ventana_compras())

# Canvas 12: Botoneras
reg_sell_btn = tk.Canvas(main_page, width=280, height=100, highlightthickness=0, bg="#232323")
reg_sell_btn.place(x=1000, y=430)  # Colocado justo debajo del canvas1
reg_sell_rectangulo = dibujar_rectangulo_redondeado(reg_sell_btn, 0, 0, 280, 100, r=20, color="#FFA382")
reg_sell_btn1 = tk.Canvas(main_page, width=100, height=100, highlightthickness=0, bg="#FF8351")
reg_sell_btn1.place(x=1000, y=430)  # Colocado justo debajo del canvas1
reg_sell_rectangulo1 = reg_sell_btn1.create_rectangle(0, 0, 100, 100, fill="#FF8351", outline="#FF8351")

# Agregar texto dentro del rectángulo
texto1_reg_sell = reg_sell_btn.create_text(108, 30, text="Registrar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto2_reg_sell = reg_sell_btn.create_text(108, 55, text="Venta", fill="white", font=("Arial", 18, "bold"), anchor="w")

reg_sell_img = Image.open("Img/Img-6.png")  # Cambia la ruta por la de tu imagen
reg_sell_photo = ImageTk.PhotoImage(reg_sell_img)
reg_sell_img1 = reg_sell_btn1.create_image(50, 50, image=reg_sell_photo)
reg_sell_btn1.image = reg_sell_photo

reg_sell_btn.config(cursor="hand2")  # Cursor estilo "manito"
reg_sell_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
reg_sell_btn.tag_bind(reg_sell_rectangulo, "<Button-1>", lambda e: abrir_ventana_ventas())
reg_sell_btn1.tag_bind(reg_sell_rectangulo1, "<Button-1>", lambda e: abrir_ventana_ventas())
reg_sell_btn1.tag_bind(reg_sell_img1, "<Button-1>", lambda e: abrir_ventana_ventas())
reg_sell_btn.tag_bind(texto1_reg_sell, "<Button-1>", lambda e: abrir_ventana_ventas())
reg_sell_btn.tag_bind(texto2_reg_sell, "<Button-1>", lambda e: abrir_ventana_ventas())



# PÁGINA DE CONFIGURACIÓN

# Canvas 1: Botoneras
securitycopy_btn = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
securitycopy_btn.place(x=352, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo = dibujar_rectangulo_redondeado(securitycopy_btn, 0, 0, 280, 100, r=20, color="#3D8AF7")
securitycopy_btn1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#1464F6")
securitycopy_btn1.place(x=352, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo1 = securitycopy_btn1.create_rectangle(0, 0, 100, 100, fill="#1464F6", outline="#1464F6")

# Agregar texto dentro del rectángulo
titulo_canvas_securitycopy = securitycopy_btn.create_text(108, 30, text="Copia", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_securitycopy = securitycopy_btn.create_text(108, 55, text="De Seguridad", fill="white", font=("Arial", 16), anchor="w")

securitycopy_img = Image.open("Img/Img-10.png")  # Cambia la ruta por la de tu imagen
securitycopy_photo = ImageTk.PhotoImage(securitycopy_img)
securitycopy_img1 = securitycopy_btn1.create_image(50, 50, image=securitycopy_photo)
securitycopy_btn1.image = securitycopy_photo

securitycopy_btn.config(cursor="hand2")  # Cursor estilo "manito"
securitycopy_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
securitycopy_btn.tag_bind(securitycopy_rectangulo, "<Button-1>", lambda e: hacer_copia_seguridad())
securitycopy_btn1.tag_bind(securitycopy_rectangulo1, "<Button-1>", lambda e: hacer_copia_seguridad())
securitycopy_btn1.tag_bind(securitycopy_img1, "<Button-1>", lambda e: hacer_copia_seguridad())
securitycopy_btn.tag_bind(texto_canvas_securitycopy, "<Button-1>", lambda e: hacer_copia_seguridad())
securitycopy_btn.tag_bind(titulo_canvas_securitycopy, "<Button-1>", lambda e: hacer_copia_seguridad())

# Canvas 2: Botoneras
resetsecuritycopy_btn = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
resetsecuritycopy_btn.place(x=352, y=365)  # Colocado justo debajo del canvas1
resetsecuritycopy_rectangulo = dibujar_rectangulo_redondeado(resetsecuritycopy_btn, 0, 0, 280, 100, r=20, color="#3D8AF7")
resetsecuritycopy_btn1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#1464F6")
resetsecuritycopy_btn1.place(x=352, y=365)  # Colocado justo debajo del canvas1
resetsecuritycopy_rectangulo1 = resetsecuritycopy_btn1.create_rectangle(0, 0, 100, 100, fill="#1464F6", outline="#1464F6")

# Agregar texto dentro del rectángulo
titulo_canvas_resetsecuritycopy = resetsecuritycopy_btn.create_text(108, 30, text="Restaurar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_resetsecuritycopy = resetsecuritycopy_btn.create_text(108, 52, text="Copia de", fill="white", font=("Arial", 16), anchor="w")
texto_canvas2_resetsecuritycopy = resetsecuritycopy_btn.create_text(108, 72, text="Seguridad", fill="white", font=("Arial", 16), anchor="w")

resetsecuritycopy_img = Image.open("Img/Img-11.png")  # Cambia la ruta por la de tu imagen
resetsecuritycopy_photo = ImageTk.PhotoImage(resetsecuritycopy_img)
resetsecuritycopy_img1 = resetsecuritycopy_btn1.create_image(50, 50, image=resetsecuritycopy_photo)
resetsecuritycopy_btn1.image = resetsecuritycopy_photo

resetsecuritycopy_btn.config(cursor="hand2")  # Cursor estilo "manito"
resetsecuritycopy_btn1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
resetsecuritycopy_btn.tag_bind(resetsecuritycopy_rectangulo, "<Button-1>", lambda e: restaurar_copia_seguridad())
resetsecuritycopy_btn1.tag_bind(resetsecuritycopy_rectangulo1, "<Button-1>", lambda e: restaurar_copia_seguridad())
resetsecuritycopy_btn1.tag_bind(resetsecuritycopy_img1, "<Button-1>", lambda e: restaurar_copia_seguridad())
resetsecuritycopy_btn.tag_bind(texto_canvas_resetsecuritycopy, "<Button-1>", lambda e: restaurar_copia_seguridad())
resetsecuritycopy_btn.tag_bind(texto_canvas2_resetsecuritycopy, "<Button-1>", lambda e: restaurar_copia_seguridad())
resetsecuritycopy_btn.tag_bind(titulo_canvas_resetsecuritycopy, "<Button-1>", lambda e: restaurar_copia_seguridad())

# Canvas 3: Botoneras
resetbd = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
resetbd.place(x=672, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo = dibujar_rectangulo_redondeado(resetbd, 0, 0, 280, 100, r=20, color="#FFC581")
resetbd1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#FFB253")
resetbd1.place(x=672, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo1 = resetbd1.create_rectangle(0, 0, 100, 100, fill="#FFB253", outline="#FFB253")

# Agregar texto dentro del rectángulo
titulo_canvas_resetbd = resetbd.create_text(108, 30, text="Resetear", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_resetbd = resetbd.create_text(108, 55, text="Base de Datos", fill="white", font=("Arial", 16), anchor="w")

securitycopy_img = Image.open("Img/Img-12.png")  # Cambia la ruta por la de tu imagen
securitycopy_photo = ImageTk.PhotoImage(securitycopy_img)
securitycopy_img1 = resetbd1.create_image(50, 50, image=securitycopy_photo)
resetbd1.image = securitycopy_photo

resetbd.config(cursor="hand2")  # Cursor estilo "manito"
resetbd1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
resetbd.tag_bind(securitycopy_rectangulo, "<Button-1>", lambda e: limpiar_base_datos())
resetbd1.tag_bind(securitycopy_rectangulo1, "<Button-1>", lambda e: limpiar_base_datos())
resetbd1.tag_bind(securitycopy_img1, "<Button-1>", lambda e: limpiar_base_datos())
resetbd.tag_bind(texto_canvas_resetbd, "<Button-1>", lambda e: limpiar_base_datos())
resetbd.tag_bind(titulo_canvas_resetbd, "<Button-1>", lambda e: limpiar_base_datos())

# Canvas 4: Botoneras
generarrepportes = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
generarrepportes.place(x=672, y=365)  # Colocado justo debajo del canvas1
securitycopy_rectangulo = dibujar_rectangulo_redondeado(generarrepportes, 0, 0, 280, 100, r=20, color="#C0C0C0")
generarrepportes1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#AAAAAA")
generarrepportes1.place(x=672, y=365)  # Colocado justo debajo del canvas1
securitycopy_rectangulo1 = generarrepportes1.create_rectangle(0, 0, 100, 100, fill="#AAAAAA", outline="#AAAAAA")

# Agregar texto dentro del rectángulo
titulo_canvas_generarrepportes = generarrepportes.create_text(108, 30, text="Generar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_generarrepportes = generarrepportes.create_text(108, 55, text="Reportes", fill="white", font=("Arial", 16), anchor="w")

securitycopy_img = Image.open("Img/Img-13.png")  # Cambia la ruta por la de tu imagen
securitycopy_photo = ImageTk.PhotoImage(securitycopy_img)
securitycopy_img1 = generarrepportes1.create_image(50, 50, image=securitycopy_photo)
generarrepportes1.image = securitycopy_photo

generarrepportes.config(cursor="hand2")  # Cursor estilo "manito"
generarrepportes1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
generarrepportes.tag_bind(securitycopy_rectangulo, "<Button-1>", lambda e: on_click())
generarrepportes1.tag_bind(securitycopy_rectangulo1, "<Button-1>", lambda e: on_click())
generarrepportes1.tag_bind(securitycopy_img1, "<Button-1>", lambda e: on_click())
generarrepportes.tag_bind(texto_canvas_generarrepportes, "<Button-1>", lambda e: on_click())
generarrepportes.tag_bind(titulo_canvas_generarrepportes, "<Button-1>", lambda e: on_click())

# Canvas 5: Botoneras
exportbd = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
exportbd.place(x=992, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo = dibujar_rectangulo_redondeado(exportbd, 0, 0, 280, 100, r=20, color="#FF8A84")
exportbd1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#FF5D55")
exportbd1.place(x=992, y=234)  # Colocado justo debajo del canvas1
securitycopy_rectangulo1 = exportbd1.create_rectangle(0, 0, 100, 100, fill="#FF5D55", outline="#FF5D55")

# Agregar texto dentro del rectángulo
titulo_canvas_exportbd = exportbd.create_text(108, 30, text="Exportar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_exportbd = exportbd.create_text(108, 55, text="Base de Datos", fill="white", font=("Arial", 16), anchor="w")

securitycopy_img = Image.open("Img/Img-14.png")  # Cambia la ruta por la de tu imagen
securitycopy_photo = ImageTk.PhotoImage(securitycopy_img)
securitycopy_img1 = exportbd1.create_image(50, 50, image=securitycopy_photo)
exportbd1.image = securitycopy_photo

exportbd.config(cursor="hand2")  # Cursor estilo "manito"
exportbd1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
exportbd.tag_bind(securitycopy_rectangulo, "<Button-1>", lambda e: exportar_bd_excel())
exportbd1.tag_bind(securitycopy_rectangulo1, "<Button-1>", lambda e: exportar_bd_excel())
exportbd1.tag_bind(securitycopy_img1, "<Button-1>", lambda e: exportar_bd_excel())
exportbd.tag_bind(texto_canvas_exportbd, "<Button-1>", lambda e: exportar_bd_excel())
exportbd.tag_bind(titulo_canvas_exportbd, "<Button-1>", lambda e: exportar_bd_excel())

# Canvas 6: Botoneras
importbd = tk.Canvas(config_page, width=280, height=100, highlightthickness=0, bg="#232323")
importbd.place(x=992, y=365)  # Colocado justo debajo del canvas1
securitycopy_rectangulo = dibujar_rectangulo_redondeado(importbd, 0, 0, 280, 100, r=20, color="#AEDD94")
importbd1 = tk.Canvas(config_page, width=100, height=100, highlightthickness=0, bg="#92D36E")
importbd1.place(x=992, y=365)  # Colocado justo debajo del canvas1
securitycopy_rectangulo1 = importbd1.create_rectangle(0, 0, 100, 100, fill="#92D36E", outline="#92D36E")

# Agregar texto dentro del rectángulo
titulo_canvas_importbd = importbd.create_text(108, 30, text="Importar", fill="white", font=("Arial", 18, "bold"), anchor="w")
texto_canvas_importbd = importbd.create_text(108, 55, text="Base de Datos", fill="white", font=("Arial", 16), anchor="w")

securitycopy_img = Image.open("Img/Img-15.png")  # Cambia la ruta por la de tu imagen
securitycopy_photo = ImageTk.PhotoImage(securitycopy_img)
securitycopy_img1 = importbd1.create_image(50, 50, image=securitycopy_photo)
importbd1.image = securitycopy_photo

importbd.config(cursor="hand2")  # Cursor estilo "manito"
importbd1.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el client_btn con la función del rectángulo
importbd.tag_bind(securitycopy_rectangulo, "<Button-1>", lambda e: importar_bd_excel())
importbd1.tag_bind(securitycopy_rectangulo1, "<Button-1>", lambda e: importar_bd_excel())
importbd1.tag_bind(securitycopy_img1, "<Button-1>", lambda e: importar_bd_excel())
importbd.tag_bind(texto_canvas_importbd, "<Button-1>", lambda e: importar_bd_excel())
importbd.tag_bind(titulo_canvas_importbd, "<Button-1>", lambda e: importar_bd_excel())

#Contenedor de los detalles del producto
pp_dta = tk.Canvas(productos_page, width=380, height=470, highlightthickness=0, bg="#232323")
pp_dta.place(x=325, y=110)
dibujar_rectangulo_redondeado(pp_dta, 0, 0, 380, 470, r=10, color="#2A2B2A")

pp_dta_2 = tk.Canvas(productos_page, width=300, height=36, highlightthickness=0, bg="#2A2B2A")
pp_dta_2.place(x=365, y=95)
pp_dta_info = dibujar_rectangulo_redondeado(pp_dta_2, 0, 0, 300, 36, r=10, color="#393A3A")
pp_dta_2.create_text(150, 18, text="Detalles de Productos", fill="white", font=("Arial", 16), anchor="center")

#Filtros de búsqueda, Página productos
reg_filter = tk.Canvas(productos_page, width=600, height=65, highlightthickness=0, bg="#232323")
reg_filter.place(x=720, y=110)
dibujar_rectangulo_redondeado(reg_filter, 0, 0, 600, 65, r=10, color="#2A2B2A")

opcion_filtro_busqueda = tk.StringVar()
opcion_filtro_busqueda.set("Seleccione un filtro") # Texto inicial filtro

opciones_filtro_busqueda_opciones = ["ID", "Nombre", "Cantidad", "Estado", "Tipo"]

menu_filtros_busqueda = tk.OptionMenu(productos_page, opcion_filtro_busqueda, *opciones_filtro_busqueda_opciones)
menu_filtros_busqueda.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_filtros_busqueda.place(x=732, y=128, width=172, height=30)

# Etiqueta y campo para Cantidad
input_busqueda = tk.Entry(productos_page, width=22, font=('Arial', 12), bg="#333538", fg="white")
input_busqueda.place(x=916, y=128, width=160, height=30)

btn_buscar_filtro = tk.Button(productos_page, text="Buscar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: obtener_productos_filtrados(opcion_filtro_busqueda.get(),input_busqueda.get()))
btn_buscar_filtro.place(x=1088, y=128, width=82, height=30)

btn_mostrar_todo_filtro = tk.Button(productos_page, text="Mostrar Todo", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: mostrar_productos())
btn_mostrar_todo_filtro.place(x=1182, y=128, width=126, height=30)


pp_dta.create_text(90, 95, text="ID", fill="white", font=("Arial", 12), anchor="e")
pp_dta.create_text(90, 140, text="Nombre", fill="white", font=("Arial", 12), anchor="e")
pp_dta.create_text(90, 185, text="Cantidad", fill="white", font=("Arial", 12), anchor="e")
pp_dta.create_text(90, 230, text="Estado", fill="white", font=("Arial", 12), anchor="e")
pp_dta.create_text(90, 275, text="Tipo", fill="white", font=("Arial", 12), anchor="e")

input_productos_id = tk.Entry(productos_page, width=22, font=('Arial', 12), bg="#333538", fg="white")
input_productos_id.place(x=424, y=191, width=254, height=26)

input_productos_nombre = tk.Entry(productos_page, width=22, font=('Arial', 12), bg="#333538", fg="white")
input_productos_nombre.place(x=424, y=236, width=254, height=26)

input_productos_cantidad = tk.Entry(productos_page, width=22, font=('Arial', 12), bg="#333538", fg="white")
input_productos_cantidad.place(x=424, y=280, width=254, height=26)

option_productos_estado = tk.StringVar()
option_productos_estado.set("Seleccione un Estado") # Texto inicial filtro
option_productos_estado_opciones = ["Disponible", "No Disponible"]
option_productos_estado_menu = tk.OptionMenu(productos_page, option_productos_estado, *option_productos_estado_opciones)
option_productos_estado_menu.config(font=("Arial", 12), bg="#333538", fg="white", highlightthickness=0)
option_productos_estado_menu.place(x=424, y=326, width=254, height=26)

input_productos_tipo = tk.Entry(productos_page, width=22, font=('Arial', 12), bg="#333538", fg="white")
input_productos_tipo.place(x=424, y=376, width=254, height=26)

btn_nuevo_producto = tk.Button(productos_page, text="Nuevo", font=('Arial', 12), bg="#1F68A3", fg="white", command=agregar_nuevo)
btn_nuevo_producto.place(x=353, y=480, width=150, height=30)
btn_actualizar_producto = tk.Button(productos_page, text="Actualizar", font=('Arial', 12), bg="#1F68A3", fg="white", command=actualizar_registro)
btn_actualizar_producto.place(x=528, y=480, width=150, height=30)
btn_eliminar_producto = tk.Button(productos_page, text="Eliminar", font=('Arial', 12), bg="#1F68A3", fg="white", command=eliminar_registro)
btn_eliminar_producto.place(x=353, y=520, width=150, height=30)
btn_limpiar_producto = tk.Button(productos_page, text="Limpiar", font=('Arial', 12), bg="#1F68A3", fg="white", command=limpiar_campos)
btn_limpiar_producto.place(x=528, y=520, width=150, height=30)

# Crear un estilo para la tabla
style = ttk.Style(root)
style.theme_use("winnative")

# Estilo para la tabla sin bordes ni contornos
style.configure("Custom.Treeview", 
                background="#333538", 
                foreground="white", 
                font=("Arial", 12), 
                relief="flat", 
                borderwidth=0,  # Puedes ajustar el grosor del borde
                fieldbackground="#333538",  # Cambia el fondo vacío al mismo color de la tabla
                highlightthickness=0, 
                rowheight=30)  # Sin borde ni contorno, sin espaciado extra

# Estilo para el encabezado sin bordes ni contornos
style.configure("Custom.Treeview.Heading", 
                background="#333538", 
                foreground="white", 
                font=("Arial", 12), 
                relief="flat", 
                borderwidth=0, 
                highlightthickness=0, 
                anchor="center")  # Cabeceras sin bordes ni contorno

# Estilo para productos "No Disponible"
style.configure("highlight.Treeview", 
                background="lightcoral", 
                foreground="black")

# Tabla para mostrar productos
tabla = ttk.Treeview(productos_page, style="Custom.Treeview", columns=("ID_Producto", "Nombre", "Cantidad", "Estado", "Tipo"), show="headings")

tabla.heading("ID_Producto", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Cantidad", text="Cantidad [KG]")
tabla.heading("Estado", text="Estado")
tabla.heading("Tipo", text="Tipo")

tabla.column("ID_Producto", width=50, anchor="center", stretch=False)  
tabla.column("Nombre", width=150, anchor="w", stretch=True)  
tabla.column("Cantidad", width=100, anchor="w", stretch=True)  
tabla.column("Estado", width=120, anchor="w", stretch=True)  
tabla.column("Tipo", width=120, anchor="w", stretch=True)  

tabla.place(x=720, y=190, width=600, height=390)

# Configurar la etiqueta "highlight" para el estilo especial
tabla.tag_configure("highlight", background="lightcoral", foreground="black")
# Asociar el evento de clic a la tabla para cargar la información al seleccionar un producto
tabla.bind("<ButtonRelease-1>", cargar_registro_seleccionado)

#VISTA PERSONAS

#Contenedor de los detalles del producto
Contenedor_Personas = tk.Canvas(clientes_page, width=970, height=250, highlightthickness=0, bg="#232323")
Contenedor_Personas.place(x=335, y=99)
dibujar_rectangulo_redondeado(Contenedor_Personas, 0, 0, 970, 250, r=10, color="#2A2B2A")

Contenedor_Texto_Personas = tk.Canvas(clientes_page, width=430, height=36, highlightthickness=0, bg="#2A2B2A")
Contenedor_Texto_Personas.place(x=618, y=82)
Contenedor_Texto_Personas_Info = dibujar_rectangulo_redondeado(Contenedor_Texto_Personas, 0, 0, 430, 36, r=10, color="#393A3A")
Contenedor_Texto_Personas.create_text(215, 18, text="Detalles de Personas", fill="white", font=("Arial", 16), anchor="center")


opcion_filtro_busqueda_personas = tk.StringVar()
opcion_filtro_busqueda_personas.set("Seleccione un filtro") # Texto inicial filtro

opciones_filtro_busqueda_personas_opciones = ["Rut", "Nombre", "Apellido", "Rol"]

menu_filtros_busqueda_personas = tk.OptionMenu(clientes_page, opcion_filtro_busqueda_personas, *opciones_filtro_busqueda_personas_opciones)
menu_filtros_busqueda_personas.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_filtros_busqueda_personas.place(x=419, y=156, width=168, height=40)

input_busqueda_personas = tk.Entry(clientes_page, font=('Arial', 12), bg="#333538", fg="white")
input_busqueda_personas.place(x=605, y=156, width=280, height=40)

btn_buscar_filtro_personas = tk.Button(clientes_page, text="Buscar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: obtener_personas_filtrados(opcion_filtro_busqueda_personas.get(),input_busqueda_personas.get()))
btn_buscar_filtro_personas.place(x=903, y=156, width=150, height=40)

btn_mostrar_todo_filtro_personas = tk.Button(clientes_page, text="Mostrar Todo", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: mostrar_personas())
btn_mostrar_todo_filtro_personas.place(x=1071, y=156, width=150, height=40)


Contenedor_Personas.create_text(140, 150, text="RUT", fill="white", font=("Arial", 12), anchor="e")
Contenedor_Personas.create_text(140, 192, text="Nombre", fill="white", font=("Arial", 12), anchor="e")
Contenedor_Personas.create_text(390, 150, text="Apellido", fill="white", font=("Arial", 12), anchor="e")
Contenedor_Personas.create_text(390, 192, text="Rol", fill="white", font=("Arial", 12), anchor="e")

input_personas_rut = tk.Entry(clientes_page, font=('Arial', 12), bg="#333538", fg="white")
input_personas_rut.place(x=487, y=234, width=150, height=30)

input_personas_nombre = tk.Entry(clientes_page, font=('Arial', 12), bg="#333538", fg="white")
input_personas_nombre.place(x=487, y=278, width=150, height=30)

input_personas_apellido = tk.Entry(clientes_page, font=('Arial', 12), bg="#333538", fg="white")
input_personas_apellido.place(x=735, y=234, width=150, height=30)

option_personas_estado = tk.StringVar()
option_personas_estado.set("Elige un Rol") # Texto inicial filtro
option_personas_estado_opciones = ["Proveedor", "Cliente"]
option_personas_estado_menu = tk.OptionMenu(clientes_page, option_personas_estado, *option_personas_estado_opciones)
option_personas_estado_menu.config(font=("Arial", 12), bg="#333538", fg="white", highlightthickness=0)
option_personas_estado_menu.place(x=735, y=277, width=150, height=30)

btn_nueva_persona = tk.Button(clientes_page, text="Nuevo", font=('Arial', 12), bg="#1F68A3", fg="white", command=agregar_nueva_persona)
btn_nueva_persona.place(x=903, y=234, width=150, height=30)
btn_actualizar_persona = tk.Button(clientes_page, text="Actualizar", font=('Arial', 12), bg="#1F68A3", fg="white", command=actualizar_registro_persona)
btn_actualizar_persona.place(x=1071, y=234, width=150, height=30)
btn_eliminar_persona = tk.Button(clientes_page, text="Eliminar", font=('Arial', 12), bg="#1F68A3", fg="white", command=eliminar_registro_persona)
btn_eliminar_persona.place(x=903, y=278, width=150, height=30)
btn_limpiar_persona = tk.Button(clientes_page, text="Limpiar", font=('Arial', 12), bg="#1F68A3", fg="white", command=limpiar_campos_persona)
btn_limpiar_persona.place(x=1071, y=278, width=150, height=30)


# Tabla para mostrar productos
tabla_personas = ttk.Treeview(clientes_page, style="Custom.Treeview", columns=("Rut_Persona", "Nombre", "Apellido", "Rol"), show="headings")

tabla_personas.heading("Rut_Persona", text="Rut")
tabla_personas.heading("Nombre", text="Nombre")
tabla_personas.heading("Apellido", text="Apellido")
tabla_personas.heading("Rol", text="Estado")

tabla_personas.column("Rut_Persona", width=150, anchor="center", stretch=False)  
tabla_personas.column("Nombre", width=150, anchor="w", stretch=True)  
tabla_personas.column("Apellido", width=150, anchor="w", stretch=True)  
tabla_personas.column("Rol", width=150, anchor="w", stretch=True)    

tabla_personas.place(x=335, y=360, width=970, height=250)

# Asociar el evento de clic a la tabla para cargar la información al seleccionar un producto
tabla_personas.bind("<ButtonRelease-1>", cargar_registro_seleccionado_persona)


#VISTA TRANSACCIONES

#Contenedor de los detalles del producto
Contenedor_transacciones = tk.Canvas(transac_page, width=320, height=510, highlightthickness=0, bg="#232323")
Contenedor_transacciones.place(x=320, y=100)
dibujar_rectangulo_redondeado(Contenedor_transacciones, 0, 0, 320, 510, r=10, color="#2A2B2A")

Contenedor_Texto_transacciones = tk.Canvas(transac_page, width=270, height=32, highlightthickness=0, bg="#2A2B2A")
Contenedor_Texto_transacciones.place(x=343, y=84)
Contenedor_Texto_transacciones_Info = dibujar_rectangulo_redondeado(Contenedor_Texto_transacciones, 0, 0, 270, 32, r=10, color="#393A3A")
Contenedor_Texto_transacciones.create_text(135, 16, text="Detalles de Transacciones", fill="white", font=("Arial", 16), anchor="center")

#Contenedor de los detalles de las personas
Contenedor_transacciones_Personas = tk.Canvas(transac_page, width=680, height=65, highlightthickness=0, bg="#232323")
Contenedor_transacciones_Personas.place(x=650, y=100)
dibujar_rectangulo_redondeado(Contenedor_transacciones_Personas, 0, 0, 680, 65, r=10, color="#2A2B2A")

Contenedor_Texto_transacciones = tk.Canvas(transac_page, width=233, height=32, highlightthickness=0, bg="#2A2B2A")
Contenedor_Texto_transacciones.place(x=665, y=84)
Contenedor_Texto_transacciones_Info = dibujar_rectangulo_redondeado(Contenedor_Texto_transacciones, 0, 0, 233, 32, r=10, color="#393A3A")
Contenedor_Texto_transacciones.create_text(116, 16, text="Detalles de Personas", fill="white", font=("Arial", 16), anchor="center")

Contenedor_transacciones_Personas.create_text(80, 40, text="Nombre", fill="white", font=("Arial", 12), anchor="e")
input_transacciones_nombre_persona = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_nombre_persona.place(x=735, y=125, width=100, height=30)

Contenedor_transacciones_Personas.create_text(262, 40, text="Apellido", fill="white", font=("Arial", 12), anchor="e")
input_transacciones_apellido_persona = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_apellido_persona.place(x=917, y=125, width=100, height=30)

Contenedor_transacciones_Personas.create_text(451, 40, text="Producto", fill="white", font=("Arial", 12), anchor="e")
input_transacciones_nombre_producto = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_nombre_producto.place(x=1106, y=125, width=100, height=30)


#Contenedor de los filtros del producto
Contenedor_transacciones_filtros = tk.Canvas(transac_page, width=680, height=66, highlightthickness=0, bg="#232323")
Contenedor_transacciones_filtros.place(x=650, y=180)
dibujar_rectangulo_redondeado(Contenedor_transacciones_filtros, 0, 0, 680, 66, r=10, color="#2A2B2A")


opcion_filtro_busqueda_transacciones = tk.StringVar()
opcion_filtro_busqueda_transacciones.set("Seleccione un filtro") # Texto inicial filtro

opciones_filtro_busqueda_transacciones_opciones = ["ID", "Rut_Persona", "ID_Producto", "Fecha", "Accion", "Cantidad", "Precio"]

menu_filtros_busqueda_transacciones = tk.OptionMenu(transac_page, opcion_filtro_busqueda_transacciones, *opciones_filtro_busqueda_transacciones_opciones)
menu_filtros_busqueda_transacciones.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_filtros_busqueda_transacciones.place(x=668, y=198, width=172, height=30)

input_busqueda_transacciones = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_busqueda_transacciones.place(x=852, y=198, width=176, height=30)

btn_buscar_filtro_transacciones = tk.Button(transac_page, text="Buscar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: obtener_transacciones_filtrados(opcion_filtro_busqueda_transacciones.get(),input_busqueda_transacciones.get()))
btn_buscar_filtro_transacciones.place(x=1040, y=198, width=120, height=30)

btn_mostrar_todo_filtro_transacciones = tk.Button(transac_page, text="Mostrar Todo", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: mostrar_transacciones())
btn_mostrar_todo_filtro_transacciones.place(x=1172, y=198, width=140, height=30)






Contenedor_transacciones.create_text(115, 60, text="ID", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 110, text="Rut", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 160, text="ID_Producto", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 215, text="Fecha", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 265, text="Acción", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 320, text="Cantidad [KG]", fill="white", font=("Arial", 12), anchor="e")
Contenedor_transacciones.create_text(115, 370, text="Precio [$]", fill="white", font=("Arial", 12), anchor="e")

input_transacciones_id = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_id.place(x=445, y=145, width=160, height=30)

input_transacciones_id_persona = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_id_persona.place(x=445, y=194, width=160, height=30)

input_transacciones_id_producto = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_id_producto.place(x=445, y=246, width=160, height=30)

input_transacciones_fecha = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_fecha.place(x=445, y=302, width=160, height=30)

option_transacciones_estado = tk.StringVar()
option_transacciones_estado.set("Elige una acción") # Texto inicial filtro
option_transacciones_estado_opciones = ["Compra", "Venta"]
option_transacciones_estado_menu = tk.OptionMenu(transac_page, option_transacciones_estado, *option_transacciones_estado_opciones)
option_transacciones_estado_menu.config(font=("Arial", 12), bg="#333538", fg="white", highlightthickness=0)
option_transacciones_estado_menu.place(x=445, y=353, width=160, height=30)

input_transacciones_cantidad = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_cantidad.place(x=445, y=404, width=160, height=30)

input_transacciones_precio = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_precio.place(x=445, y=455, width=160, height=30)

btn_nueva_transac = tk.Button(transac_page, text="Nuevo", font=('Arial', 12), bg="#1F68A3", fg="white", command=agregar_nueva_transaccion)
btn_nueva_transac.place(x=355, y=515, width=120, height=30)
btn_actualizar_transac = tk.Button(transac_page, text="Actualizar", font=('Arial', 12), bg="#1F68A3", fg="white", command=actualizar_registro_transaccion)
btn_actualizar_transac.place(x=485, y=515, width=120, height=30)
btn_eliminar_transac = tk.Button(transac_page, text="Eliminar", font=('Arial', 12), bg="#1F68A3", fg="white", command=eliminar_registro_transaccion)
btn_eliminar_transac.place(x=355, y=555, width=120, height=30)
btn_limpiar_transac = tk.Button(transac_page, text="Limpiar", font=('Arial', 12), bg="#1F68A3", fg="white", command=limpiar_campos_transacciones)
btn_limpiar_transac.place(x=485, y=555, width=120, height=30)

# Tabla para mostrar productos
tabla_transacciones = ttk.Treeview(transac_page, style="Custom.Treeview", columns=("ID_Transaccion", "Persona_ID", "Producto_ID", "Fecha", "Accion", "Cantidad", "Precio"), show="headings")

tabla_transacciones.heading("ID_Transaccion", text="ID")
tabla_transacciones.heading("Persona_ID", text="Rut")
tabla_transacciones.heading("Producto_ID", text="Producto")
tabla_transacciones.heading("Fecha", text="Fecha")
tabla_transacciones.heading("Accion", text="Accion")
tabla_transacciones.heading("Cantidad", text="Cantidad")
tabla_transacciones.heading("Precio", text="Precio")

tabla_transacciones.column("ID_Transaccion", width=50, anchor="center", stretch=False)  
tabla_transacciones.column("Persona_ID", width=100, anchor="w", stretch=True)  
tabla_transacciones.column("Producto_ID", width=50, anchor="w", stretch=True)  
tabla_transacciones.column("Fecha", width=80, anchor="w", stretch=True)    
tabla_transacciones.column("Accion", width=100, anchor="w", stretch=True)    
tabla_transacciones.column("Cantidad", width=100, anchor="w", stretch=True)    
tabla_transacciones.column("Precio", width=100, anchor="w", stretch=True)    

tabla_transacciones.place(x=650, y=261, width=680, height=349)

# Asociar el evento de clic a la tabla para cargar la información al seleccionar un producto
tabla_transacciones.bind("<ButtonRelease-1>", cargar_registro_seleccionado_transaccion)

#Contenedor de los detalles del producto
Contenedor_informes = tk.Canvas(reports_page, width=360, height=170, highlightthickness=0, bg="#232323")
Contenedor_informes.place(x=320, y=115)
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 360, 170, r=10, color="#2A2B2A")

Contenedor_Texto_informes = tk.Canvas(reports_page, width=310, height=36, highlightthickness=0, bg="#2A2B2A")
Contenedor_Texto_informes.place(x=345, y=100)
Contenedor_Texto_informes_Info = dibujar_rectangulo_redondeado(Contenedor_Texto_informes, 0, 0, 310, 36, r=10, color="#393A3A")
Contenedor_Texto_informes.create_text(155, 18, text="Detalles de Transacciones", fill="white", font=("Arial", 16), anchor="center")

Contenedor_informes_ventas_precio = tk.Canvas(reports_page, width=170, height=85, highlightthickness=0, bg="#232323")
Contenedor_informes_ventas_precio.place(x=320, y=305)
Contenedor_informes_ventas_precio.create_text(85, 45, text="Ventas", fill="white", font=("Arial", 12, "bold"), anchor="center")
ci_ventas_precio = Contenedor_informes_ventas_precio.create_text(85, 65, text="0", fill="white", font=("Arial", 12, "bold"), anchor="center")
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 170, 85, r=10, color="#2A2B2A")

Contenedor_informes_ventas_peso = tk.Canvas(reports_page, width=170, height=85, highlightthickness=0, bg="#232323")
Contenedor_informes_ventas_peso.place(x=320, y=410)
Contenedor_informes_ventas_peso.create_text(85, 45, text="Ventas", fill="white", font=("Arial", 12, "bold"), anchor="center")
ci_ventas_peso = Contenedor_informes_ventas_peso.create_text(85, 65, text="0", fill="white", font=("Arial", 12, "bold"), anchor="center")
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 170, 85, r=10, color="#2A2B2A")

Contenedor_informes_compras_precio = tk.Canvas(reports_page, width=170, height=85, highlightthickness=0, bg="#232323")
Contenedor_informes_compras_precio.place(x=510, y=305)
Contenedor_informes_compras_precio.create_text(85, 45, text="Compras", fill="white", font=("Arial", 12, "bold"), anchor="center")
ci_compras_precio = Contenedor_informes_compras_precio.create_text(85, 65, text="0", fill="white", font=("Arial", 12, "bold"), anchor="center")
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 170, 85, r=10, color="#2A2B2A")

Contenedor_informes_compras_peso = tk.Canvas(reports_page, width=170, height=85, highlightthickness=0, bg="#232323")
Contenedor_informes_compras_peso.place(x=510, y=410)
Contenedor_informes_compras_peso.create_text(85, 45, text="Compras", fill="white", font=("Arial", 12, "bold"), anchor="center")
ci_compras_peso = Contenedor_informes_compras_peso.create_text(85, 65, text="0", fill="white", font=("Arial", 12, "bold"), anchor="center")
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 170, 85, r=10, color="#2A2B2A")

Contenedor_informes_stock = tk.Canvas(reports_page, width=360, height=83, highlightthickness=0, bg="#232323")
Contenedor_informes_stock.place(x=320, y=515)
Contenedor_informes_stock.create_text(180, 45, text="Stock", fill="white", font=("Arial", 12, "bold"), anchor="center")
ci_stock = Contenedor_informes_stock.create_text(180, 65, text="0", fill="white", font=("Arial", 12, "bold"), anchor="center")
dibujar_rectangulo_redondeado(Contenedor_informes, 0, 0, 360, 83, r=10, color="#2A2B2A")

opcion_mes_informe = tk.StringVar()
opcion_mes_informe.set("Seleccione un filtro") # Texto inicial filtro

opcion_mes_informe_opciones = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

menu_opcion_mes_informe = tk.OptionMenu(reports_page, opcion_mes_informe, *opcion_mes_informe_opciones)
menu_opcion_mes_informe.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_opcion_mes_informe.place(x=335, y=222, width=330, height=40)



opcion_producto_informe = tk.StringVar()
opcion_producto_informe.set("Seleccione un filtro") # Texto inicial filtro

meses_dict = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
    "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

menu_opcion_producto_informe = tk.OptionMenu(reports_page, opcion_producto_informe, *meses_dict.keys())
menu_opcion_producto_informe.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_opcion_producto_informe.place(x=335, y=162, width=330, height=40)

# --- Vincular eventos ---
opcion_mes_informe.trace_add("write", ejecutar_consulta)
opcion_producto_informe.trace_add("write", ejecutar_consulta)

create_database()
actualizar_contenido()
# Iniciar la actualización del reloj
actualizar_reloj(canvas3, texto_id)
mostrar_pestaña("dashboard")
center_window(root)
root.mainloop()
