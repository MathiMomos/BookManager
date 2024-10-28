import sqlite3
from BookManager.Data.ConexionBD import ConexionBD

class InventarioControlador:
    
    def __init__(self):
        self.conexion_bd = ConexionBD().conexion_inventario()
        self.historial_cambios = []  # Usaremos una pila para registrar cambios
    
    def agregar_producto(self, nombre, cantidad, precio, descripcion):
        cursor = self.conexion_bd.cursor()
        cursor.execute("INSERT INTO inventario (nombre, cantidad, precio, descripcion) VALUES (?, ?, ?, ?)",
                       (nombre, cantidad, precio, descripcion))
        self.conexion_bd.commit()
        self.historial_cambios.append(('agregar', nombre))  # Registrar en historial
        cursor.close()
        print(f"Producto '{nombre}' agregado correctamente.")
        
    def eliminar_producto(self, nombre):
        cursor = self.conexion_bd.cursor()
        cursor.execute("DELETE FROM inventario WHERE nombre = ?", (nombre,))
        self.conexion_bd.commit()
        self.historial_cambios.append(('eliminar', nombre))  # Registrar en historial
        cursor.close()
        print(f"Producto '{nombre}' eliminado correctamente.")
    
    def modificar_producto(self, nombre, nueva_cantidad):
        cursor = self.conexion_bd.cursor()
        cursor.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
        self.conexion_bd.commit()
        self.historial_cambios.append(('modificar', nombre, nueva_cantidad))  # Registrar en historial
        cursor.close()
        print(f"Cantidad actualizada para el producto '{nombre}'.")
    
    def buscar_producto(self, nombre):
        cursor = self.conexion_bd.cursor()
        cursor.execute("SELECT * FROM inventario WHERE nombre LIKE ?", ('%' + nombre + '%',))
        resultados = cursor.fetchall()
        cursor.close()
        if resultados:
            for producto in resultados:
                print(f"Producto encontrado: ID={producto[0]}, Nombre={producto[1]}, Cantidad={producto[2]}, Precio={producto[3]}, Descripción={producto[4]}")
        else:
            print(f"No se encontraron productos con el nombre '{nombre}'.")

    def ordenar_productos(self):
        cursor = self.conexion_bd.cursor()
        cursor.execute("SELECT nombre, cantidad FROM inventario ORDER BY nombre ASC")
        productos_ordenados = cursor.fetchall()
        cursor.close()
        return productos_ordenados  # Devuelve una lista ordenada de productos para su manejo
