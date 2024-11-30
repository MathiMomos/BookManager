from BookManager.Data.ConexionBD import ConexionBD

class EstadisticasSQL:
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.conexion_ventas = self.conexion_bd.conexion_ventas()  # Usar la conexión de ventas

    def producto_mas_vendido(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""SELECT producto, cantidad FROM ventas""")
        ventas = cursor.fetchall()
        cursor.close()

        producto_ventas = {}  # Diccionario para contar las ventas de cada producto

        # Contar la cantidad total vendida de cada producto
        for producto, cantidad in ventas:
            if producto in producto_ventas:
                producto_ventas[producto] += cantidad
            else:
                producto_ventas[producto] = cantidad

        # Identificar el producto más vendido
        if producto_ventas:
            producto_mas_vendido = max(producto_ventas, key=producto_ventas.get)
            return producto_mas_vendido, producto_ventas[producto_mas_vendido]

        return None

    def producto_menos_vendido(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""SELECT producto, cantidad FROM ventas""")
        ventas = cursor.fetchall()
        cursor.close()

        producto_ventas = {}  # Diccionario para contar las ventas de cada producto

        # Contar la cantidad total vendida de cada producto
        for producto, cantidad in ventas:
            if producto in producto_ventas:
                producto_ventas[producto] += cantidad
            else:
                producto_ventas[producto] = cantidad

        # Identificar el producto menos vendido
        if producto_ventas:
            producto_menos_vendido = min(producto_ventas, key=producto_ventas.get)
            return producto_menos_vendido, producto_ventas[producto_menos_vendido]

        return None

    def total_ventas_dia(self):
        cursor = self.conexion_ventas.cursor()
        cursor.execute("""
            SELECT fecha, precioTotal FROM ventas
        """)
        ventas = cursor.fetchall()
        cursor.close()

        # Usamos un diccionario para acumular las ventas por fecha
        ventas_dia = {}

        for fecha, precio_total in ventas:
            if fecha in ventas_dia:
                ventas_dia[fecha] += precio_total
            else:
                ventas_dia[fecha] = precio_total

        # Obtener el total de ventas del día de hoy (fecha local)
        fecha_hoy = str(self.obtener_fecha_hoy())

        return ventas_dia.get(fecha_hoy, 0.0)

    def obtener_fecha_hoy(self):
        # Esta función obtiene la fecha actual en formato 'YYYY-MM-DD'
        cursor = self.conexion_ventas.cursor()
        cursor.execute("SELECT DATE('now', 'localtime')")
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return resultado[0]
        return None

    def cerrar_conexion(self):
        self.conexion_ventas.close()