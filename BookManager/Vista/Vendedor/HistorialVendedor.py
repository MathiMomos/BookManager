import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from BookManager.BookManager.Controlador.VendedorControlador import VendedorControlador  # Importar el controlador

class HistorialVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        # Ruta base del archivo actual para cargar las imágenes
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Titulo de la sección
        label = tk.Label(self, text="Historial de ventas", font=("Arial", 16), bg="white")
        label.pack(pady=20)

        # Marco para la barra de búsqueda
        marco_busqueda = tk.Frame(self, bg="white")
        marco_busqueda.pack(fill="x", pady=(0, 10), padx=10)

        canvas = tk.Canvas(marco_busqueda, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="x", expand=True)

        # Rectangulo redondeado
        self.crear_rectangulo_redondeado(canvas, 10, 10, 490, 40, radio=15, relleno="#E6E6FA", borde="black")

        # Cargar el icono de búsqueda (lupa)
        icono_lupa_path = os.path.join(base_dir, "iconos", "lupa.png")
        self.icono_lupa = ImageTk.PhotoImage(Image.open(icono_lupa_path).resize((24, 24)))
        canvas.create_image(30, 25, image=self.icono_lupa, anchor="center")

        # Cuadro de entrada para búsqueda
        self.entrada_busqueda = tk.Entry(marco_busqueda, font=("Arial", 12), bd=0, bg="#E6E6FA", fg="grey", width=40)
        self.entrada_busqueda.insert(0, "Buscar en el historial")

        def on_entry_click(event):
            if self.entrada_busqueda.get() == "Buscar en el historial":
                self.entrada_busqueda.delete(0, "end")
                self.entrada_busqueda.config(fg="black")

        self.entrada_busqueda.bind("<FocusIn>", on_entry_click)
        self.entrada_busqueda.bind("<Return>", self.buscar_por_id)  # Buscar al presionar Enter
        canvas.create_window(250, 25, window=self.entrada_busqueda)

        # Botón para mostrar todo
        boton_mostrar_todo = tk.Button(marco_busqueda, text="Mostrar todo", command=self.mostrar_todo, bg="#d3d3d3", fg="black", font=("Arial", 12), padx=10, pady=5)
        boton_mostrar_todo.pack(side="right", padx=5)

        # Tabla de historial de ventas
        columnas = ("#", "Producto", "Precio Unitario", "Cantidad", "Precio Total", "Fecha", "Hora")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar las columnas
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Instanciar el controlador y cargar el historial de ventas
        self.controlador = VendedorControlador()
        self.cargar_historial_ventas()

        # Botón de exportar
        boton_exportar = tk.Button(self, text="Exportar historial", bg="green", fg="white", font=("Arial", 12), padx=10, pady=5)
        boton_exportar.pack(pady=10)

    def cargar_historial_ventas(self):
        historial = self.controlador.ver_historial_ventas() or []  # Asegurarse de que siempre sea una lista
        if historial:
            for venta in historial:
                self.tree.insert("", "end", values=venta)
        else:
            print("No se encontraron ventas en el historial")

    def buscar_por_id(self, event):
        buscar_id = self.entrada_busqueda.get().strip()
        if not buscar_id.isdigit():
            return

        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrar las ventas por ID
        historial = self.controlador.ver_historial_ventas() or []
        for venta in historial:
            if str(venta[0]) == buscar_id:
                self.tree.insert("", "end", values=venta)

    def mostrar_todo(self):
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Volver a cargar todas las ventas
        self.cargar_historial_ventas()

    def crear_rectangulo_redondeado(self, canvas, x1, y1, x2, y2, radio=25, relleno="#E6E6FA", borde="black"):
        """Función para crear un rectángulo con bordes redondeados en el canvas."""
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
