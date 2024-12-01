from BookManager.Data.ConexionBD import ConexionBD
from collections import deque

class VendedorControlador:
    
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.cola_reembolsos = deque()

    def mostrar_productos(self):
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT idProducto, nombre, cantidad, precio FROM inventario")
        inventario = cursor.fetchall()

        cursor.close()
        conexion.close()

        return inventario if inventario else [] # Para la interfaz grafica

        #if inventario:
        #    print("ID |         Nombre          | Cantidad | Precio")
        #    print("=" * 50)
        #    for producto in inventario:
        #        print(f"{producto[0]} |         {producto[1]}         | {producto[2]} | {producto[3]}")
        #else:
        #    print("No hay ningun producto en el inventario")

    def ver_disponibilidad(self, id_producto):
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT cantidad, precio, nombre FROM inventario WHERE idProducto = ?", (id_producto,)) # No existia tabla productos
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

        confirmacion = True
        #confirmacion = input(f"Confirmar venta de {cantidad} unidades de {nombre} (y/n): ").strip().lower()
        if confirmacion:
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

        return historial if historial else []

        #if historial:
        #    print("ID |         Nombre          | Precio Unitario | Cantidad | Precio Total | Fecha | Hora")
        #    print("=" * 50)
        #    for venta in historial:
        #        print(
        #            f"{venta[0]} |         {venta[1]}         | {venta[2]} | {venta[3]} | {venta[4]} | {venta[5]} | {venta[6]}")
        #else:
        #    print("No hay ninguna venta en el historial")

    def solicitar_reembolso(self, id_pedido):
        self.cola_reembolsos.append(id_pedido)
        print(f"Reembolso solicitado para la venta con ID {id_pedido}")

    def realizar_reembolso(self):
        if not self.cola_reembolsos:
            print("No hay solicitudes de reembolso pendientes.")
            return False

        id_pedido = self.cola_reembolsos.popleft()

        conexion_ventas = self.conexion_bd.conexion_ventas()
        cursor_ventas = conexion_ventas.cursor()
        cursor_ventas.execute("SELECT producto, cantidad FROM ventas WHERE idPedido = ?", (id_pedido,))
        venta = cursor_ventas.fetchone()

        #cursor_ventas.close()
        #conexion_ventas.close()

        if venta is None:
            print(f"No se encontró la venta con ID {id_pedido}")
            return False

        nombre_producto, cantidad = venta

        conexion_inventario = self.conexion_bd.conexion_inventario()
        cursor_inventario = conexion_inventario.cursor()

        cursor_inventario.execute("SELECT cantidad FROM inventario WHERE nombre = ?", (nombre_producto,))
        inventario = cursor_inventario.fetchone()

        if inventario is None:
            print(f"No se encontró el producto {nombre_producto} en el inventario")
            return

        cantidad_actual = inventario[0]
        nueva_cantidad = cantidad_actual + cantidad

        cursor_inventario.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?",
                                  (nueva_cantidad, nombre_producto))
        conexion_inventario.commit()

        cursor_ventas.execute("DELETE FROM ventas WHERE idPedido = ?", (id_pedido,))
        conexion_ventas.commit()

        cursor_inventario.close()
        conexion_inventario.close()

        print(
            f"Reembolso procesado para el pedido ID {id_pedido}: {cantidad} unidades de {nombre_producto} devueltas al inventario.")
        return True # Para la interfaz grafica y no me de error