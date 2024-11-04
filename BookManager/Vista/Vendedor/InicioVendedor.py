import tkinter as tk

class InicioVendedor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        # Aquí puedes agregar el contenido de la ventana de inicio
        label = tk.Label(self, text="Bienvenido a la página de inicio", font=("Arial", 16), bg="white")
        label.pack(pady=20)