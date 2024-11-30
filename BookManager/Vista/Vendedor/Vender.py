import os
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
from BookManager.BookManager.Vista.Vendedor.InicioVendedor import InicioVendedor
from BookManager.BookManager.Vista.Vendedor.InventarioVendedor import InventarioVendedor
from BookManager.BookManager.Vista.Vendedor.HistorialVendedor import HistorialVendedor
from BookManager.BookManager.Vista.Vendedor.CarritoCompra import CarritoCompra
from BookManager.BookManager.Controlador.VendedorControlador import VendedorControlador

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
            command=self.volver_a_login # Llama a la función para volver al login
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

        # Mostrar la pestaña "Inicio" al loguearse
        self.cambiar_pestaña("Inicio")

        # Inicializar controlador
        self.vendedor_controlador = VendedorControlador()

        self.carrito_compras = []  # Lista para almacenar los productos seleccionados para el carrito
        self.mostrar_productos() # Llama a la función para mostrar los productos

    def cambiar_pestaña(self, pestaña):
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget() # Para ocultar el frame

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
        from BookManager.BookManager.Vista.Login import Login  # Importación diferida para evitar circularidad
        login_app = Login()  # Crea una nueva instancia de Login
        login_app.mainloop()  # Muestra la ventana de Login

    #CONTENIDO PARA VENDER
    def create_vender_frame(self, parent):
        frame = tk.Frame(parent, bg="white")

        # Barra de búsqueda con diseño redondeado
        search_frame = tk.Frame(frame, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))

        canvas = tk.Canvas(search_frame, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(fill="x", expand=True)

        # Llamar a la función para crear un rectángulo redondeado
        self.rectangulo_busqueda(canvas, 10, 10, 490, 40, radius=15, fill="#E6E6FA", outline="black")

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

        search_entry.bind("<FocusIn>", on_entry_click) # Llama a la función on_entry_click al hacer clic en el cuadro de entrada
        canvas.create_window(250, 25, window=search_entry)

        # Entrada para cantidad a vender
        cantidad_frame = tk.Frame(frame, bg="white") # Frame para la cantidad
        cantidad_frame.pack(fill="x", pady=5)
        self.cantidad_label = tk.Label(cantidad_frame, text="Cantidad a vender:", font=("Arial", 12), bg="white")
        self.cantidad_label.pack(side="left", padx=10)
        self.cantidad_entry = tk.Entry(cantidad_frame, font=("Arial", 12), width=10)
        self.cantidad_entry.pack(side="left", padx=10)

        # Tabla de productos con más columnas
        columns = ("#", "Descripción", "Cantidad", "Precio", "Total")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=8, selectmode="browse") # Para crear la tabla
        self.tree.pack(fill="both", expand=True) # Para expandir la tabla

        # Configurar columnas
        self.tree.heading("#", text="#")
        self.tree.column("#", anchor="center", width=50)
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Descripción", anchor="center", width=150)
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.heading("Precio", text="Precio")
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", anchor="center", width=100)

        # Cambiar fuente y tamaño de las columnas
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        # Aumentar el alto de las filas
        style.configure("Treeview", rowheight=30)

        # Botones de acción
        action_frame = tk.Frame(frame, bg="white")
        action_frame.pack(fill="x", pady=10)

        # Botón para agregar a carrito
        agregar_carrito_button = tk.Button(
            action_frame,
            text="Agregar a carrito",
            bg="#FFA500",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 12),
            command=self.agregar_a_carrito
        )
        agregar_carrito_button.pack(side="left", padx=10)

        # Botón para abrir el carrito de compras
        carrito_button = tk.Button(
            action_frame,
            text="Carrito de compras",
            image=self.icons.get("Carrito"),
            compound="left",
            bg=self.default_menu_color,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.menu_font, # Usa la fuente del menú
            command=self.abrir_carrito_compras
        )
        carrito_button.pack(side="left", padx=10)

        # Botón para confirmar la compra
        confirm_button = tk.Button(
            action_frame, text="Confirmar compra y generar ticket",
            bg="green", fg="white", padx=10, pady=5,
            font=("Arial", 12),
            command=self.confirmar_compra
        )
        confirm_button.pack(side="right")

        return frame

    def agregar_a_carrito(self):
        # Obtener el producto seleccionado
        selected_item = self.tree.selection() # Para obtener los elementos seleccionados
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Por favor, selecciona un producto de la tabla.")
            return

        # Obtener la cantidad ingresada
        cantidad = self.cantidad_entry.get()
        if not cantidad.isdigit() or int(cantidad) <= 0:
            tk.messagebox.showwarning("Advertencia", "Por favor, ingresa una cantidad válida.")
            return

        # Obtener los datos del producto seleccionado
        producto = self.tree.item(selected_item, "values") # Tupla con los valores de la fila seleccionada
        descripcion = producto[1]
        precio = float(producto[3].replace('S/. ', '').strip())
        total = int(cantidad) * precio

        # Añadir el producto al carrito de compras
        self.carrito_compras.append((descripcion, cantidad, f"S/. {total:.2f}")) # Es una lista : carrito_compras
        tk.messagebox.showinfo("Producto agregado", f"{cantidad} unidades de '{descripcion}' agregado al carrito.")

    def confirmar_compra(self):
        if not self.carrito_compras:
            tk.messagebox.showwarning("Advertencia", "El carrito de compras está vacío.")
            return

        for producto in self.carrito_compras:
            descripcion, cantidad, total = producto
            id_producto = self.obtener_id_producto(descripcion)
            if id_producto is None:
                tk.messagebox.showwarning("Error", f"No se encontró el producto '{descripcion}' en el inventario.")
                continue

            cantidad = int(cantidad)

            # Llamar a la función vender_producto del controlador
            venta_exitosa = self.vendedor_controlador.vender_producto(id_producto, cantidad)

            if venta_exitosa:
                # Mostrar ventana emergente
                ventana_emergente = tk.Toplevel(self)
                ventana_emergente.title("Venta generada")
                ventana_emergente.geometry("300x150")
                ventana_emergente.transient(self)
                ventana_emergente.grab_set()
                ventana_emergente.configure(bg="white")
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                position_x = int((screen_width - 300) / 2)
                position_y = int((screen_height - 150) / 2)
                ventana_emergente.geometry(f"300x150+{position_x}+{position_y}")

                # Icono y mensaje
                icon_path = os.path.join(self.base_dir, "iconos", "comprobado.png")
                icon = ImageTk.PhotoImage(Image.open(icon_path).resize((50, 50)))
                tk.Label(ventana_emergente, image=icon, bg="white").pack(pady=10)
                tk.Label(ventana_emergente, text="Venta generada", font=("Arial", 14), bg="white").pack()

                # Mantener referencia del icono
                ventana_emergente.icon = icon

                # Cerrar ventana emergente después de 3 segundos
                def cerrar_ventana():
                    ventana_emergente.destroy()

                self.after(3000, cerrar_ventana)
            else:
                tk.messagebox.showwarning("Error", f"No se pudo realizar la venta del producto '{descripcion}'. Verifica el stock disponible.")

    def obtener_id_producto(self, descripcion):
        # Buscar el producto en la tabla de productos para obtener su ID
        for item in self.tree.get_children():
            producto = self.tree.item(item, "values")
            if producto[1] == descripcion:
                return producto[0]
        return None

    def abrir_carrito_compras(self):
        carrito = CarritoCompra(self) # Crea una nueva ventana de carrito de compras
        # Limpiar la tabla del carrito
        for item in carrito.tree.get_children():
            carrito.tree.delete(item)

        # Añadir los productos seleccionados al carrito
        for producto in self.carrito_compras:
            carrito.tree.insert("", "end", values=producto)

        carrito.grab_set()  # Hacer la ventana modal, acepta entradas como clics y teclas
        carrito.mainloop() # Para q no se cierre inmediatamente la ventana

    def rectangulo_busqueda(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
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

    def mostrar_productos(self):
        # Limpiar la tabla antes de agregar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener los productos del controlador
        productos = self.vendedor_controlador.mostrar_productos()

        # Insertar los productos en la tabla
        for producto in productos:
            id_producto, nombre, cantidad, precio = producto
            total = cantidad * float(precio)
            self.tree.insert("", "end", values=(id_producto, nombre, cantidad, f"S/. {precio}", f"S/. {total}"))

