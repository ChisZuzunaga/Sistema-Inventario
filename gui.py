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
clientes_page = tk.Frame(root, bg="#32CD32")  # Pestaña 2
productos_page = tk.Frame(root, bg="#1E90FF")  # Pestaña 3
transac_page = tk.Frame(root, bg="#BEDFAA")  # Pestaña 4
reports_page = tk.Frame(root, bg="#AAAAAA")  # Pestaña 5
config_page = tk.Frame(root, bg="#242224")  # Pestaña 6

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

def actualizar_contenido():
    main_page.after(100, get_clientes)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_proveedor)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_productos)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_compras)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_ventas)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_transacciones)  # Ejecuta la función 100ms después de iniciar la main_page
    main_page.after(100, get_utilidad)  # Ejecuta la función 100ms después de iniciar la main_page

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

        cursor.execute("SELECT COUNT(*) FROM Persona")
        info["Personas"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Transaccion")
        info["Transacciones"] = cursor.fetchone()[0]

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
                           f"Personas: {info.get('Personas', 'Error')}\n"
                           f"Transacciones: {info.get('Transacciones', 'Error')}\n")

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
    ventana_personas = tk.Toplevel(root)
    ventana_personas.title("Agregar Proveedor")
    ventana_personas.geometry("400x300")
    ventana_personas.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Etiqueta y campo para Cantidad

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_personas)
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
    btn_agregar = tk.Button(frame_entrada, text="Agregar Proveedor", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_personas(campos_compras))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas.destroy)
    btn_cerrar.pack(pady=0)

def abrir_ventana_personas_cliente():
    ventana_personas = tk.Toplevel(root)
    ventana_personas.title("Agregar Cliente")
    ventana_personas.geometry("400x300")
    ventana_personas.configure(bg="#2A2B2A")

    # Diccionario para almacenar los campos_compras de entrada
    campos_compras = {}

    # Etiqueta y campo para Cantidad

    # Entradas para agregar producto
    frame_entrada = tk.Frame(ventana_personas)
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
    btn_agregar = tk.Button(frame_entrada, text="Agregar Cliente", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_personas(campos_compras))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas.destroy)
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
        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, DATE('now'), ?, ?, ?)
        """, (proveedor_rut, producto_id, accion, cantidad, precio))
        conn.commit()
        conn.close()
        actualizar_contenido()
        messagebox.showinfo("Éxito", "Compra registrada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la compra: {e}")

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
        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, DATE('now'), ?, ?, ?)
        """, (cliente_rut, producto_id, accion, cantidad, precio))
        conn.commit()
        conn.close()
        actualizar_contenido()
        messagebox.showinfo("Éxito", "Venta registrada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")

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
    btn_cerrar = tk.Button(ventana_compras, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_transaccion_compras(campos_compras, productos_dict, proveedores_dict))
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
    btn_cerrar = tk.Button(ventana_ventas, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_transaccion_ventas(campos_compras, productos_dict, clientes_dict))
    btn_cerrar.pack()


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

actualizar_contenido()

# Iniciar la actualización del reloj
actualizar_reloj(canvas3, texto_id)

mostrar_pestaña("dashboard")
center_window(root)
root.mainloop()
