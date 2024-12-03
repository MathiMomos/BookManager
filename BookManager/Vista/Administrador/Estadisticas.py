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
        # Aqui van los estilos
        estilo = ttk.Style()
        estilo.theme_use("clam")
        # Estilos para las etiquetas de titulo
        estilo.configure(
            "etiquetaTitulo.TLabel",
            foreground="Gray",  # Color del texto

            font=("Helvetica", 16, "bold"),  # Tipo de fuente, tamaño, y estilo (negrita)
        )
        # para etiquetas de texto
        estilo.configure(
            "etiquetaTexto.TLabel",
            foreground="black",  # Color del texto
            background="#e1f5d2",  # Fondo verde
            font=("Helvetica", 16),  # Fuente, tamaño
            padding=10  # Relleno interno
        )
        # para etiquetas de texto de numero
        estilo.configure(
            "etiquetaTexto2.TLabel",
            foreground="black",  # Color del texto
            background="#e1f5d2",  # Fondo verde
            font=("Helvetica", 16, "bold"),  # Fuente, tamaño y negrita
            padding=10  # Relleno interno
        )
        estilo.configure(
            "estiloFrame.TFrame",
            background="#e1f5d2",
            padding=2
        )
        # Crear el Frame
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        self.Frame2.rowconfigure(0,weight=1)
        self.Frame2.rowconfigure(1, weight=2)
        self.Frame2.rowconfigure(2,weight=1)

        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)

        # Etiqueta titulo
        self.TituloEstadistica = ttk.Label(self.Frame2, text = "ESTADISTICA", style="etiquetaTitulo.TLabel")
        self.TituloEstadistica.grid(row = 0, column=0, columnspan=2)

        self.Frame3 = ttk.Frame(self.Frame2, style="estiloFrame.TFrame")
        self.Frame3.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20,pady=20)
        # configurar las grillas
        for i in range(0,3):
            self.Frame3.rowconfigure(i,weight=1)
            self.Frame3.columnconfigure(i,weight=1)


        # Etiquetas (Contenido adicional ya existente)
        self.etiquetaMayorProductoVendido = ttk.Label(self.Frame3, text="Producto con más ventas: ", style="etiquetaTexto.TLabel")
        self.etiquetaMayorProductoVendido.grid(row=0, column=0)

        self.etiquetaArticuloMayor = ttk.Label(self.Frame3, text="[Articulo más vendido]", style="etiquetaTexto2.TLabel")
        self.etiquetaArticuloMayor.grid(row=0, column=1)

        self.etiquetaMenorProductoVendido = ttk.Label(self.Frame3, text="Producto con menos ventas: ",style="etiquetaTexto.TLabel")
        self.etiquetaMenorProductoVendido.grid(row=1, column=0)

        self.etiquetaArticuloMenor = ttk.Label(self.Frame3, text="[Articulo menos vendido]", style="etiquetaTexto2.TLabel")
        self.etiquetaArticuloMenor.grid(row=1, column=1)

        self.etiquetaTotalDeVentasAlDia = ttk.Label(self.Frame3, text="Total de ventas de hoy: ", style="etiquetaTexto.TLabel")
        self.etiquetaTotalDeVentasAlDia.grid(row=2, column=0)

        self.etiquetaTotalVentasCambiarTexto = ttk.Label(self.Frame3, text="[Total de ventas]", style="etiquetaTexto2.TLabel")
        self.etiquetaTotalVentasCambiarTexto.grid(row=2, column=1)

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