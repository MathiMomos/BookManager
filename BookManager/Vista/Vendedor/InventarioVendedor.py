import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from BookManager.Controlador.VendedorControlador import VendedorControlador

class InventarioVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        self.controlador = VendedorControlador()  # Crear una instancia del controlador

        # Ruta base del archivo actual para cargar las imágenes
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Título de la sección
        etiqueta_titulo = tk.Label(self, text="Inventario de productos", font=("Arial", 16), bg="white")
        etiqueta_titulo.pack(pady=20)

        # Marco para la barra de búsqueda
        marco_busqueda = tk.Frame(self, bg="white")
        marco_busqueda.pack(fill="x", pady=(0, 10), padx=10)

        canvas = tk.Canvas(marco_busqueda, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="x", expand=True)

        # Rectángulo redondeado para el cuadro de búsqueda
        self.crear_rectangulo_redondeado(canvas, 10, 10, 490, 40, radio=15, relleno="#E6E6FA", borde="black")

        # Cargar el icono de búsqueda (lupa)
        icono_lupa_path = os.path.join(base_dir, "iconos", "lupa.png")
        self.icono_lupa = ImageTk.PhotoImage(Image.open(icono_lupa_path).resize((24, 24)))
        canvas.create_image(30, 25, image=self.icono_lupa, anchor="center")

        # Cuadro de entrada para búsqueda
        self.entrada_busqueda = tk.Entry(marco_busqueda, font=("Arial", 12), bd=0, bg="#E6E6FA", fg="grey", width=40)
        self.entrada_busqueda.insert(0, "Buscar en el inventario")

        def on_entry_click(event):
            if self.entrada_busqueda.get() == "Buscar en el inventario":
                self.entrada_busqueda.delete(0, "end")
                self.entrada_busqueda.config(fg="black")

        self.entrada_busqueda.bind("<FocusIn>", on_entry_click)
        canvas.create_window(250, 25, window=self.entrada_busqueda)

        # Botón de búsqueda
        boton_buscar = tk.Button(
            marco_busqueda,
            text="Buscar",
            command=self.buscar_producto,
            font=("Arial", 12),
        )
        boton_buscar.pack(side="right", padx=10)

        # Tabla de inventario de productos
        columnas = ("#", "Nombre", "Cantidad", "Precio")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar las columnas
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=120)

        # Llenar la tabla con los productos del inventario desde la base de datos
        self.cargar_inventario()

        # Botón de exportación (opcional)
        boton_exportar = tk.Button(self, text="Exportar inventario", bg="green", fg="white", font=("Arial", 12),
                                   padx=10, pady=5)
        boton_exportar.pack(pady=10)

    def cargar_inventario(self):
        inventario = self.controlador.mostrar_productos()
        if inventario:
            for producto in inventario:
                self.tabla.insert("", "end", values=producto)

    def crear_rectangulo_redondeado(self, canvas, x1, y1, x2, y2, radio=25, relleno="#E6E6FA", borde="black"):
        points = [
            x1 + radio, y1,
            x2 - radio, y1,
            x2, y1, x2, y1 + radio,
            x2, y2 - radio, x2, y2,
            x2 - radio, y2, x1 + radio, y2,
            x1, y2, x1, y2 - radio,
            x1, y1 + radio, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, fill=relleno, outline=borde)

    def buscar_producto(self):
        id_producto = self.entrada_busqueda.get()
        producto = self.controlador.ver_disponibilidad(id_producto)

        if producto:
            cantidad, precio, nombre = producto
            self.mostrar_producto_ventana(nombre, cantidad, precio)
        else:
            self.mostrar_producto_no_encontrado()

    def mostrar_producto_ventana(self, nombre, cantidad, precio):
        # Crear una ventana emergente centrada
        ventana = tk.Toplevel(self)
        ventana.title("Producto Encontrado")
        ventana.geometry("300x200")
        ventana.transient(self)
        ventana.grab_set()  # Para que la ventana sea modal

        # Centrar la ventana en la pantalla
        ventana.update_idletasks()
        width = ventana.winfo_width()
        height = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana.winfo_screenheight() // 2) - (height // 2)
        ventana.geometry(f"{width}x{height}+{x}+{y}")

        # Etiqueta con la información del producto
        etiqueta_info = tk.Label(ventana, text="Este es el producto buscado:", font=("Arial", 14))
        etiqueta_info.pack(pady=10)
        etiqueta_producto = tk.Label(ventana, text=f"Nombre: {nombre}\nCantidad: {cantidad}\nPrecio: S/. {precio}",
                                     font=("Arial", 12))
        etiqueta_producto.pack(pady=10)

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
        boton_cerrar.pack(pady=10)

    def mostrar_producto_no_encontrado(self):
        # Crear una ventana emergente de aviso
        messagebox.showinfo("Producto no encontrado", "El producto con el ID ingresado no existe en el inventario.")
