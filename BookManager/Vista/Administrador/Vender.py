import os
from tkinter import ttk
from PIL import Image, ImageTk
from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador
from BookManager.Controlador.AdministradorControlador import Administrador
import tkinter as tk

class Vender(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.Administrador = Administrador()
        self.carrito = []  # Inicializar el carrito como una lista vacía
        self.agregar_mas_widgets()

    def agregar_mas_widgets(self):
        # Aqui van los estilos -----------------------------------------
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Este frame será para las tablas y etiquetas
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        self.Frame2.rowconfigure(0, weight=1)
        self.Frame2.rowconfigure(1, weight=1)
        self.Frame2.rowconfigure(2, weight=1)
        self.Frame2.rowconfigure(3, weight=5)
        self.Frame2.rowconfigure(4, weight=1)

        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)
        self.Frame2.columnconfigure(2, weight=2)
        self.Frame2.columnconfigure(3,weight=2)

        # Label titulo
        self.titulo_vender = ttk.Label(self.Frame2, text="VENDER")
        self.titulo_vender.grid(row = 0, column = 0, columnspan=4)

        self.agregar_imagen()

        # Crear la entrada del buscador

        self.entrada_buscador = ttk.Entry(self.Frame2)
        self.entrada_buscador.grid(row=1, column=1, sticky="w")

        # Cantidades a elegir -----

        self.etiqueta_cantidades = ttk.Label(self.Frame2, text="Ingrese la cantidad a vender: ")
        self.etiqueta_cantidades.grid(row=2,column=0)

        self.entrada_cantidad_venta = ttk.Entry(self.Frame2)
        self.entrada_cantidad_venta.grid(row=2, column=1, sticky="w")

        # Tabla
        self.cargar_tabla_inventario()

        # Botones
        self.boton_agregar_carrito = ttk.Button(self.Frame2, text="Agregar al carrito", command=self.agregar_al_carrito)
        self.boton_agregar_carrito.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=5, pady=5)

        self.boton_ver_carrito = ttk.Button(self.Frame2, text="Ver carrito", command=self.ver_carrito)
        self.boton_ver_carrito.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

        self.boton_confirmar_venta = ttk.Button(self.Frame2, text="Confirmar compra", command=self.confirmar_venta)
        self.boton_confirmar_venta.grid(row=4, column=3, sticky="nsew", padx=5, pady=5)

        self.boton_buscar = ttk.Button(self.Frame2, text = "Buscar", command = self.buscar_por_id)
        self.boton_buscar.grid(row=1, column=2, sticky="w")

        # Seleccionar una fila de la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)


    def agregar_imagen(self):
        directorio_base = os.path.dirname(os.path.abspath(__file__))
        ruta_base = os.path.join(directorio_base, "Iconos", "buscador")
        # Cargar la imagen original
        ruta_imagen = os.path.join(ruta_base, "lupa.png")
        imagen_original = Image.open(ruta_imagen)

        # Cambiar tamaño de la imagen (200x200 píxeles)
        imagen_redimensionada = imagen_original.resize((25, 25))

        # Convertir la imagen para Tkinter
        self.imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

        # Mostrar la imagen en un Label
        label_imagen = ttk.Label(self.Frame2, image=self.imagen_tk)
        label_imagen.grid(row=1, column=0, padx=10, pady=10)

    def cargar_tabla_inventario(self):
        self.tabla = ttk.Treeview(self.Frame2, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        self.tabla.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=5)

        # Configuración de las columnas de la tabla
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio")

        # Configuración del ancho de las columnas
        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=150, anchor="w")
        self.tabla.column("Cantidad", width=100, anchor="center")
        self.tabla.column("Precio", width=100, anchor="e")

        # Cargar los datos de la tabla
        self.cargarTabla()

    def cargarTabla(self):
        from BookManager.Data.ConexionBD import ConexionBD
        self.conexion_bd = ConexionBD()
        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM inventario")
        self.ListaProductos = cursor.fetchall()

        # Agregar algunas filas a la tabla (por ejemplo)
        for id, nombre, cantidad, precio in self.ListaProductos:
            self.tabla.insert("", "end", values=(id, nombre, cantidad, precio))

    def actualizar_tabla(self):
        self.limpiar_tabla()
        self.cargarTabla()

    def seleccionar_fila(self, event):
        """Llena la entrada de cantidad con el máximo disponible de la fila seleccionada."""
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion, "values")
            cantidad_disponible = int(valores[2])
            self.entrada_cantidad_venta.delete(0, tk.END)
            self.entrada_cantidad_venta.insert(0, cantidad_disponible)

    def agregar_al_carrito(self):
        """Agrega un producto al carrito con la cantidad especificada."""
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion, "values")
            cantidad_disponible = int(valores[2])
            precio_unitario = float(valores[3])
            cantidad_ingresada = int(self.entrada_cantidad_venta.get())

            if cantidad_ingresada > 0 and cantidad_ingresada <= cantidad_disponible:
                precio_total = cantidad_ingresada * precio_unitario
                self.carrito.append((valores[1], cantidad_ingresada, precio_unitario, precio_total))
                tk.messagebox.showinfo("Carrito", f"Producto {valores[1]} agregado al carrito.")
            else:
                tk.messagebox.showerror("Error", "Cantidad ingresada inválida.")

    def ver_carrito(self):
        """Muestra el contenido del carrito en una nueva ventana."""
        ventana_carrito = tk.Toplevel(self)
        ventana_carrito.title("Carrito de compras")
        ventana_carrito.geometry("400x300")

        tabla_carrito = ttk.Treeview(ventana_carrito, columns=("Nombre", "Cantidad", "Precio Unitario", "Precio Total"),
                                     show="headings")
        tabla_carrito.pack(fill=tk.BOTH, expand=True)

        # Configurar encabezados de la tabla
        tabla_carrito.heading("Nombre", text="Nombre")
        tabla_carrito.heading("Cantidad", text="Cantidad")
        tabla_carrito.heading("Precio Unitario", text="Precio Unitario")
        tabla_carrito.heading("Precio Total", text="Precio Total")

        for nombre, cantidad, precio_unitario, precio_total in self.carrito:
            tabla_carrito.insert("", "end", values=(nombre, cantidad, precio_unitario, precio_total))

    def confirmar_venta(self):
        """Confirma la venta actualizando la base de datos."""
        if not self.carrito:
            tk.messagebox.showerror("Error", "El carrito está vacío.")
            return

        conexion = self.conexion_bd.conexion_inventario()
        cursor = conexion.cursor()

        try:
            for nombre, cantidad, precioU, precioT in self.carrito:
                cursor.execute(
                    "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ? AND cantidad >= ?",
                    (cantidad, nombre, cantidad),
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Error actualizando el producto {nombre}. Stock insuficiente.")
                Administrador.registrar_venta(self, nombre, cantidad, precioU, precioT)


            conexion.commit()
            tk.messagebox.showinfo("Éxito", "La venta se ha confirmado con éxito.")
            self.carrito = []
            self.actualizar_tabla()
        except Exception as e:
            conexion.rollback()
            tk.messagebox.showerror("Error", f"No se pudo completar la venta: {str(e)}")
        finally:
            conexion.close()
    def buscar_por_id(self):
        dato = int(self.entrada_buscador.get())

        # Se uso administrador controlador
        if dato > 0:
            producto = self.Administrador.ver_disponibilidad(dato)
            id, cantidad, precio, nombre = producto
            self.limpiar_tabla()
            self.tabla.insert("", "end",values = (id,nombre,precio,cantidad))
        else:
            tk.messagebox.showerror("Error", "Ingrese un id valido")

    def limpiar_tabla(self):
        # Elimina todos los elementos de la tabla
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)



if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Vender() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos

