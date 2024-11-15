import os
import tkinter as tk
from PIL import Image, ImageTk

class InicioVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        # Obtener la ruta absoluta de la carpeta donde se encuentra InicioVendedor.py
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Crear el marco principal para organizar los widgets
        marco_principal = tk.Frame(self, bg="#f0f2fa")
        marco_principal.pack(expand=True, padx=10, pady=10)

        # Crear los tres paneles de opciones con rutas absolutas
        self.crear_panel_opcion(marco_principal, "Vender producto", os.path.join(self.base_dir, "iconos", "vender.png"), 0, 0, columnspan=2)
        self.crear_panel_opcion(marco_principal, "Ver inventario", os.path.join(self.base_dir, "iconos", "inventario.png"), 1, 0)
        self.crear_panel_opcion(marco_principal, "Ver historial de ventas", os.path.join(self.base_dir, "iconos", "documentos.png"), 1, 1)

    def crear_panel_opcion(self, parent, text, icon_path, row, column, columnspan=1):
        # Crear marco para cada opción con un tamaño mayor
        option_frame = tk.Frame(parent, bg="#dfe1e8", width=300, height=180)  # Aumenta el tamaño del marco
        option_frame.grid(row=row, column=column, columnspan=columnspan, padx=15, pady=15, sticky="nsew")
        option_frame.grid_propagate(False)  # Para que el marco mantenga su tamaño

        # Cargar y redimensionar el icono a un tamaño mayor
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
            image = image.resize((100, 100), Image.LANCZOS)  # Redimensionar a 100x100 píxeles
            icon = ImageTk.PhotoImage(image)
            icon_label = tk.Label(option_frame, image=icon, bg="#dfe1e8")
            icon_label.image = icon  # Guardar una referencia para evitar que la imagen sea recolectada por el recolector de basura
            icon_label.pack(pady=(20, 10), expand=True, anchor="center")  # Centrar la imagen con mayor espacio superior
        else:
            print(f"Error: No se encontró el archivo de icono en la ruta '{icon_path}'")
            icon_label = tk.Label(option_frame, text="(Icono)", bg="#dfe1e8")
            icon_label.pack(pady=5, expand=True, anchor="center")

        # Etiqueta con el texto, centrada debajo de la imagen y con fuente más grande
        text_label = tk.Label(option_frame, text=text, bg="#dfe1e8",
                              font=("Arial", 16, "bold"))  # Aumenta el tamaño de la fuente
        text_label.pack(pady=(0, 20), expand=True, anchor="center")  # Centrar el texto con mayor espacio inferior

        # Asegurar que el marco principal se expanda para llenar el espacio disponible
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(column, weight=1)