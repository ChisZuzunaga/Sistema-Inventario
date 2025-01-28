import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk  # Usado para cargar imágenes JPG/PNG

def mostrar_pestaña(frame):
    # Ocultar todos los frames
    for f in frames:
        f.pack_forget()  # Esconde todos los frames
    # Mostrar el frame seleccionado
    frame.pack(fill="both", expand=True)

root = tk.Tk()
root.title("Sistema de Inventario")
root.geometry("1340x630")
root.configure(bg="#232323")
root.resizable(False, False)

# Crear los frames (simulando pestañas)
ventana = tk.Frame(root, bg="#232323")  # Pestaña 1
ventana2 = tk.Frame(root, bg="#32CD32")  # Pestaña 2
ventana3 = tk.Frame(root, bg="#1E90FF")  # Pestaña 3

# Agregar contenido a los frames
label1 = tk.Label(ventana, text="Contenido de la Pestaña 1", font=("Arial", 20), bg="#FF6347")
label1.pack(pady=20)

label2 = tk.Label(ventana2, text="Contenido de la Pestaña 2", font=("Arial", 20), bg="#32CD32")
label2.pack(pady=20)

label3 = tk.Label(ventana3, text="Contenido de la Pestaña 3", font=("Arial", 20), bg="#1E90FF")
label3.pack(pady=20)

