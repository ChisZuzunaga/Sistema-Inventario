
# Sistema de inventario

Este es un sistema de inventario basado en Python con una interfaz gráfica desarrollada en Tkinter. Permite gestionar productos, generar reportes en PDF, realizar copias de seguridad y visualizar datos de manera sencilla.



## Características principales
- ✅ Interfaz gráfica intuitiva con Tkinter
- ✅ Base de datos local con SQLite
- ✅ Generación de reportes en Excel (XlsxWriter) y PDF (FPDF, ReportLab)
- ✅ Visualización de datos con Matplotlib
- ✅ Gestión de imágenes con Pillow
- ✅ Creación de copias de seguridad
## Requisitos e instalación

Para ejecutar el programa, primero instala las dependencias necesarias con:

```pip pandas fpdf pillow matplotlib reportlab install XlsxWriter openpyxl pyinstaller```

Si necesitas ejecutar el programa en otro entorno o máquina, asegúrate de instalar Python 3.x y las dependencias anteriores.

## Ejecución del programa
Para ejecutar el programa directamente desde Python, usa:

```python gui.py```

Si deseas convertirlo en un ejecutable independiente, usa el siguiente comando:

```pyinstaller --onefile --noconsole --add-data "Img;Img" --add-data "Copias-De-Seguridad;Copias-De-Seguridad" --add-data "productos.db;." --icon=icon.ico gui.py```

### Explicación de los parámetros:

```
--onefile: Genera un único archivo .exe para mayor portabilidad.
--noconsole: Oculta la consola (ideal para aplicaciones GUI).
--add-data: Incluye archivos y carpetas necesarias para el funcionamiento.
--icon=icon.ico: Especifica un icono personalizado para el ejecutable.
```
Una vez generado, el archivo ejecutable estará en la carpeta dist/ y podrás ejecutarlo sin necesidad de instalar Python. **Aunque probablemente debas copiar la carpeta *Img* dentro de la carpeta *dist/***

## Estructura del proyecto

```
📂 Sistema-Inventario  
 ├── 📂 Img                     # Imágenes de los productos  
 ├── 📂 Copias-De-Seguridad     # Carpeta de backups automáticos  
 ├── 📜 gui.py                  # Archivo principal con la interfaz gráfica  
 ├── 📜 productos.db            # Base de datos SQLite  
 ├── 📜 README.md               # Documento con información del proyecto  
 ├── 📜 icon.ico                # Icono de la aplicación  
 ```