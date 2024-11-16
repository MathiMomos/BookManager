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
        ancho_ventana = 1000
        alto_ventana = 600
        self.geometry(f"{ancho_ventana}x{alto_ventana}")

        # Calcular la posición x, y para centrar la ventana en la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        posicion_x = int((ancho_pantalla - ancho_ventana) / 2)
        posicion_y = int((alto_pantalla - alto_ventana) / 2)

        # Centrar la ventana en la pantalla
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
        self.configure(bg="white")

        # Colores de los botones de menú
        self.color_menu_predeterminado = "#e0e0e0"
        self.color_menu_activo = "#d0d0ff"

        # Aumenta el tamaño de la fuente del menú
        self.fuente_menu = font.Font(family="Arial", size=12, weight="bold")

        # Directorio base del proyecto
        self.directorio_base = os.path.dirname(os.path.abspath(__file__))

        # Cargar los íconos
        rutas_iconos = {
            "Inicio": os.path.join(self.directorio_base, "iconos", "casa.png"),
            "Vender": os.path.join(self.directorio_base, "iconos", "carrito-de-compras.png"),
            "Historial de ventas": os.path.join(self.directorio_base, "iconos", "notas.png"),
            "Ver inventario": os.path.join(self.directorio_base, "iconos", "caja.png"),
            "Salir": os.path.join(self.directorio_base, "iconos", "salir.png"),
            "Carrito": os.path.join(self.directorio_base, "iconos", "carrito-de-compras.png"),
        }

        self.icons = {}
        for key, path in rutas_iconos.items():
            if os.path.exists(path):
                self.icons[key] = ImageTk.PhotoImage(Image.open(path).resize((24, 24)))
            else:
                print(f"Error: El archivo de ícono '{path}' no existe.")
                self.icons[key] = None

        # Menú lateral
        self.marco_menu = tk.Frame(self, bg=self.color_menu_predeterminado)
        self.marco_menu.pack(side="left", fill="y")

        # Frame para centrar los botones
        self.marco_botones = tk.Frame(self.marco_menu, bg=self.color_menu_predeterminado)
        self.marco_botones.pack(expand=True)

        # Menú de opciones
        elementos_menu = ["Inicio", "Vender", "Historial de ventas", "Ver inventario"]
        self.botones_menu = {}

        for item in elementos_menu:
            button = tk.Button(
                self.marco_botones,
                text=item,
                image=self.icons.get(item),
                compound="left",
                bg=self.color_menu_predeterminado,
                relief="flat",
                anchor="w",
                padx=20,
                font=self.fuente_menu,
                command=lambda i=item: self.cambiar_pestaña(i)
            )
            button.pack(fill="x", pady=5, ipady=5, anchor="center")
            self.botones_menu[item] = button

        # Botón de salir
        salir_button = tk.Button(
            self.marco_menu,
            text="Salir",
            image=self.icons.get("Salir"),
            compound="left",
            bg=self.color_menu_predeterminado,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.fuente_menu,
            command=self.volver_a_login
        )
        salir_button.pack(side="bottom", fill="x", pady=5, ipady=5)

        # Contenedor principal
        self.marco_principal = tk.Frame(self, bg="white")
        self.marco_principal.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Crear los frames para cada sección
        self.frames = {}
        self.frames["Inicio"] = InicioVendedor(self.marco_principal)
        self.frames["Vender"] = self.create_vender_frame(self.marco_principal)
        self.frames["Historial de ventas"] = HistorialVendedor(self.marco_principal)
        self.frames["Ver inventario"] = InventarioVendedor(self.marco_principal)

        # Mostrar la pestaña "Inicio" al inicio
        self.cambiar_pestaña("Inicio")

        # Inicializar controlador
        self.vendedor_controlador = VendedorControlador()
        self.carrito_productos = []  # Lista para almacenar los lista_productos seleccionados para el carrito
        self.mostrar_productos()

    def cambiar_pestaña(self, pestaña):
        # Ocultar todos los frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Mostrar el frame correspondiente
        self.frames[pestaña].pack(fill="both", expand=True)

        # Restaurar el color de todas las pestañas
        for item, button in self.botones_menu.items():
            button.config(bg=self.color_menu_predeterminado)

        # Cambiar el color de la pestaña activa
        if pestaña in self.botones_menu:
            self.botones_menu[pestaña].config(bg=self.color_menu_activo)

    def volver_a_login(self):
        self.destroy()  # Cierra la ventana actual
        from BookManager.BookManager.Vista.Login import Login  # Importación diferida para evitar circularidad
        login_app = Login()  # Crea una nueva instancia de Login
        login_app.mainloop()  # Muestra la ventana de Login

    def create_vender_frame(self, parent):
        frame = tk.Frame(parent, bg="white")

        # Barra de búsqueda con diseño redondeado
        marco_busqueda = tk.Frame(frame, bg="white")
        marco_busqueda.pack(fill="x", pady=(0, 10))

        canvas = tk.Canvas(marco_busqueda, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(fill="x", expand=True)

        # Llamar a la función para crear un rectángulo redondeado
        self.create_rounded_rectangle(canvas, 10, 10, 490, 40, radius=15, fill="#E6E6FA", outline="black")

        # Cargar el icono de búsqueda
        self.icono_busqueda = ImageTk.PhotoImage(
            Image.open(os.path.join(self.directorio_base, "iconos", "lupa.png")).resize((24, 24)))
        canvas.create_image(30, 25, image=self.icono_busqueda, anchor="center")

        # Crear el cuadro de entrada
        entrada_busqueda = tk.Entry(marco_busqueda, font=("Arial", 12), bd=0, bg="#E6E6FA", fg="grey", width=40)
        entrada_busqueda.insert(0, "Ingresa el ID del producto")

        def on_entry_click(event):
            if entrada_busqueda.get() == "Ingresa el ID del producto":
                entrada_busqueda.delete(0, "end")
                entrada_busqueda.config(fg="black")

        entrada_busqueda.bind("<FocusIn>", on_entry_click)
        canvas.create_window(250, 25, window=entrada_busqueda)

        # Entry para cantidad a vender
        marco_cantidad = tk.Frame(frame, bg="white")
        marco_cantidad.pack(fill="x", pady=5)
        self.cantidad_label = tk.Label(marco_cantidad, text="Cantidad a vender:", font=("Arial", 12), bg="white")
        self.cantidad_label.pack(side="left", padx=10)
        self.cantidad_entry = tk.Entry(marco_cantidad, font=("Arial", 12), width=10)
        self.cantidad_entry.pack(side="left", padx=10)

        # Tabla de lista_productos con más columnas
        columns = ("#", "Descripción", "Cantidad", "Precio", "Total")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=8, selectmode="browse")
        self.tree.pack(fill="both", expand=True)

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
        marco_accion = tk.Frame(frame, bg="white")
        marco_accion.pack(fill="x", pady=10)

        boton_agregar_carrito = tk.Button(
            marco_accion,
            text="Agregar a carrito",
            bg="#FFA500",
            fg="white",
            padx=10,
            pady=5,
            font=("Arial", 12),
            command=self.agregar_a_carrito
        )
        boton_agregar_carrito.pack(side="left", padx=10)

        boton_carrito = tk.Button(
            marco_accion,
            text="Carrito de compras",
            image=self.icons.get("Carrito"),
            compound="left",
            bg=self.color_menu_predeterminado,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.fuente_menu,
            command=self.abrir_carrito_compras
        )
        boton_carrito.pack(side="left", padx=10)

        boton_confirmar = tk.Button(
            marco_accion, text="Confirmar compra y generar ticket",
            bg="green", fg="white", padx=10, pady=5,
            font=("Arial", 12),
            command=self.confirmar_compra
        )
        boton_confirmar.pack(side="right")

        return frame

    def agregar_a_carrito(self):
        # Obtener el producto seleccionado
        elemento_seleccionado = self.tree.selection()
        if not elemento_seleccionado:
            tk.messagebox.showwarning("Advertencia", "Por favor, selecciona un producto de la tabla.")
            return

        # Obtener la cantidad ingresada
        cantidad = self.cantidad_entry.get()
        if not cantidad.isdigit() or int(cantidad) <= 0:
            tk.messagebox.showwarning("Advertencia", "Por favor, ingresa una cantidad válida.")
            return

        # Obtener los datos del producto seleccionado
        producto = self.tree.item(elemento_seleccionado, "values")
        descripcion = producto[1]
        precio = float(producto[3].replace('S/. ', '').strip())
        total = int(cantidad) * precio

        # Añadir el producto al carrito de compras
        self.carrito_productos.append((descripcion, cantidad, f"S/. {total:.2f}"))
        tk.messagebox.showinfo("Producto agregado", f"{cantidad} unidades de '{descripcion}' agregado al carrito.")

    def confirmar_compra(self):
        if not self.carrito_productos:
            tk.messagebox.showwarning("Advertencia", "El carrito de compras está vacío.")
            return

        ventas_exitosas = []

        for producto in self.carrito_productos:
            descripcion, cantidad, total = producto
            id_producto = self.obtener_id_producto(descripcion)
            if id_producto is None:
                tk.messagebox.showwarning("Error", f"No se encontró el producto '{descripcion}' en el inventario.")
                continue

            cantidad = int(cantidad)

            # Llamar a la función vender_producto del controlador
            venta_realizada = self.vendedor_controlador.vender_producto(id_producto, cantidad)

            if venta_realizada:
                ventas_exitosas.append(descripcion)
            else:
                tk.messagebox.showwarning("Error",
                                          f"No se pudo realizar la venta del producto '{descripcion}'. Verifica el stock disponible.")

        # Mostrar la ventana emergente solo una vez, si hubo ventas exitosas
        if ventas_exitosas:
            ventana_popup = tk.Toplevel(self)
            ventana_popup.title("Venta generada")
            ventana_popup.geometry("300x150")
            ventana_popup.transient(self)
            ventana_popup.grab_set()
            ventana_popup.configure(bg="white")
            ancho_pantalla = self.winfo_screenwidth()
            alto_pantalla = self.winfo_screenheight()
            posicion_x = int((ancho_pantalla - 300) / 2)
            posicion_y = int((alto_pantalla - 150) / 2)
            ventana_popup.geometry(f"300x150+{posicion_x}+{posicion_y}")

            # Icono y mensaje
            ruta_icono = os.path.join(self.directorio_base, "iconos", "comprobado.png")
            icon = ImageTk.PhotoImage(Image.open(ruta_icono).resize((50, 50)))
            tk.Label(ventana_popup, image=icon, bg="white").pack(pady=10)
            tk.Label(ventana_popup, text="Venta generada", font=("Arial", 14), bg="white").pack()

            # Mantener referencia del icono
            ventana_popup.icon = icon

            # Cerrar ventana emergente después de 3 segundos
            def cerrar_ventana():
                ventana_popup.destroy()

            self.after(3000, cerrar_ventana)

        # Vaciar el carrito después de procesar todas las ventas
        self.carrito_productos = []

    def obtener_id_producto(self, descripcion):
        # Buscar el producto en la tabla de lista_productos para obtener su ID
        for item in self.tree.get_children():
            producto = self.tree.item(item, "values")
            if producto[1] == descripcion:
                return producto[0]
        return None

    def abrir_carrito_compras(self):
        carrito = CarritoCompra(self)
        # Limpiar la tabla del carrito
        for item in carrito.tree.get_children():
            carrito.tree.delete(item)

        # Añadir los lista_productos seleccionados al carrito
        for producto in self.carrito_productos:
            carrito.tree.insert("", "end", values=producto)

        carrito.grab_set()  # Hacer la ventana modal
        carrito.mainloop()

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

    def mostrar_productos(self):
        # Limpiar la tabla antes de agregar nuevos datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener los lista_productos del controlador
        lista_productos = self.vendedor_controlador.mostrar_productos()

        # Insertar los lista_productos en la tabla
        for producto in lista_productos:
            id_producto, nombre, cantidad, precio = producto
            total = cantidad * float(precio)
            self.tree.insert("", "end", values=(id_producto, nombre, cantidad, f"S/. {precio}", f"S/. {total}"))


