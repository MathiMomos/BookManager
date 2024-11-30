# BookManager/Controlador/EstadisticasControlador.py
from BookManager.Modelo.EstadisticasSQL import EstadisticasSQL

class EstadisticasControlador:
    def __init__(self):
        self.estadisticas_modelo = EstadisticasSQL()

    def obtener_producto_mas_vendido(self):
        return self.estadisticas_modelo.producto_mas_vendido()

    def obtener_producto_menos_vendido(self):
        return self.estadisticas_modelo.producto_menos_vendido()

    def obtener_total_ventas_dia(self):
        return self.estadisticas_modelo.total_ventas_dia()

    def cerrar_conexion(self):
        self.estadisticas_modelo.cerrar_conexion()

