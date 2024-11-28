from tkinter import ttk
import tkinter as tk
from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador

class Inicio(PlantillaAdministrador):
        def __init__(self):
            super().__init__()
            self.agregar_mas_widgets()

        def agregar_mas_widgets(self):
            # Estilos

            # Frames
                self.Frame2 = ttk.Frame(self)
                self.Frame2.grid(row=0, column=1, sticky="nsew")
                self.Frame2.rowconfigure(0,weight=1)
                self.Frame2.columnconfigure(0,weight=1)
            # Etiquetas
                eti1 = ttk.Label(self.Frame2, text="INICIO")
                eti1.grid(row=0,column=0)
            # Botones


if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Inicio() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos