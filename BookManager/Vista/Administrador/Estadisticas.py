# BookManager/Vista/Administrador/Estadisticas.py
from tkinter import ttk
import tkinter as tk
from BookManager.Controlador.EstadisticasControlador import EstadisticasControlador
from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador


class Estadisticas(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.agregar_mas_widgets()
        self.controlador = EstadisticasControlador()  # Instancia el controlador
        self.actualizar_estadisticas()

    def agregar_mas_widgets(self):
        # Crear el Frame
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        self.Frame2.rowconfigure(1, weight=2)
        self.Frame2.rowconfigure(2, weight=1)
        self.Frame2.rowconfigure(3, weight=1)
        self.Frame2.rowconfigure(4, weight=1)
        self.Frame2.rowconfigure(5, weight=2)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)

        # Etiquetas (Contenido adicional ya existente)
        self.etiquetaMayorProductoVendido = ttk.Label(self.Frame2, text="Producto con más ventas: ")
        self.etiquetaMayorProductoVendido.grid(row=1, column=0)

        self.etiquetaArticuloMayor = ttk.Label(self.Frame2, text="[Articulo más vendido]")
        self.etiquetaArticuloMayor.grid(row=1, column=1)

        self.etiquetaMenorProductoVendido = ttk.Label(self.Frame2, text="Producto con menos ventas: ")
        self.etiquetaMenorProductoVendido.grid(row=2, column=0)

        self.etiquetaArticuloMenor = ttk.Label(self.Frame2, text="[Articulo menos vendido]")
        self.etiquetaArticuloMenor.grid(row=2, column=1)

        self.etiquetaTotalDeVentasAlDia = ttk.Label(self.Frame2, text="Total de ventas de hoy: ")
        self.etiquetaTotalDeVentasAlDia.grid(row=3, column=0)

        self.etiquetaTotalVentasCambiarTexto = ttk.Label(self.Frame2, text="[Total de ventas]")
        self.etiquetaTotalVentasCambiarTexto.grid(row=3, column=1)

    def actualizar_estadisticas(self):
        # Obtener los datos del controlador
        producto_mas_vendido = self.controlador.obtener_producto_mas_vendido()
        producto_menos_vendido = self.controlador.obtener_producto_menos_vendido()
        total_ventas_dia = self.controlador.obtener_total_ventas_dia()

        # Actualizar las etiquetas con los resultados obtenidos
        if producto_mas_vendido:
            self.etiquetaArticuloMayor.config(text=f"{producto_mas_vendido[0]} ({producto_mas_vendido[1]} unidades)")
        else:
            self.etiquetaArticuloMayor.config(text="No disponible")

        if producto_menos_vendido:
            self.etiquetaArticuloMenor.config(text=f"{producto_menos_vendido[0]} ({producto_menos_vendido[1]} unidades)")
        else:
            self.etiquetaArticuloMenor.config(text="No disponible")

        self.etiquetaTotalVentasCambiarTexto.config(text=f"S/. {total_ventas_dia:.2f}")

        # Cerrar la conexión con la base de datos
        self.controlador.cerrar_conexion()

    # Métodos adicionales que quieras mantener para la vista
    def mostrar_mas_detalles(self):
        pass  # Puedes implementar otras funcionalidades adicionales aquí si lo necesitas

if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Estadisticas() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos
