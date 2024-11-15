import os
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
from BookManager.Vista.Vendedor.InicioVendedor import InicioVendedor
from BookManager.Vista.Vendedor.InventarioVendedor import InventarioVendedor
from BookManager.Vista.Vendedor.HistorialVendedor import HistorialVendedor


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
            command=self.volver_a_login
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

    def volver_a_login(self):
        self.destroy()  # Cierra la ventana actual
        from BookManager.Vista.Login import Login  # Importación diferida para evitar circularidad
        login_app = Login()  # Crea una nueva instancia de Login
        login_app.mainloop()  # Muestra la ventana de Login

    def create_vender_frame(self, parent):
        frame = tk.Frame(parent, bg="white")

        # Barra de búsqueda con diseño redondeado
        search_frame = tk.Frame(frame, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))

        canvas = tk.Canvas(search_frame, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(fill="x", expand=True)

        # Llamar a la función para crear un rectángulo redondeado
        self.create_rounded_rectangle(canvas, 10, 10, 490, 40, radius=15, fill="#E6E6FA", outline="black")

        # Cargar el icono de búsqueda
        self.search_icon = ImageTk.PhotoImage(
            Image.open(os.path.join(self.base_dir, "iconos", "lupa.png")).resize((24, 24)))
        canvas.create_image(30, 25, image=self.search_icon, anchor="center")

        # Crear el cuadro de entrada
        search_entry = tk.Entry(search_frame, font=("Arial", 12), bd=0, bg="#E6E6FA", fg="grey", width=40)
        search_entry.insert(0, "Ingresa el ID del producto")

        def on_entry_click(event):
            if search_entry.get() == "Ingresa el ID del producto":
                search_entry.delete(0, "end")
                search_entry.config(fg="black")

        search_entry.bind("<FocusIn>", on_entry_click)
        canvas.create_window(250, 25, window=search_entry)

        # Tabla de productos con más columnas
        columns = ("#", "Descripción", "Cantidad", "Precio", "Total", "Unidades")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        tree.pack(fill="both", expand=True)

        # Cambiar fuente y tamaño de las columnas
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        # Datos de ejemplo
        productos = [
            ("1", "Cuaderno", "10", "S/. 5", "S/. 50"),
            ("2", "Lapicero", "10", "S/. 1", "S/. 10"),
            ("3", "Plumones", "2", "S/. 4.50", "S/. 9"),
        ]
        for producto in productos:
            tree.insert("", "end", values=producto)

        # Aumentar el alto de las filas
        style.configure("Treeview", rowheight=30)

        # Botón de confirmación
        confirm_frame = tk.Frame(frame, bg="white")
        confirm_frame.pack(fill="x", pady=10)

        carrito_button = tk.Button(
            confirm_frame,
            text="Carrito de compras",
            image=self.icons.get("Carrito"),
            compound="left",
            bg=self.default_menu_color,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.menu_font
        )
        carrito_button.pack(side="left", padx=10)

        confirm_button = tk.Button(
            confirm_frame, text="Confirmar compra y generar ticket",
            bg="green", fg="white", padx=10, pady=5,
            font=("Arial", 12)
        )
        confirm_button.pack(side="right")

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