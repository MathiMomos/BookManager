# BookManager/Modelo/EstadisticasSQL.py
from BookManager.Data.ConexionBD import ConexionBD

class EstadisticasSQL:
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.conexion_ventas = self.conexion_bd.conexion_ventas()  # Usar la conexión de ventas

    def producto_mas_vendido(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""
            SELECT producto, SUM(cantidad) AS total_vendido
            FROM ventas
            GROUP BY producto
            ORDER BY total_vendido DESC
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return resultado
        return None

    def producto_menos_vendido(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""
            SELECT producto, SUM(cantidad) AS total_vendido
            FROM ventas
            GROUP BY producto
            ORDER BY total_vendido ASC
            LIMIT 1;
        """)
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return resultado
        return None

    def total_ventas_dia(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""
            SELECT SUM(precioTotal) AS total_ventas_dia
            FROM ventas
            WHERE fecha = DATE('now', 'localtime');
        """)
        resultado = cursor.fetchone()
        cursor.close()
        if resultado and resultado[0]:
            return resultado[0]
        return 0.0

    def cerrar_conexion(self):
        self.conexion_ventas.close()

