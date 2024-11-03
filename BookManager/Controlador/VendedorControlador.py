from BookManager.Data.ConexionBD import ConexionBD

class VendedorControlador:
    
    def __init__(self):
        self.conexion_bd = ConexionBD()

    def mostrar_productos(self):
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT idProducto, nombre, cantidad, precio FROM inventario")
        inventario = cursor.fetchall()

        cursor.close()
        conexion.close()

        if inventario:
            print("ID |         Nombre          | Cantidad | Precio")
            print("=" * 50)
            for producto in inventario:
                print(f"{producto[0]} |         {producto[1]}         | {producto[2]} | {producto[3]}")
        else:
            print("No hay ningun producto en el inventario")

    def ver_disponibilidad(self, id_producto):
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT cantidad, precio, nombre FROM productos WHERE idProducto = ?", (id_producto,))
        producto = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if producto:
            print("Cantidad | Precio Unitario |        Nombre")
            return producto  # Devuelve (cantidad_disponible, precio_unitario, nombre)
        else:
            print(f"El producto con ID {id_producto} no ha sido encontrado en inventario")
            return None
    

    def vender_producto(self, id_producto, cantidad):
        producto = self.ver_disponibilidad(id_producto)
        
        if producto is None:
            return False
        
        stock_disponible, precio_unitario, nombre = producto

        if stock_disponible < cantidad:
            print(f"Stock insuficiente para el producto {id_producto}")
            print(f"Stock disponible: {stock_disponible}")
            return False
        
        confirmacion = input(f"Confirmar venta de {cantidad} unidades de {nombre} (y/n): ").strip().lower()
        if confirmacion == "y":
            conexion = self.conexion_bd.conexion_inventario()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE inventario SET cantidad = ? - ?
                WHERE idProducto = ?
            """, (stock_disponible, cantidad, id_producto))
            
            conexion.commit()
            cursor.close()
            conexion.close()

            print(f"Venta realizada del producto {nombre}")
            print("Inventario actualizado")
            
            precio_total = cantidad * precio_unitario
            self.registrar_venta(nombre, cantidad, precio_unitario, precio_total)
            return True
        else:
            print("Venta cancelada")
            return False

    def registrar_venta(self, nombre, cantidad, precioUnitario, precioTotal):
        conexion = self.conexion_bd.conexion_ventas()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO ventas (producto, precioUnitario, cantidad, precioTotal, fecha, hora)
            VALUES (?, ?, ?, ?, DATE('now', 'localtime'), TIME('now', 'localtime'))
        """, (nombre, precioUnitario, cantidad, precioTotal))

        conexion.commit()
        cursor.close()
        conexion.close()

        print(f"Venta registrada, {cantidad} unidades x <{nombre}> a S/.{precioUnitario} cada uno")

    def ver_historial_ventas(self):
        conexion = self.conexion_bd.conexion_ventas()
        cursor = conexion.cursor()

        cursor.execute("SELECT idPedido, producto, precioUnitario, cantidad, precioTotal, fecha, hora from ventas")
        historial = cursor.fetchall()

        cursor.close()
        conexion.close()

        if historial:
            print("ID |         Nombre          | Precio Unitario | Cantidad | Precio Total | Fecha | Hora")
            print("=" * 50)
            for venta in historial:
                print(f"{venta[0]} |         {venta[1]}         | {venta[2]} | {venta[3]} | {venta[4]} | {venta[5]} | {venta[6]}")
        else:
            print("No hay ninguna venta en el historial")
    
    def realizar_reembolso(self):
        pass