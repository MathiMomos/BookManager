from BookManager.Data.ConexionBD import ConexionBD

class InventarioControlador:
    
    def __init__(self):
        self.conexion_bd = ConexionBD().conexion_inventario()

    def agregar_producto(self, nombre, cantidad, precio):
        cursor = self.conexion_bd.cursor()
        cursor.execute("INSERT INTO inventario (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (nombre, cantidad, precio))
        self.conexion_bd.commit()
        cursor.close()
        print(f"Producto '{nombre}' agregado correctamente.")
        
    def eliminar_producto(self, nombre):
        cursor = self.conexion_bd.cursor()
        cursor.execute("DELETE FROM inventario WHERE nombre = ?", (nombre,))
        self.conexion_bd.commit()
        cursor.close()
        print(f"Producto '{nombre}' eliminado correctamente.")
    
    def modificar_producto(self, nombre, nueva_cantidad):
        cursor = self.conexion_bd.cursor()
        cursor.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
        self.conexion_bd.commit()
        cursor.close()
        print(f"Cantidad actualizada para el producto '{nombre}'.")
    
    def buscar_producto(self, nombre):
        cursor = self.conexion_bd.cursor()
        cursor.execute("SELECT * FROM inventario WHERE nombre LIKE ?", ('%' + nombre + '%',))
        resultados = cursor.fetchone()
        cursor.close()
        if resultados:
            print(f"Producto encontrado: ID={resultados[0]}, Nombre={resultados[1]}, Cantidad={resultados[2]}, Precio={resultados[3]}")
        else:
            print(f"No se encontraron productos con el nombre '{nombre}'.")

    def ordenar_productos(self):
        cursor = self.conexion_bd.cursor()
        cursor.execute("SELECT nombre, cantidad FROM inventario ORDER BY nombre ASC")
        productos_ordenados = cursor.fetchall()
        cursor.close()
        return productos_ordenados  # Devuelve una lista ordenada de productos para su manejo
    
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
                print(f"{venta[0]} |         {venta[1]}         | {venta[2]} | {venta[3]} | {venta[4]} | {venta[5]} | {venta[6]} | {venta[7]}")
        else:
            print("No hay ninguna venta en el historial")
