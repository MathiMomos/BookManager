import tkinter as tk

class HistorialVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        # Aquí puedes agregar el contenido de la ventana de historial de ventas
        label = tk.Label(self, text="Historial de ventas", font=("Arial", 16), bg="white")
        label.pack(pady=20)