import sqlite3
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Conexión y manejo de la base de datos SQLite
def crear_tabla():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id_producto TEXT PRIMARY KEY,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    ''')
    conexion.commit()
    conexion.close()

def cargar_productos_desde_db():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM inventario')
    productos = cursor.fetchall()
    conexion.close()
    return productos

def agregar_producto_db(id_producto, nombre, cantidad, precio):
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO inventario (id_producto, nombre, cantidad, precio)
        VALUES (?, ?, ?, ?)
    ''', (id_producto, nombre, cantidad, precio))
    conexion.commit()
    conexion.close()

def eliminar_producto_db(id_producto):
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM inventario WHERE id_producto = ?', (id_producto,))
    conexion.commit()
    conexion.close()

# Estructura de datos dinámica: Lista en Python para manejar el inventario en memoria
class SistemaInventario:
    def __init__(self):
        crear_tabla()  # Crear tabla si no existe (manejo externo: base de datos)
        self.inventario = []  # Lista dinámica para manejar productos internamente
        self.cargar_inventario_desde_db()

    def cargar_inventario_desde_db(self):
        productos_db = cargar_productos_desde_db()
        # Cargar productos desde la base de datos hacia la estructura dinámica interna (lista)
        self.inventario = [{'id': prod[0], 'nombre': prod[1], 'cantidad': prod[2], 'precio': prod[3]} for prod in productos_db]
    
    def agregar_producto(self, id_producto, nombre, cantidad, precio, posicion=None):
        producto = {'id': id_producto, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio}
        if posicion is None or posicion > len(self.inventario):
            self.inventario.append(producto)  # Agregar al final de la lista dinámica
        else:
            self.inventario.insert(posicion - 1, producto)  # Insertar en posición específica
        agregar_producto_db(id_producto, nombre, cantidad, precio)  # Almacenar externamente
        print(f"Producto {nombre} agregado en la posición {posicion if posicion is not None else len(self.inventario)}.")
    
    def eliminar_producto(self, posicion):
        if 1 <= posicion <= len(self.inventario):
            producto = self.inventario.pop(posicion - 1)  # Eliminar de la lista dinámica
            eliminar_producto_db(producto['id'])  # Eliminar también de la base de datos (almacenamiento)
            print(f"Producto {producto['nombre']} eliminado de la posición {posicion}.")
            return producto
        else:
            print(f"No hay producto en la posición {posicion}.")
            return None
    
    def buscar_producto(self, id_producto):
        for idx, producto in enumerate(self.inventario):
            if producto['id'] == id_producto:
                return idx + 1, producto  # Retornar posición basada en 1 y el producto
        return None, None
    
    def mostrar_inventario(self):
        return self.inventario

    def guardar_inventario_excel(self, archivo_excel):
        df = pd.DataFrame(self.inventario)
        df.to_excel(archivo_excel, index=False)
        print(f"Inventario guardado en {archivo_excel}.")

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

    if posicion is not None and (posicion < 1 or posicion > len(inventario.mostrar_inventario()) + 1):
        messagebox.showwarning("Posición inválida", f"Posición fuera de rango. Inserta en un rango válido de 1 a {len(inventario.mostrar_inventario()) + 1}")
    else:
        inventario.agregar_producto(id_producto, nombre, cantidad, precio, posicion)
        actualizar_listbox()
        messagebox.showinfo("Éxito", f"Producto {nombre} agregado al inventario.")
        limpiar_campos()

def eliminar_producto():
    posicion = lb_inventario.curselection()  # Obtener la posición seleccionada
    if posicion:
        inventario.eliminar_producto(posicion[0] + 1)  # Basado en 1
        actualizar_listbox()
        messagebox.showinfo("Éxito", f"Producto eliminado de la posición {posicion[0] + 1}")
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
        lb_inventario.insert(tk.END, f"Pos {idx + 1}: {producto['nombre']} - Cantidad: {producto['cantidad']}, Precio: {producto['precio']}")  # Basado en 1

def limpiar_campos():
    entry_id_producto.delete(0, tk.END)
    entry_nombre_producto.delete(0, tk.END)
    entry_cantidad_producto.delete(0, tk.END)
    entry_precio_producto.delete(0, tk.END)
    entry_posicion_producto.delete(0, tk.END)

def guardar_inventario_excel():
    archivo_excel = "BookManager/inventario.xlsx"  # Guardar dentro de la carpeta BookManager
    inventario.guardar_inventario_excel(archivo_excel)
    messagebox.showinfo("Éxito", f"Inventario guardado en {archivo_excel}")

# Crear la base de datos y la tabla
crear_tabla()

# Inicialización de estructuras
inventario = SistemaInventario()

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

# Botón para guardar el inventario en Excel
tk.Button(root, text="Guardar Inventario en Excel", command=guardar_inventario_excel).pack(pady=10)

# Cargar el inventario inicial en el Listbox
actualizar_listbox()

# Iniciar la ventana principal
root.mainloop()
