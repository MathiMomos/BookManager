from Data.ConexionBD import ConexionBD

class InventarioControlador:
    
    def __init__(self):
        self.conexion = ConexionBD().conexion_inventario()

    def agregarProducto(self, nombre, cantidad, precio, descripcion):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio, descripcion) VALUES (?, ?, ?, ?)",
                       (nombre, cantidad, precio, descripcion))
        self.conexion.commit()
        cursor.close()
        print(f"Producto '{nombre}' agregado correctamente")

    def eliminarProducto(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
        self.conexion.commit()
        cursor.close()
        print(f"Producto '{nombre}' eliminado correctamente")

    def modificarProducto(self, nombre, nueva_cantidad):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
        self.conexion.commit()
        cursor.close()
        print(f"Cantidad actualizada para el producto '{nombre}'")

    def buscarProducto(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
        resultados = cursor.fetchall()
        cursor.close()
        if resultados:
            print(f"Productos encontrados para '{nombre}': {resultados}")
        else:
            print(f"No se encontraron productos para '{nombre}'")

    def ordenarProducto(self, criterio='nombre'):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT * FROM productos ORDER BY {criterio}")
        productos_ordenados = cursor.fetchall()
        cursor.close()
        return productos_ordenados
