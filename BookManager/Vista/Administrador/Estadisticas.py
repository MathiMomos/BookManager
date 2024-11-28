from tkinter import ttk

from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador
import tkinter as tk

class Estadisticas(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.agregar_mas_widgets()

    def agregar_mas_widgets(self):
        # Aqui iran los estilos de los widgets

        #Creacion del frame
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        self.Frame2.rowconfigure(1,weight=2)
        self.Frame2.rowconfigure(2,weight=1)
        self.Frame2.rowconfigure(3,weight=1)
        self.Frame2.rowconfigure(4,weight=1)
        self.Frame2.rowconfigure(5,weight=2)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1,weight=1)

        # Etiquetas
        self.etiquetaMayorProductoVendido = ttk.Label(self.Frame2, text="Producto con mas ventas: ")
        self.etiquetaMayorProductoVendido.grid(row=1,column=0)

        self.etiquetaArticuloMayor = ttk.Label(self.Frame2, text = "[Articulo + vendido]")
        self.etiquetaArticuloMayor.grid(row = 1, column =1)

        self.etiquetaMenorProductoVendido = ttk.Label(self.Frame2, text = "Producto con menos ventas: ")
        self.etiquetaMenorProductoVendido.grid(row=2,column=0)

        self.etiquetaArticuloMenor = ttk.Label(self.Frame2, text="[Articulo - vendido]")
        self.etiquetaArticuloMenor.grid(row=2, column=1)

        self.etiquetaTotalDeVentasAlDia = ttk.Label(self.Frame2, text = "Total de ventas de hoy: ")
        self.etiquetaTotalDeVentasAlDia.grid(row=3,column=0)

        self.etiquetaTotalVentasCambiarTexto = ttk.Label(self.Frame2, text = "[Total de ventas]")
        self.etiquetaTotalVentasCambiarTexto.grid(row=3, column=1)

        self.modificarEtiquetas()

    def modificarEtiquetas(self):

        # Parte de Arley

        textoArticuloMayor = ""
        self.etiquetaArticuloMayor.config(text=textoArticuloMayor)
        textoArticuloMenor = ""
        self.etiquetaArticuloMenor.config(text=textoArticuloMenor)
        textoVentasDia = ""
        self.etiquetaTotalVentasCambiarTexto.config(text=textoVentasDia)

if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Estadisticas() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos