import tkinter as tk
from tkinter import messagebox

# Estructuras de datos (las mismas implementaciones que antes)
class NodoProducto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.siguiente = None

class ListaEnlazadaInventario:
    def __init__(self):
        self.cabeza = None
    
    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        nuevo_producto = NodoProducto(id_producto, nombre, cantidad, precio)
        if self.cabeza is None:
            self.cabeza = nuevo_producto
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_producto
    
    def eliminar_producto(self, id_producto):
        actual = self.cabeza
        anterior = None
        while actual is not None:
            if actual.id_producto == id_producto:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False
    
    def modificar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        actual = self.cabeza
        while actual is not None:
            if actual.id_producto == id_producto:
                if nueva_cantidad is not None:
                    actual.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    actual.precio = nuevo_precio
                return True
            actual = actual.siguiente
        return False
    
    def mostrar_inventario(self):
        productos = []
        actual = self.cabeza
        while actual is not None:
            productos.append((actual.id_producto, actual.nombre, actual.cantidad, actual.precio))
            actual = actual.siguiente
        return productos

class ColaVentas:
    def __init__(self):
        self.frente = None
        self.final = None
    
    def registrar_venta(self, id_venta, id_producto, cantidad, total, fecha, vendedor):
        nueva_venta = NodoVenta(id_venta, id_producto, cantidad, total, fecha, vendedor)
        if self.final is None:
            self.frente = self.final = nueva_venta
        else:
            self.final.siguiente = nueva_venta
            self.final = nueva_venta
    
    def generar_reporte(self):
        actual = self.frente
        reporte = "Reporte de ventas:\n"
        while actual is not None:
            reporte += f"ID Venta: {actual.id_venta}, Producto: {actual.id_producto}, Cantidad: {actual.cantidad}, Total: {actual.total}, Fecha: {actual.fecha}, Vendedor: {actual.vendedor}\n"
            actual = actual.siguiente
        with open("reporte_ventas.txt", "w") as archivo:
            archivo.write(reporte)
        return "Reporte de ventas generado en 'reporte_ventas.txt'."

# Inicialización de estructuras
inventario = ListaEnlazadaInventario()
cola_ventas = ColaVentas()

# Funciones de la GUI
def agregar_producto():
    id_producto = entry_id_producto.get()
    nombre = entry_nombre_producto.get()
    cantidad = int(entry_cantidad_producto.get())
    precio = float(entry_precio_producto.get())
    inventario.agregar_producto(id_producto, nombre, cantidad, precio)
    messagebox.showinfo("Éxito", f"Producto {nombre} agregado al inventario.")
    entry_id_producto.delete(0, tk.END)
    entry_nombre_producto.delete(0, tk.END)
    entry_cantidad_producto.delete(0, tk.END)
    entry_precio_producto.delete(0, tk.END)

