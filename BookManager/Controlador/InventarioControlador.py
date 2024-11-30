from BookManager.Data.ConexionBD import ConexionBD

class InventarioControlador:
    def __init__(self):
        self.conexion_bd = ConexionBD().conexion_inventario()
        self.inventario = TablaHashInventario()
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        cursor = self.conexion_bd.cursor()
        cursor.execute("SELECT * FROM inventario")
        productos = cursor.fetchall()
        cursor.close()
        for id_producto, nombre, cantidad, precio in productos:
            producto = Producto(id_producto, nombre, cantidad, precio)
            self.inventario.insertar(producto)

    def agregar_producto(self, nombre, cantidad, precio):
        cursor = self.conexion_bd.cursor()
        cursor.execute("INSERT INTO inventario (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (nombre, cantidad, precio))
        id_producto = cursor.lastrowid
        self.conexion_bd.commit()
        cursor.close()
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self.inventario.insertar(nuevo_producto)
        print(f"Producto '{nombre}' agregado correctamente.")

    def eliminar_producto(self, nombre):
        self.inventario.eliminar(nombre)
        cursor = self.conexion_bd.cursor()
        cursor.execute("DELETE FROM inventario WHERE nombre = ?", (nombre,))
        self.conexion_bd.commit()
        cursor.close()
        print(f"Producto '{nombre}' eliminado correctamente.")

    def modificar_producto(self, nombre, nueva_cantidad):
        producto = self.inventario.buscar(nombre)
        if producto:
            producto.cantidad = nueva_cantidad
            cursor = self.conexion_bd.cursor()
            cursor.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
            self.conexion_bd.commit()
            cursor.close()
            print(f"Cantidad actualizada para el producto '{nombre}'.")
        else:
            print(f"Producto '{nombre}' no encontrado en el inventario.")

    def buscar_producto(self, nombre):
        producto = self.inventario.buscar(nombre)
        if producto:
            print(f"Producto encontrado: ID={producto.id_producto}, Nombre={producto.nombre}, Cantidad={producto.cantidad}, Precio={producto.precio}")
        else:
            print(f"No se encontraron productos con el nombre '{nombre}'.")

    def ordenar_productos(self):
        productos_ordenados = self.inventario.listar_productos_ordenados()
        for producto in productos_ordenados:
            print(f"Nombre: {producto.nombre}, Cantidad: {producto.cantidad}, Precio: {producto.precio}")
        return productos_ordenados

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

class TablaHashInventario:
    def __init__(self, size=100):
        self.size = size
        self.tabla = [[] for _ in range(size)]

    def funcion_hash(self, nombre):
        return sum(ord(char) for char in nombre) % self.size

    def insertar(self, producto):
        indice = self.funcion_hash(producto.nombre)
        # Actualizamos si el producto ya existe
        for prod in self.tabla[indice]:
            if prod.nombre == producto.nombre:
                prod.cantidad = producto.cantidad
                prod.precio = producto.precio
                return
        # Si no existe, lo agregamos
        self.tabla[indice].append(producto)

    def eliminar(self, nombre):
        indice = self.funcion_hash(nombre)
        self.tabla[indice] = [prod for prod in self.tabla[indice] if prod.nombre != nombre]

    def buscar(self, nombre):
        indice = self.funcion_hash(nombre)
        for prod in self.tabla[indice]:
            if prod.nombre == nombre:
                return prod
        return None

    def listar_productos_ordenados(self):
        productos = []
        for lista in self.tabla:
            productos.extend(lista)
        return sorted(productos, key=lambda p: p.nombre)


