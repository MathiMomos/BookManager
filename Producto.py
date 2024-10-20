import tkinter as tk
from tkinter import messagebox

# Estructura de datos con lista para manejar el inventario con orden
class SistemaInventario:
    def __init__(self):
        self.inventario = []  # Lista para manejar productos en orden

    def agregar_producto(self, id_producto, nombre, cantidad, precio, posicion=None):
        producto = {'id': id_producto, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio}
        if posicion is None or posicion >= len(self.inventario):
            self.inventario.append(producto)
        else:
            self.inventario.insert(posicion, producto)
        print(f"Producto {nombre} agregado en la posición {posicion if posicion is not None else len(self.inventario) - 1}.")
    
    def eliminar_producto(self, posicion):
        if 0 <= posicion < len(self.inventario):
            producto = self.inventario.pop(posicion)
            print(f"Producto {producto['nombre']} eliminado de la posición {posicion}.")
            return producto
        else:
            print(f"No hay producto en la posición {posicion}.")
            return None
    
    def buscar_producto(self, id_producto):
        for idx, producto in enumerate(self.inventario):
            if producto['id'] == id_producto:
                return idx, producto
        return None, None
    
    def mostrar_inventario(self):
        return self.inventario

# Inicialización de estructuras
inventario = SistemaInventario()

# Funciones de la GUI
def agregar_producto():
    id_producto = entry_id_producto.get()
    nombre = entry_nombre_producto.get()
    cantidad = int(entry_cantidad_producto.get())
    precio = float(entry_precio_producto.get())
    
    # Obtener la posición ingresada por el usuario
    posicion_str = entry_posicion_producto.get()
    if posicion_str.isdigit():
        posicion = int(posicion_str)
    else:
        posicion = None  # Si no se ingresa una posición válida, se agregará al final

    if posicion is not None and (posicion < 0 or posicion > len(inventario.mostrar_inventario())):
        messagebox.showwarning("Posición inválida", f"Posición fuera de rango. Inserta en un rango válido de 0 a {len(inventario.mostrar_inventario())}")
    else:
        inventario.agregar_producto(id_producto, nombre, cantidad, precio, posicion)
        actualizar_listbox()
        messagebox.showinfo("Éxito", f"Producto {nombre} agregado al inventario.")
        limpiar_campos()

def eliminar_producto():
    posicion = lb_inventario.curselection()  # Obtener la posición seleccionada
    if posicion:
        inventario.eliminar_producto(posicion[0])
        actualizar_listbox()
        messagebox.showinfo("Éxito", f"Producto eliminado de la posición {posicion[0]}")
    else:
        messagebox.showwarning("Error", "Seleccione un producto para eliminar")

def buscar_producto():
    id_producto = entry_buscar_producto.get()
    posicion, producto = inventario.buscar_producto(id_producto)
    if producto:
        messagebox.showinfo("Producto Encontrado", f"Producto: {producto['nombre']}, Posición: {posicion}, Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")
    else:
        messagebox.showwarning("Error", "Producto no encontrado.")

def actualizar_listbox():
    lb_inventario.delete(0, tk.END)  # Limpiar el Listbox
    for idx, producto in enumerate(inventario.mostrar_inventario()):
        lb_inventario.insert(tk.END, f"Pos {idx}: {producto['nombre']} - Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")

def limpiar_campos():
    entry_id_producto.delete(0, tk.END)
    entry_nombre_producto.delete(0, tk.END)
    entry_cantidad_producto.delete(0, tk.END)
    entry_precio_producto.delete(0, tk.END)
    entry_posicion_producto.delete(0, tk.END)

# Creación de la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Inventario")

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

# Campo para ingresar la posición
tk.Label(frame_agregar, text="Posición (opcional):").grid(row=5, column=0)
entry_posicion_producto = tk.Entry(frame_agregar)
entry_posicion_producto.grid(row=5, column=1)

tk.Button(frame_agregar, text="Agregar", command=agregar_producto).grid(row=6, column=0, columnspan=2)

# Listbox para mostrar el inventario
frame_inventario = tk.Frame(root)
frame_inventario.pack(pady=10)

lb_inventario = tk.Listbox(frame_inventario, width=50)
lb_inventario.pack()

# Botón para eliminar producto seleccionado
tk.Button(root, text="Eliminar Producto Seleccionado", command=eliminar_producto).pack(pady=10)

# Widgets para buscar producto
frame_buscar = tk.Frame(root)
frame_buscar.pack(pady=10)

tk.Label(frame_buscar, text="Buscar Producto por ID:").grid(row=0, column=0)
entry_buscar_producto = tk.Entry(frame_buscar)
entry_buscar_producto.grid(row=0, column=1)
tk.Button(frame_buscar, text="Buscar", command=buscar_producto).grid(row=1, column=0, columnspan=2)

# Iniciar la ventana principal
root.mainloop()