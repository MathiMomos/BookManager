import sqlite3

class ModeloVentas:
    def __init__(self, db_path='ventas.db'):
        self.conexion = sqlite3.connect(db_path)

    # Parte de la estadistica
    def obtener_ventas_diarias(self):
        cursor = self.conexion.cursor()
        query = """
        SELECT fecha, SUM(precio * cantidad) AS total_ventas
        FROM ventas
        GROUP BY fecha
        ORDER BY fecha ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def obtener_ventas_mensuales(self):
        cursor = self.conexion.cursor()
        query = """
        SELECT strftime('%Y-%m', fecha) AS mes, SUM(precio * cantidad) AS total_ventas
        FROM ventas
        GROUP BY mes
        ORDER BY mes ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def obtener_precios_productos(self):
        cursor = self.conexion.cursor()
        query = """
        SELECT precio FROM ventas
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return [precio[0] for precio in resultados]

    def cerrar_conexion(self):
        self.conexion.close()