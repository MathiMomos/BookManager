import sqlite3
import datetime

class ModeloVentas:
    def __init__(self, db_path='ventas.db'):
        self.conexion = sqlite3.connect(db_path)

    def obtener_ventas_diarias(self):
        cursor = self.conexion.cursor()
        query = """
        SELECT fecha, precio, cantidad
        FROM ventas
        ORDER BY fecha ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        # Estructura de datos: diccionario para agrupar las ventas por fecha
        ventas_diarias = {}
        # Iterar sobre los resultados y sumar los totales
        for fecha, precio, cantidad in resultados:
            if fecha not in ventas_diarias:
                ventas_diarias[fecha] = 0  # Inicializar la fecha en el diccionario
            ventas_diarias[fecha] += precio * cantidad  # Sumar el total para la fecha
        # Convertir el diccionario a una lista ordenada de tuplas (fecha, total_ventas)
        # Eficiencia
        ventas_ordenadas = sorted(ventas_diarias.items())
        return ventas_ordenadas

    def obtener_ventas_mensuales(self):
        cursor = self.conexion.cursor()
        query = """
        SELECT fecha, precio, cantidad
        FROM ventas
        ORDER BY fecha ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        # Estructura de datos: diccionario para agrupar las ventas por mes
        ventas_mensuales = {}
        # Iterar sobre los resultados y sumar los totales
        for fecha_str, precio, cantidad in resultados:
            # Convertir la fecha a un objeto datetime y formatear el mes como 'YYYY-MM'
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
            mes = fecha.strftime('%Y-%m')
            # Inicializar la clave del mes
            if mes not in ventas_mensuales:
                ventas_mensuales[mes] = 0
            # Sumar el total de ventas al mes correspondiente
            ventas_mensuales[mes] += precio * cantidad
        # Convertir el diccionario a una lista ordenada de tuplas (mes, total_ventas)
        ventas_ordenadas = sorted(ventas_mensuales.items())
        return ventas_ordenadas

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