def mostrar_inventario():
    productos = inventario.mostrar_inventario()
    ventana_inventario = tk.Toplevel(root)
    ventana_inventario.title("Inventario")
    for idx, producto in enumerate(productos):
        tk.Label(ventana_inventario, text=f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio: {producto[3]}").pack()

def eliminar_producto():
    id_producto = entry_id_producto_eliminar.get()
    if inventario.eliminar_producto(id_producto):
        messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado.")
    else:
        messagebox.showwarning("Error", f"Producto con ID {id_producto} no encontrado.")
    entry_id_producto_eliminar.delete(0, tk.END)

def generar_reporte_ventas():
    reporte = cola_ventas.generar_reporte()
    messagebox.showinfo("Reporte", reporte)

# Creación de la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Inventario y Ventas")

# Widgets para agregar producto
frame_agregar = tk.Frame(root)
frame_agregar.pack(pady=10)

tk.Label(frame_agregar, text="Agregar Producto").grid(row=0, column=0, columnspan=2)
tk.Label(frame_agregar, text="ID Producto:").grid(row=1, column=0)
entry_id_producto = tk.Entry(frame_agregar)
entry_id_producto.grid(row=1, column=1)

tk.Label(frame_agregar, text="Nombre Producto:").grid(row=2, column=0)
entry_nombre_producto = tk.Entry(frame_agregar)
entry_nombre_producto.grid(row=2, column=1)

tk.Label(frame_agregar, text="Cantidad:").grid(row=3, column=0)
entry_cantidad_producto = tk.Entry(frame_agregar)
entry_cantidad_producto.grid(row=3, column=1)

tk.Label(frame_agregar, text="Precio:").grid(row=4, column=0)
entry_precio_producto = tk.Entry(frame_agregar)
entry_precio_producto.grid(row=4, column=1)

tk.Button(frame_agregar, text="Agregar", command=agregar_producto).grid(row=5, column=0, columnspan=2)

# Widgets para mostrar inventario
frame_mostrar = tk.Frame(root)
frame_mostrar.pack(pady=10)

tk.Button(frame_mostrar, text="Mostrar Inventario", command=mostrar_inventario).pack()

# Widgets para eliminar producto
frame_eliminar = tk.Frame(root)
frame_eliminar.pack(pady=10)

tk.Label(frame_eliminar, text="Eliminar Producto").grid(row=0, column=0, columnspan=2)
tk.Label(frame_eliminar, text="ID Producto:").grid(row=1, column=0)
entry_id_producto_eliminar = tk.Entry(frame_eliminar)
entry_id_producto_eliminar.grid(row=1, column=1)

tk.Button(frame_eliminar, text="Eliminar", command=eliminar_producto).grid(row=2, column=0, columnspan=2)

# Widgets para generar reporte de ventas
frame_reporte = tk.Frame(root)
frame_reporte.pack(pady=10)

tk.Button(frame_reporte, text="Generar Reporte de Ventas", command=generar_reporte_ventas).pack()

# Iniciar la ventana principal
root.mainloop()

class NodoProducto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.siguiente = None

class ListaEnlazadaInventario:
    def __init__(self):
        self.cabeza = None
    
    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        nuevo_producto = NodoProducto(id_producto, nombre, cantidad, precio)
        if self.cabeza is None:
            self.cabeza = nuevo_producto
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_producto
        print(f"Producto {nombre} agregado al inventario.")
    
    def eliminar_producto(self, id_producto):
        actual = self.cabeza
        anterior = None
        while actual is not None:
            if actual.id_producto == id_producto:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                print(f"Producto con ID {id_producto} eliminado del inventario.")
                return
            anterior = actual
            actual = actual.siguiente
        print(f"Producto con ID {id_producto} no encontrado.")

    def modificar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        actual = self.cabeza
        while actual is not None:
            if actual.id_producto == id_producto:
                if nueva_cantidad is not None:
                    actual.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    actual.precio = nuevo_precio
                print(f"Producto con ID {id_producto} actualizado.")
                return
            actual = actual.siguiente
        print(f"Producto con ID {id_producto} no encontrado.")
    
    def mostrar_inventario(self):
        actual = self.cabeza
        print("Inventario actual:")
        while actual is not None:
            print(f"ID: {actual.id_producto}, Nombre: {actual.nombre}, Cantidad: {actual.cantidad}, Precio: {actual.precio}")
            actual = actual.siguiente

class NodoArbolProducto:
    def __init__(self, id_producto, nombre):
        self.id_producto = id_producto
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusquedaProductos:
    def __init__(self):
        self.raiz = None
    
    def insertar_producto(self, id_producto, nombre):
        nuevo_nodo = NodoArbolProducto(id_producto, nombre)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)
        print(f"Producto {nombre} agregado al árbol de búsqueda.")
    
    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.nombre < actual.nombre:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecha, nuevo_nodo)
    
    def buscar_producto(self, nombre):
        return self._buscar_recursivo(self.raiz, nombre)
    
    def _buscar_recursivo(self, actual, nombre):
        if actual is None:
            return None
        if actual.nombre == nombre:
            return actual
        elif nombre < actual.nombre:
            return self._buscar_recursivo(actual.izquierda, nombre)
        else:
            return self._buscar_recursivo(actual.derecha, nombre)
    
    def mostrar_productos_ordenados(self):
        print("Productos ordenados por nombre:")
        self._mostrar_in_orden(self.raiz)
    
    def _mostrar_in_orden(self, actual):
        if actual is not None:
            self._mostrar_in_orden(actual.izquierda)
            print(f"ID: {actual.id_producto}, Nombre: {actual.nombre}")
            self._mostrar_in_orden(actual.derecha)

class NodoVenta:
    def __init__(self, id_venta, id_producto, cantidad, total, fecha, vendedor):
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha
        self.vendedor = vendedor
        self.siguiente = None

class ColaVentas:
    def __init__(self):
        self.frente = None
        self.final = None
    
    def registrar_venta(self, id_venta, id_producto, cantidad, total, fecha, vendedor):
        nueva_venta = NodoVenta(id_venta, id_producto, cantidad, total, fecha, vendedor)
        if self.final is None:
            self.frente = self.final = nueva_venta
        else:
            self.final.siguiente = nueva_venta
            self.final = nueva_venta
        print(f"Venta registrada: ID Venta: {id_venta}, Producto: {id_producto}, Cantidad: {cantidad}, Total: {total}, Fecha: {fecha}")
    
    def procesar_ventas(self):
        actual = self.frente
        while actual is not None:
            print(f"Procesando venta ID: {actual.id_venta} de producto {actual.id_producto}")
            actual = actual.siguiente

    def generar_reporte(self):
        actual = self.frente
        reporte = "Reporte de ventas:\n"
        while actual is not None:
            reporte += f"ID Venta: {actual.id_venta}, Producto: {actual.id_producto}, Cantidad: {actual.cantidad}, Total: {actual.total}, Fecha: {actual.fecha}, Vendedor: {actual.vendedor}\n"
            actual = actual.siguiente
        with open("reporte_ventas.txt", "w") as archivo:
            archivo.write(reporte)
        print("Reporte de ventas generado.")

def mostrar_menu():
    print("\n--- Menú de Opciones ---")
    print("1. Agregar Producto al Inventario")
    print("2. Eliminar Producto del Inventario")
    print("3. Modificar Producto")
    print("4. Buscar Producto")
    print("5. Registrar Venta")
    print("6. Generar Reporte de Ventas")
    print("7. Mostrar Inventario")
    print("0. Salir")

# Inicialización de estructuras
inventario = ListaEnlazadaInventario()
arbol_productos = ArbolBinarioBusquedaProductos()
cola_ventas = ColaVentas()
