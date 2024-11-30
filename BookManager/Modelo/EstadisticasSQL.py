import sqlite3
import os

class EstadisticasSQL:
    def __init__(self):
        # Conectar a la base de datos de ventas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_ruta = os.path.join(self.base_dir, "..", "Data", "ventas.db")
        self.conexion = sqlite3.connect(self.db_ruta)
        self.cursor = self.conexion.cursor()

    def producto_mas_vendido(self):
        """Consulta para obtener el producto más vendido del día"""
        self.cursor.execute("""
            SELECT producto, SUM(cantidad) AS total_vendido
            FROM ventas
            WHERE fecha = DATE('now', 'localtime')
            GROUP BY producto
            ORDER BY total_vendido DESC
            LIMIT 1;
        """)
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado  # Devuelve el producto y su cantidad vendida
        return None  # Si no hay resultados

    def producto_menos_vendido(self):
        """Consulta para obtener el producto menos vendido del día"""
        self.cursor.execute("""
            SELECT producto, SUM(cantidad) AS total_vendido
            FROM ventas
            WHERE fecha = DATE('now', 'localtime')
            GROUP BY producto
            ORDER BY total_vendido ASC
            LIMIT 1;
        """)
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado  # Devuelve el producto y su cantidad vendida
        return None  # Si no hay resultados

    def total_ventas_dia(self):
        """Consulta para obtener el total de ventas realizadas hoy"""
        self.cursor.execute("""
            SELECT SUM(precioTotal) AS total_ventas_dia
            FROM ventas
            WHERE fecha = DATE('now', 'localtime');
        """)
        resultado = self.cursor.fetchone()
        if resultado and resultado[0]:
            return resultado[0]
        return 0.0  # Si no hay ventas, devuelve 0

    def cerrar_conexion(self):
        """Cerrar la conexión con la base de datos"""
        self.cursor.close()
        self.conexion.close()