def get_clientes():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Persona WHERE rol = 'Cliente'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_clientes = resultado[0]

        # Actualizar el texto del canvas
        canvas4.itemconfig(texto_canvas, text=f"Clientes: {conteo_clientes}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas4.itemconfig(texto_canvas, text="Error al cargar datos")

def get_proveedor():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Persona WHERE rol = 'Proveedor'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_proveedor = resultado[0]

        # Actualizar el texto del canvas
        canvas5.itemconfig(texto_canvas, text=f"Proveedor: {conteo_proveedor}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas5.itemconfig(texto_canvas, text="Error al cargar datos")

def get_productos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Productos")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_productos = resultado[0]

        # Actualizar el texto del canvas
        canvas6.itemconfig(texto_canvas, text=f"Productos: {conteo_productos}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas6.itemconfig(texto_canvas, text="Error al cargar datos")

def get_compras():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Compra'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_compras = resultado[0]

        # Actualizar el texto del canvas
        canvas8.itemconfig(texto_canvas, text=f"Compras: {conteo_compras}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas8.itemconfig(texto_canvas, text="Error al cargar datos")

def get_ventas():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion where accion = 'Venta'")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_ventas = resultado[0]

        # Actualizar el texto del canvas
        canvas9.itemconfig(texto_canvas, text=f"Ventas: {conteo_ventas}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas9.itemconfig(texto_canvas, text="Error al cargar datos")

def get_transacciones():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT count(*) FROM Transaccion")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_transacciones = resultado[0]

        # Actualizar el texto del canvas
        canvas10.itemconfig(texto_canvas, text=f"Transacciones: {conteo_transacciones}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas10.itemconfig(texto_canvas, text="Error al cargar datos")

def get_utilidad():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('productos.db')  # Cambia la ruta si es necesario
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT SUM(CASE WHEN Accion = 'Venta' THEN Precio ELSE 0 END) - SUM(CASE WHEN Accion = 'Compra' THEN Precio ELSE 0 END) AS Utilidad FROM Transaccion")
        resultado = cursor.fetchone()

        # Obtener el conteo de vendedores
        conteo_utilidad = resultado[0]

        # Actualizar el texto del canvas
        canvas7.itemconfig(texto_canvas, text=f"Utilidad: {conteo_utilidad}")

        # Cerrar conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        canvas7.itemconfig(texto_canvas, text="Error al cargar datos")

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

# Canvas 1: Barra superior
canvas1 = tk.Canvas(ventana, width=1340, height=70, highlightthickness=0, bg="#292B2B")
canvas1.place(x=0, y=0)
canvas1.create_rectangle(0, 0, 1340, 70, fill="#292B2B", outline="#292B2B")
# Agregar texto dentro del rectángulo
texto = canvas1.create_text(80, 35, text="Inventario", fill="white", font=("Arial", 16, "bold"))
image1A = Image.open("Img/Img-8.png")  # Cambia la ruta por la de tu imagen
photo1A = ImageTk.PhotoImage(image1A)
canvas1.create_image(170, 35, image=photo1A)
canvas1.image = photo1A

# Canvas 2: Panel lateral izquierdo
canvas2 = tk.Canvas(ventana, width=300, height=560, highlightthickness=0, bg="#292B2B")
canvas2.place(x=0, y=70)  # Colocado justo debajo del canvas1
canvas2.create_rectangle(0, 0, 300, 560, fill="#292B2B", outline="#292B2B")

image2A = Image.open("Img/Img-9.png")  # Cambia la ruta por la de tu imagen
photo2A = ImageTk.PhotoImage(image2A)
canvas2.create_image(150, 80, image=photo2A)
canvas2.image = photo2A
canvas2.create_text(70, 180, text="Menú", fill="white", font=("Helvetica", 30, "bold"))
canvas2.create_rectangle(20, 200, 275, 203, fill="#FFFFFF", outline="#FFFFFF")
# Canvas 3: Contenido principal
canvas3 = tk.Canvas(ventana, width=1000, height=35, highlightthickness=0, bg="#292B2B")
canvas3.place(x=312, y=17)  # Coordenadas específicas dentro de la ventana
dibujar_rectangulo_redondeado(canvas3, 0, 0, 1000, 35, r=10, color="#3A3939")

# Texto inicial en el centro del Canvas
texto_id = canvas3.create_text(500, 17.5, text="", fill="white", font=("Helvetica", 16, "bold"))

# Canvas 4: Botoneras
canvas4 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas4.place(x=360, y=170)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(canvas4, 0, 0, 280, 100, r=20, color="#8B51F5")
canvas41 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#6334E3")
canvas41.place(x=360, y=170)  # Colocado justo debajo del canvas1
canvas41.create_rectangle(0, 0, 100, 100, fill="#6334E3", outline="#6334E3")

# Agregar texto dentro del rectángulo
texto_canvas = canvas4.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image1 = Image.open("Img/Img-1.png")  # Cambia la ruta por la de tu imagen
photo1 = ImageTk.PhotoImage(image1)
canvas41.create_image(50, 50, image=photo1)
canvas41.image = photo1

# Canvas 5: Botoneras
canvas5 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas5.place(x=680, y=170)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(canvas5, 0, 0, 280, 100, r=20, color="#C0C0C0")
canvas51 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#AAAAAA")
canvas51.place(x=680, y=170)  # Colocado justo debajo del canvas1
canvas51.create_rectangle(0, 0, 100, 100, fill="#AAAAAA", outline="#AAAAAA")

# Agregar texto dentro del rectángulo
texto = canvas5.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image2 = Image.open("Img/Img-2.png")  # Cambia la ruta por la de tu imagen
photo2 = ImageTk.PhotoImage(image2)
canvas51.create_image(50, 50, image=photo2)
canvas51.image = photo2

# Canvas 6: Botoneras
canvas6 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas6.place(x=1000, y=170)  # Colocado justo debajo del canvas1
rectangulo3 = dibujar_rectangulo_redondeado(canvas6, 0, 0, 280, 100, r=20, color="#F06E9C")
canvas61 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#E93578")
canvas61.place(x=1000, y=170)  # Colocado justo debajo del canvas1
rectangulo31 = canvas61.create_rectangle(0, 0, 100, 100, fill="#E93578", outline="#E93578")

# Agregar texto dentro del rectángulo
texto = canvas6.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image3 = Image.open("Img/Img-3.png")  # Cambia la ruta por la de tu imagen
photo3 = ImageTk.PhotoImage(image3)
image31 = canvas61.create_image(50, 50, image=photo3)
canvas61.image = photo3

canvas6.config(cursor="hand2")  # Cursor estilo "manito"
canvas61.config(cursor="hand2")  # Cursor estilo "manito"


# Canvas 7: Botoneras
canvas7 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas7.place(x=360, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(canvas7, 0, 0, 280, 100, r=20, color="#3D8AF7")
canvas71 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#3D8AF7")
canvas71.place(x=360, y=300)  # Colocado justo debajo del canvas1
canvas71.create_rectangle(0, 0, 100, 100, fill="#1464F6", outline="#1464F6")

# Agregar texto dentro del rectángulo
texto = canvas7.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image4 = Image.open("Img/Img-4.png")  # Cambia la ruta por la de tu imagen
photo4 = ImageTk.PhotoImage(image4)
canvas71.create_image(50, 50, image=photo4)
canvas71.image = photo4


# Canvas 8: Botoneras
canvas8 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas8.place(x=680, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(canvas8, 0, 0, 280, 100, r=20, color="#92D36E")
canvas81 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#72BB53")
canvas81.place(x=680, y=300)  # Colocado justo debajo del canvas1
canvas81.create_rectangle(0, 0, 100, 100, fill="#72BB53", outline="#72BB53")

# Agregar texto dentro del rectángulo
texto = canvas8.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image5 = Image.open("Img/Img-5.png")  # Cambia la ruta por la de tu imagen
photo5 = ImageTk.PhotoImage(image5)
canvas81.create_image(50, 50, image=photo5)
canvas81.image = photo5

# Canvas 9: Botoneras
canvas9 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas9.place(x=1000, y=300)  # Colocado justo debajo del canvas1
dibujar_rectangulo_redondeado(canvas9, 0, 0, 280, 100, r=20, color="#FF5D55")
canvas91 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#FF3823")
canvas91.place(x=1000, y=300)  # Colocado justo debajo del canvas1
canvas91.create_rectangle(0, 0, 100, 100, fill="#FF3823", outline="#FF3823")

# Agregar texto dentro del rectángulo
texto = canvas9.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image6 = Image.open("Img/Img-6.png")  # Cambia la ruta por la de tu imagen
photo6 = ImageTk.PhotoImage(image6)
canvas91.create_image(50, 50, image=photo6)
canvas91.image = photo6


# Canvas 10: Botoneras
canvas10 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas10.place(x=360, y=430)  # Colocado justo debajo del canvas1
rectangulo7 = dibujar_rectangulo_redondeado(canvas10, 0, 0, 280, 100, r=20, color="#4DD7FA")
canvas101 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#00C8F8")
canvas101.place(x=360, y=430)  # Colocado justo debajo del canvas1
rectangulo71 = canvas101.create_rectangle(0, 0, 100, 100, fill="#00C8F8", outline="#00C8F8")

# Agregar texto dentro del rectángulo
texto = canvas10.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image7 = Image.open("Img/Img-7.png")  # Cambia la ruta por la de tu imagen
photo7 = ImageTk.PhotoImage(image7)
image71 = canvas101.create_image(50, 50, image=photo7)
canvas101.image = photo7

canvas10.config(cursor="hand2")  # Cursor estilo "manito"
canvas101.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el canvas4 con la función del rectángulo
canvas10.tag_bind(rectangulo7, "<Button-1>", on_rectangle_click1)
canvas101.tag_bind(rectangulo71, "<Button-1>", on_rectangle_click1)
canvas101.tag_bind(image71, "<Button-1>", on_rectangle_click1)

# Canvas 11: Botoneras
canvas11 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas11.place(x=680, y=430)  # Colocado justo debajo del canvas1
rectangulo8 = dibujar_rectangulo_redondeado(canvas11, 0, 0, 280, 100, r=20, color="#FFD783")
canvas111 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#FFC957")
canvas111.place(x=680, y=430)  # Colocado justo debajo del canvas1
rectangulo81 = canvas111.create_rectangle(0, 0, 100, 100, fill="#FFC957", outline="#FFC957")

# Agregar texto dentro del rectángulo
texto = canvas11.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image8 = Image.open("Img/Img-5.png")  # Cambia la ruta por la de tu imagen
photo8 = ImageTk.PhotoImage(image8)
image81 = canvas111.create_image(50, 50, image=photo8)
canvas111.image = photo8

canvas11.config(cursor="hand2")  # Cursor estilo "manito"
canvas111.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el canvas4 con la función del rectángulo
canvas11.tag_bind(rectangulo8, "<Button-1>", on_rectangle_click1)
canvas111.tag_bind(rectangulo81, "<Button-1>", on_rectangle_click1)
canvas111.tag_bind(image81, "<Button-1>", on_rectangle_click1)

# Canvas 12: Botoneras
canvas12 = tk.Canvas(ventana, width=280, height=100, highlightthickness=0, bg="#232323")
canvas12.place(x=1000, y=430)  # Colocado justo debajo del canvas1
rectangulo9 = dibujar_rectangulo_redondeado(canvas12, 0, 0, 280, 100, r=20, color="#FFA382")
canvas121 = tk.Canvas(ventana, width=100, height=100, highlightthickness=0, bg="#FF8351")
canvas121.place(x=1000, y=430)  # Colocado justo debajo del canvas1
rectangulo91 = canvas121.create_rectangle(0, 0, 100, 100, fill="#FF8351", outline="#FF8351")

# Agregar texto dentro del rectángulo
texto = canvas12.create_text(190, 50, text="Haz clic aquí", fill="white", font=("Arial", 16, "bold"))

image9 = Image.open("Img/Img-6.png")  # Cambia la ruta por la de tu imagen
photo9 = ImageTk.PhotoImage(image9)
image91 = canvas121.create_image(50, 50, image=photo9)
canvas121.image = photo9

canvas12.config(cursor="hand2")  # Cursor estilo "manito"
canvas121.config(cursor="hand2")  # Cursor estilo "manito"

# Asociar el clic sobre el canvas4 con la función del rectángulo
canvas12.tag_bind(rectangulo9, "<Button-1>", on_rectangle_click1)
canvas121.tag_bind(rectangulo91, "<Button-1>", on_rectangle_click1)
canvas121.tag_bind(image91, "<Button-1>", on_rectangle_click1)

ventana.after(100, get_clientes)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_proveedor)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_productos)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_compras)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_ventas)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_transacciones)  # Ejecuta la función 100ms después de iniciar la ventana
ventana.after(100, get_utilidad)  # Ejecuta la función 100ms después de iniciar la ventana



# Iniciar la actualización del reloj
actualizar_reloj(canvas3, texto_id)

# Lista de frames
frames = [ventana, ventana2, ventana3]

# Crear botones para cambiar entre las pestañas
boton1 = tk.Button(root, text="Pestaña 1", command=lambda: mostrar_pestaña(ventana))
boton2 = tk.Button(root, text="Pestaña 2", command=lambda: mostrar_pestaña(ventana2))
boton3 = tk.Button(root, text="Pestaña 3", command=lambda: mostrar_pestaña(ventana3))

# Colocar los botones al principio
boton1.pack(side="left", padx=5, pady=5)
boton2.pack(side="left", padx=5, pady=5)
boton3.pack(side="left", padx=5, pady=5)

mostrar_pestaña(ventana)
center_window(root)
root.mainloop()
