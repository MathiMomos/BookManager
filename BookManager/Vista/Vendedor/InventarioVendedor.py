import tkinter as tk

class InventarioVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        # Aquí puedes agregar el contenido de la ventana de inventario
        label = tk.Label(self, text="Inventario de productos", font=("Arial", 16), bg="white")
        label.pack(pady=20)