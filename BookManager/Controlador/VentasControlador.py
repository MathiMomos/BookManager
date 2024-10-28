import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from BookManager.Modelo.ModeloVentas import ModeloVentas

class VentasControlador:
    def __init__(self):
        self.modelo = ModeloVentas()

    #def __init__(self):
    #una vez ya conectado con la BD para Producto
    def registrarVenta(self):
        if producto.empty:
            print(f"Producto {nombre} no encontrado en el inventario")
            return

        print(f"Venta registrada: {cantidad} unidades de '{nombre}' por un total de {total} soles.")
    
    def verHistorialDeVentas(self):
        #BD para historial de ventas
        if historial.empty
        print(f"Historial de ventas para '{vendedor}': {historial}")

    def generarTicket(self):
        print (f"Generando ticket en PDF para la venta ID {ventaID}")
        #implementar logica del pdf

    def generar_reporte_ventas(self):
        # Crear un archivo PDF para el reporte
        with PdfPages('reporte_ventas.pdf') as pdf:
            # Gráfico 1: Ventas Diarias
            self._generar_grafico_ventas_diarias(pdf)

            # Gráfico 2: Evolución de Ventas Mensuales
            self._generar_grafico_ventas_mensuales(pdf)

            # Gráfico 3: Distribución de Precios
            self._generar_grafico_distribucion_precios(pdf)

        print("Reporte generado en 'reporte_ventas.pdf'")

    def _generar_grafico_ventas_diarias(self, pdf):
        datos = self.modelo.obtener_ventas_diarias()
        fechas = [fecha for fecha, _ in datos]
        ventas = [total for _, total in datos]

        plt.figure()
        plt.plot(fechas, ventas, marker='o', linestyle='-', color='green')
        plt.title('Ventas Diarias')
        plt.xlabel('Fecha')
        plt.ylabel('Ventas en S/.')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Guardar en el PDF
        pdf.savefig()
        plt.close()

    def _generar_grafico_ventas_mensuales(self, pdf):
        datos = self.modelo.obtener_ventas_mensuales()
        meses = [mes for mes, _ in datos]
        ventas = [total for _, total in datos]

        plt.figure()
        plt.plot(meses, ventas, marker='o', linestyle='--', color='blue')
        plt.title('Evolución de Ventas Mensuales')
        plt.xlabel('Mes')
        plt.ylabel('Ventas en S/.')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Guardar en el PDF
        pdf.savefig()
        plt.close()

    def _generar_grafico_distribucion_precios(self, pdf):
        precios = self.modelo.obtener_precios_productos()

        plt.figure()
        plt.hist(precios, bins=10, color='purple', edgecolor='black')
        plt.title('Distribución de Precios de los Productos')
        plt.xlabel('Precio (S/.)')
        plt.ylabel('Frecuencia')
        plt.tight_layout()

        # Guardar en el PDF
        pdf.savefig()
        plt.close()

    def cerrar_conexion(self):
        self.modelo.cerrar_conexion()