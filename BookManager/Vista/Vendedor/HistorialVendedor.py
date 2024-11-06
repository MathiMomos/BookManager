import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        marco_busqueda.pack(fill="x", pady=(0, 10))

        canvas = tk.Canvas(marco_busqueda, width=500, height=50, bg="white", highlightthickness=0)
        canvas.pack(fill="x", expand=True)

        # Rectangulo redondeado
        self.crear_rectangulo_redondeado(canvas, 10, 10, 490, 40, radio=15, relleno="#E6E6FA", borde="black")

        # Cargar el icono de búsqueda (lupa)
        icono_lupa_path = os.path.join(base_dir, "iconos", "lupa.png")
        self.icono_lupa = ImageTk.PhotoImage(Image.open(icono_lupa_path).resize((24, 24)))
        canvas.create_image(30, 25, image=self.icono_lupa, anchor="center")

        # Cuadro de entrada para búsqueda
        entrada_busqueda = tk.Entry(marco_busqueda, font=("Arial", 12), bd=0, bg="#E6E6FA", fg="grey", width=40)
        entrada_busqueda.insert(0, "Buscar en el historial")

        def on_entry_click(event):
            if entrada_busqueda.get() == "Buscar en el historial":
                entrada_busqueda.delete(0, "end")
                entrada_busqueda.config(fg="black")

        entrada_busqueda.bind("<FocusIn>", on_entry_click)
        canvas.create_window(250, 25, window=entrada_busqueda)

        # Tabla de historial de ventas
        columnas = ("#", "Producto", "Cantidad", "Precio", "Fecha", "Hora")
        tree = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar las columnas
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        # Datos de ejemplo
        historial = [
            ("1", "Cuaderno", "10", "S/. 5", "2024-11-06", "10:30:00"),
            ("2", "Lapicero", "10", "S/. 1", "2024-11-06", "11:15:00"),
            ("3", "Plumones", "2", "S/. 4.50", "2024-11-06", "12:00:00"),
        ]
        for venta in historial:
            tree.insert("", "end", values=venta)

        # Botón de exportar
        boton_exportar = tk.Button(self, text="Exportar historial", bg="green", fg="white", font=("Arial", 12), padx=10, pady=5)
        boton_exportar.pack(pady=10)

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
