import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Conexión a la base de datos
conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

# Inicialización de las tablas
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
conexion.commit()

# Función para ver todos los productos
def ver_productos():
    ventana_compras = tk.Toplevel(ventana)
    ventana_compras.title("Lista de Productos")
    ventana_compras.geometry("600x400")

    # Tabla para mostrar productos
    tabla = ttk.Treeview(ventana_compras, columns=("Nombre", "Cantidad", "Estado", "Tipo"), show="headings")
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
    btn_cerrar = tk.Button(ventana_compras, text="Cerrar", command=ventana_compras.destroy)
    btn_cerrar.pack(pady=10)

# Función para agregar producto
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
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar a la persona: {e}")




    tk.Label(frame_entrada, text="Acción:", font=('Arial', 12), anchor="w", bg="#2A2B2A", fg="white").grid(row=5, column=0, padx=5, pady=(0,10), sticky="w")
    campos_compras['accion'] = tk.Entry(frame_entrada, width=22, font=('Arial', 12), fg="#7A7A7A")
    campos_compras['accion'].insert(0, "Compra")  # Valor por defecto
    campos_compras['accion'].config(state=tk.DISABLED, disabledbackground="#AAAAAA", disabledforeground="#7A7A7A")
    campos_compras['accion'].grid(row=5, column=1, padx=5, pady=(0,10))


def abrir_ventana_personas_proveedor():
    ventana_personas = tk.Toplevel(ventana)
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
    btn_agregar = tk.Button(frame_entrada, text="Agregar Persona", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_personas(campos_compras))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas.destroy)
    btn_cerrar.pack(pady=0)

def abrir_ventana_personas_cliente():
    ventana_personas = tk.Toplevel(ventana)
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
    btn_agregar = tk.Button(frame_entrada, text="Agregar Persona", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_personas(campos_compras))
    btn_agregar.grid(row=4, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_personas, text="Cerrar", font=('Arial', 12), bg="#1F68A3", fg="white", command=ventana_personas.destroy)
    btn_cerrar.pack(pady=0)

def validar_numero(event, campo, label_error):
    """Valida que solo se ingresen números en el campo."""
    entrada = campo.get()
    if not entrada.isdigit():
        campo.config(bg="#FFCCCC")  # Fondo rojo si no es válido
        label_error.config(text="Solo se permiten números.", fg="red")
    else:
        campo.config(bg="#333538")  # Fondo normal si es válido
        label_error.config(text="")


def abrir_ventana_compras():
    ventana_compras = tk.Toplevel(ventana)
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
        conn = sqlite3.connect('productos.db')
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
    tk.Label(frame_entrada, text="Cantidad:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=(10,0), sticky="w")
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
    tk.Label(frame_entrada, text="Precio:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=6, column=0, padx=5, pady=(10,0), sticky="w")
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
    btn_agregar = tk.Button(frame_entrada, text="Agregar Proveedor", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: abrir_ventana_personas_cliente())
    btn_agregar.grid(row=9, column=0, columnspan=2, pady=(50,0))

    # Botón para cerrar ventana
    btn_cerrar = tk.Button(ventana_compras, text="Aceptar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: agregar_transaccion_compras(campos_compras, productos_dict, proveedores_dict))
    btn_cerrar.pack()

def abrir_ventana_ventas():
    ventana_ventas = tk.Toplevel(ventana)
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
        conn = sqlite3.connect('productos.db')
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
    tk.Label(frame_entrada, text="Cantidad:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=3, column=0, padx=5, pady=(10,0), sticky="w")
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
    tk.Label(frame_entrada, text="Precio:", font=('Arial', 12), bg="#2A2B2A", fg="white").grid(row=6, column=0, padx=5, pady=(10,0), sticky="w")
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
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, DATE('now'), ?, ?, ?)
        """, (proveedor_rut, producto_id, accion, cantidad, precio))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

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
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Transaccion (Persona_ID, Producto_ID, Fecha, Accion, Cantidad, Precio)
            VALUES (?, ?, DATE('now'), ?, ?, ?)
        """, (cliente_rut, producto_id, accion, cantidad, precio))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

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
btn_abrir_productos = tk.Button(ventana, text="Agregar Producto", command=abrir_ventana_compras)
btn_abrir_productos.pack(pady=20)

btn_abrir_personas = tk.Button(ventana, text="Agregar Persona", command=abrir_ventana_personas_cliente)
btn_abrir_personas.pack(pady=20)

btn_ver_productos = tk.Button(ventana, text="Ver Productos", command=ver_productos)
btn_ver_productos.pack(pady=10)

btn_ver_personas = tk.Button(ventana, text="Ver Personas", command=ver_personas)
btn_ver_personas.pack(pady=10)

btn_ver_ventas = tk.Button(ventana, text="Registrar venta", command=abrir_ventana_ventas)
btn_ver_ventas.pack(pady=10)
# Ejecutar la ventana principal
ventana.mainloop()



btn_abrir_productos = tk.Button(ventana, text="Agregar Producto", command=abrir_ventana_compras)
btn_abrir_productos.pack(pady=20)