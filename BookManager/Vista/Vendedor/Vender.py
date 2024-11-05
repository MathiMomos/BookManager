import os
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
from BookManager.BookManager.Vista.Vendedor.InicioVendedor import InicioVendedor
from BookManager.BookManager.Vista.Vendedor.InventarioVendedor import InventarioVendedor
from BookManager.BookManager.Vista.Vendedor.HistorialVendedor import HistorialVendedor

class Vender(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Librería La Hoja - Vender")

        # Establecer el tamaño de la ventana
        window_width = 1000
        window_height = 600
        self.geometry(f"{window_width}x{window_height}")

        # Calcular la posición x, y para centrar la ventana en la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)

        # Centrar la ventana en la pantalla
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.configure(bg="white")

        # Colores de los botones de menú
        self.default_menu_color = "#e0e0e0"
        self.active_menu_color = "#d0d0ff"

        # Aumenta el tamaño de la fuente del menú
        self.menu_font = font.Font(family="Arial", size=12, weight="bold")

        # Directorio base del proyecto
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargar los íconos
        icon_paths = {
            "Inicio": os.path.join(self.base_dir, "iconos", "casa.png"),
            "Vender": os.path.join(self.base_dir, "iconos", "carrito-de-compras.png"),
            "Historial de ventas": os.path.join(self.base_dir, "iconos", "notas.png"),
            "Ver inventario": os.path.join(self.base_dir, "iconos", "caja.png"),
            "Salir": os.path.join(self.base_dir, "iconos", "salir.png"),
            "Carrito": os.path.join(self.base_dir, "iconos", "carrito-de-compras.png"),
        }

        self.icons = {}
        for key, path in icon_paths.items():
            if os.path.exists(path):
                self.icons[key] = ImageTk.PhotoImage(Image.open(path).resize((24, 24)))
            else:
                print(f"Error: El archivo de ícono '{path}' no existe.")
                self.icons[key] = None

        # Menú lateral
        self.menu_frame = tk.Frame(self, bg=self.default_menu_color)
        self.menu_frame.pack(side="left", fill="y")

        # Frame para centrar los botones
        self.button_frame = tk.Frame(self.menu_frame, bg=self.default_menu_color)
        self.button_frame.pack(expand=True)

        # Menú de opciones
        menu_items = ["Inicio", "Vender", "Historial de ventas", "Ver inventario"]
        self.menu_buttons = {}

        for item in menu_items:
            button = tk.Button(
                self.button_frame,
                text=item,
                image=self.icons.get(item),
                compound="left",
                bg=self.default_menu_color,
                relief="flat",
                anchor="w",
                padx=20,
                font=self.menu_font,
                command=lambda i=item: self.cambiar_pestaña(i)
            )
            button.pack(fill="x", pady=5, ipady=5, anchor="center")
            self.menu_buttons[item] = button

        # Botón de salir
        salir_button = tk.Button(
            self.menu_frame,
            text="Salir",
            image=self.icons.get("Salir"),
            compound="left",
            bg=self.default_menu_color,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.menu_font,
            command=self.quit
        )
        salir_button.pack(side="bottom", fill="x", pady=5, ipady=5)

        # Contenedor principal
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Crear los frames para cada sección
        self.frames = {}
        self.frames["Inicio"] = InicioVendedor(self.main_frame)
        self.frames["Vender"] = self.create_vender_frame(self.main_frame)
        self.frames["Historial de ventas"] = HistorialVendedor(self.main_frame)
        self.frames["Ver inventario"] = InventarioVendedor(self.main_frame)

        # Mostrar la pestaña "Inicio" al inicio
        self.cambiar_pestaña("Inicio")

    def cambiar_pestaña(self, pestaña):
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Mostrar el frame correspondiente
        self.frames[pestaña].pack(fill="both", expand=True)

        # Restaurar el color de todas las pestañas
        for item, button in self.menu_buttons.items():
            button.config(bg=self.default_menu_color)

        # Cambiar el color de la pestaña activa
        if pestaña in self.menu_buttons:
            self.menu_buttons[pestaña].config(bg=self.active_menu_color)

    def create_vender_frame(self, parent):
        frame = tk.Frame(parent, bg="white")

        # Aquí va el contenido del frame de "Vender"

        return frame

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Función para crear un rectángulo con bordes redondeados en el canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
