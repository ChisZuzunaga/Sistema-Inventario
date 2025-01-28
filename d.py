import tkinter as tk

# Función para cambiar entre pestañas
def mostrar_pestaña(frame):
    # Ocultar todos los frames
    for f in frames:
        f.pack_forget()  # Esconde todos los frames
    # Mostrar el frame seleccionado
    frame.pack(fill="both", expand=True)

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("500x400")  # Tamaño de la ventana

# Crear los frames (simulando pestañas)
frame1 = tk.Frame(ventana, bg="#FF6347")  # Pestaña 1
frame2 = tk.Frame(ventana, bg="#32CD32")  # Pestaña 2
frame3 = tk.Frame(ventana, bg="#1E90FF")  # Pestaña 3

# Agregar contenido a los frames
label1 = tk.Label(frame1, text="Contenido de la Pestaña 1", font=("Arial", 20), bg="#FF6347")
label1.pack(pady=20)

label2 = tk.Label(frame2, text="Contenido de la Pestaña 2", font=("Arial", 20), bg="#32CD32")
label2.pack(pady=20)

label3 = tk.Label(frame3, text="Contenido de la Pestaña 3", font=("Arial", 20), bg="#1E90FF")
label3.pack(pady=20)

# Lista de frames
frames = [frame1, frame2, frame3]

# Crear botones para cambiar entre las pestañas
boton1 = tk.Button(ventana, text="Pestaña 1", command=lambda: mostrar_pestaña(frame1))
boton2 = tk.Button(ventana, text="Pestaña 2", command=lambda: mostrar_pestaña(frame2))
boton3 = tk.Button(ventana, text="Pestaña 3", command=lambda: mostrar_pestaña(frame3))

# Colocar los botones al principio
boton1.pack(side="left", padx=5, pady=5)
boton2.pack(side="left", padx=5, pady=5)
boton3.pack(side="left", padx=5, pady=5)

# Mostrar la primera pestaña al inicio
mostrar_pestaña(frame1)

# Ejecutar la ventana principal
ventana.mainloop()