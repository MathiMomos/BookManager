import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CarritoCompra(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Carrito de compras")
        self.geometry("400x450")

        # Centrar la ventana
        self.transient(parent)
        self.grab_set()
        self.configure(bg="white")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_x = int((screen_width - 400) / 2)
        position_y = int((screen_height - 450) / 2)
        self.geometry(f"400x450+{position_x}+{position_y}")

        # Icono del carrito de compras
        self.icon_path = "Vendedor/iconos/carrito-de-compras.png"
        self.icon = ImageTk.PhotoImage(Image.open(self.icon_path).resize((24, 24)))
        tk.Label(self, image=self.icon, bg="white").pack(pady=10)

        # Título de la ventana
        tk.Label(self, text="Carrito de compras", font=("Arial", 16), bg="white").pack(pady=10)

        # Crear una tabla para el carrito de compras con scroll
        columns = ("Producto", "Unidades", "Total")
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)
        self.tree.pack(side="left", fill="both", expand=True)

        # Barra de scroll vertical
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Configurar las columnas
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", anchor="center", width=100)
        self.tree.heading("Unidades", text="Unidades")
        self.tree.column("Unidades", anchor="center", width=100)
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", anchor="center", width=100)

        # Añadir un ejemplo de producto al carrito
        productos = [
            ("Lapicero", "5", "S/. 25.00"),
            ("Cuaderno", "3", "S/. 15.00"),
        ]
        for producto in productos:
            self.tree.insert("", "end", values=producto)

        # Botón para eliminar una fila seleccionada
        eliminar_button = tk.Button(self, text="Eliminar producto", command=self.eliminar_producto, bg="red",
                                    fg="white", font=("Arial", 12))
        eliminar_button.pack(pady=5)

        # Botón para cerrar la ventana
        cerrar_button = tk.Button(self, text="Guardar cambios", command=self.destroy, bg="#FFA07A", fg="black",
                                  font=("Arial", 12))
        cerrar_button.pack(pady=10)

    def eliminar_producto(self):
        selected_item = self.tree.selection()  # Obtener la fila seleccionada
        if selected_item:
            self.tree.delete(selected_item)  # Eliminar la fila seleccionada

