from BookManager.Controlador.VentasControlador import VentasControlador
from BookManager.Controlador.InventarioControlador import InventarioControlador
from BookManager.Data.ConexionBD import ConexionBD

class Administrador:
    
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.controlador = VentasControlador()  # Inicializar el controlador
        self.controlador_inventario = InventarioControlador()
        
    def gestionarInventario(self):
        while(True):
            print("1. Agregar producto")
            print("2. Eliminar producto")
            print("3. Modificar producto")
            print("4. Buscar producto")
            print("0. Volver")
            try:
                opcion = int(input("Ingrese su opcion: "))
            except ValueError as error:
                print(f"Opcion invalida. Error {error}")
        
            if opcion == 1:
                self.agregarProducto()
            elif opcion == 2:
                self.eliminarProducto()
            elif opcion == 3:
                self.modificarProducto()
            elif opcion == 4:
                self.buscarProducto()
            elif opcion == 0:
                print("Volviendo")
                break

    def agregarProducto(self,nombre,cantidad,precio):
        # nombre = input("Nombre del producto: ").lower().strip()
        # cantidad = int(input("Cantidad: "))
        # precio = float(input("Precio: "))
        
        self.controlador_inventario.agregar_producto(nombre, cantidad, precio)

    def eliminarProducto(self):
        nombre = input("Nombre del producto a eliminar: ")
        self.controlador_inventario.eliminar_producto(nombre)

    def modificarProducto(self):
        nombre = input("Nombre del producto a modificar: ")
        db = self.conexion_bd.conexion_inventario()
        cursor = db.cursor()
        sql = "SELECT nombre FROM inventario WHERE nombre = ?"
        valores = (nombre,)
        cursor.execute(sql,valores)
        nombre_sql = cursor.fetchone()
        
        cursor.close()
        if nombre.lower().strip() == nombre_sql[0].lower().strip():
            print(f"Se encontró el producto {nombre_sql}")
            nueva_cantidad = int(input("Nueva cantidad: "))
            self.controlador_inventario.modificar_producto(nombre, nueva_cantidad)
        else:
            print("No se encontró el producto")

    def buscarProducto(self):
        nombre = input("Nombre del producto a buscar: ")
        self.controlador_inventario.buscar_producto(nombre)
    
    #----------------------------------
    def ver_disponibilidad(self, id_producto):
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT idProducto,cantidad, precio, nombre FROM inventario WHERE idProducto = ?", (id_producto,))
        producto = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if producto:
            print("Se encontró el producto")
            return producto
        else:
            print(f"El producto con ID {id_producto} no ha sido encontrado en inventario")
            return None
        
    def vender_producto(self, id_producto, cantidad):
        producto = self.ver_disponibilidad(id_producto)
        
        if producto is None:
            return False
        
        id_producto, stock_disponible, precio_unitario, nombre = producto

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
            INSERT INTO ventas (producto,precioUnitario, cantidad, precioTotal, fecha, hora)
            VALUES (?, ?, ?, ?, DATE('now', 'localtime'), TIME('now', 'localtime'))
        """, (nombre, precioUnitario, cantidad, precioTotal))

        conexion.commit()
        cursor.close()
        conexion.close()

        print(f"Venta registrada, {cantidad} unidades x <{nombre}> a S/.{precioUnitario} cada uno")
        
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

    def buscar_historial_por_id(self,id):
        conexion = self.conexion_bd.conexion_ventas()
        cursor = conexion.cursor()

        cursor.execute("SELECT idPedido, producto, precioUnitario, cantidad, precioTotal, fecha, hora from ventas WHERE idPedido = ?", (id,))
        historial = cursor.fetchone()

        cursor.close()
        conexion.close()

        return historial
