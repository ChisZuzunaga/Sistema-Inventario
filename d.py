#Contenedor de los detalles del producto
Contenedor_transacciones = tk.Canvas(transac_page, width=970, height=250, highlightthickness=0, bg="#232323")
Contenedor_transacciones.place(x=335, y=99)
dibujar_rectangulo_redondeado(Contenedor_transacciones, 0, 0, 970, 250, r=10, color="#2A2B2A")

Contenedor_Texto_transacciones = tk.Canvas(transac_page, width=430, height=36, highlightthickness=0, bg="#2A2B2A")
Contenedor_Texto_transacciones.place(x=618, y=82)
Contenedor_Texto_transacciones_Info = dibujar_rectangulo_redondeado(Contenedor_Texto_transacciones, 0, 0, 430, 36, r=10, color="#393A3A")
Contenedor_Texto_transacciones.create_text(215, 18, text="Detalles de transacciones", fill="white", font=("Arial", 16), anchor="center")


opcion_filtro_busqueda_transacciones = tk.StringVar()
opcion_filtro_busqueda_transacciones.set("Seleccione un filtro") # Texto inicial filtro

opciones_filtro_busqueda_transacciones_opciones = ["Rut", "Nombre", "Apellido", "Rol"]

menu_filtros_busqueda_transacciones = tk.OptionMenu(transac_page, opcion_filtro_busqueda_transacciones, *opciones_filtro_busqueda_transacciones_opciones)
menu_filtros_busqueda_transacciones.config(font=("Arial", 12), bg="#1F68A3", fg="white",highlightthickness=0)
menu_filtros_busqueda_transacciones.place(x=419, y=156, width=168, height=40)

input_busqueda_transacciones = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_busqueda_transacciones.place(x=605, y=156, width=280, height=40)

btn_buscar_filtro_transacciones = tk.Button(transac_page, text="Buscar", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: obtener_transacciones_filtrados(opcion_filtro_busqueda_transacciones.get(),input_busqueda_transacciones.get()))
btn_buscar_filtro_transacciones.place(x=903, y=156, width=150, height=40)

btn_mostrar_todo_filtro_transacciones = tk.Button(transac_page, text="Mostrar Todo", font=('Arial', 12), bg="#1F68A3", fg="white", command=lambda: mostrar_transacciones())
btn_mostrar_todo_filtro_transacciones.place(x=1071, y=156, width=150, height=40)


Contenedor_transacciones.create_text(140, 150, text="RUT", fill="white", font=("Arial", 14), anchor="e")
Contenedor_transacciones.create_text(140, 192, text="Nombre", fill="white", font=("Arial", 14), anchor="e")
Contenedor_transacciones.create_text(390, 150, text="Apellido", fill="white", font=("Arial", 14), anchor="e")
Contenedor_transacciones.create_text(390, 192, text="Rol", fill="white", font=("Arial", 14), anchor="e")

input_transacciones_rut = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_rut.place(x=487, y=234, width=150, height=30)

input_transacciones_nombre = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_nombre.place(x=487, y=278, width=150, height=30)

input_transacciones_apellido = tk.Entry(transac_page, font=('Arial', 12), bg="#333538", fg="white")
input_transacciones_apellido.place(x=735, y=234, width=150, height=30)

option_transacciones_estado = tk.StringVar()
option_transacciones_estado.set("Elige un Rol") # Texto inicial filtro
option_transacciones_estado_opciones = ["Proveedor", "Cliente"]
option_transacciones_estado_menu = tk.OptionMenu(transac_page, option_transacciones_estado, *option_transacciones_estado_opciones)
option_transacciones_estado_menu.config(font=("Arial", 12), bg="#333538", fg="white", highlightthickness=0)
option_transacciones_estado_menu.place(x=735, y=277, width=150, height=30)

btn_nueva_persona = tk.Button(transac_page, text="Nuevo", font=('Arial', 12), bg="#1F68A3", fg="white", command=agregar_nueva_persona)
btn_nueva_persona.place(x=903, y=234, width=150, height=30)
btn_actualizar_persona = tk.Button(transac_page, text="Actualizar", font=('Arial', 12), bg="#1F68A3", fg="white", command=actualizar_registro_persona)
btn_actualizar_persona.place(x=1071, y=234, width=150, height=30)
btn_eliminar_persona = tk.Button(transac_page, text="Eliminar", font=('Arial', 12), bg="#1F68A3", fg="white", command=eliminar_registro_persona)
btn_eliminar_persona.place(x=903, y=278, width=150, height=30)
btn_limpiar_persona = tk.Button(transac_page, text="Limpiar", font=('Arial', 12), bg="#1F68A3", fg="white", command=limpiar_campos_persona)
btn_limpiar_persona.place(x=1071, y=278, width=150, height=30)
