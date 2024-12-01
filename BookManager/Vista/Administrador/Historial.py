import os
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from BookManager.Controlador.AdministradorControlador import Administrador
from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador
import tkinter as tk
from BookManager.Controlador.VendedorControlador import VendedorControlador

class Historial(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.agregar_mas_widgets()
        self.Administrador = Administrador()
        self.controlador = VendedorControlador()

    def agregar_mas_widgets(self):
        # Aqui van los estilos -----------------------------------------
        estilo = ttk.Style()
        estilo.theme_use("clam")
        # Estilos para las etiquetas
        estilo.configure(
            "etiquetaTitulo.TLabel",
            foreground="Gray",  # Color del texto

            font=("Helvetica", 16, "bold"),  # Tipo de fuente, tamaño, y estilo (negrita)
        )
        # Estilos para los botones
        estilo.configure(
            "botonEstilo.TButton",
            background="#c7c1ec",  # Color de fondo normal
            foreground="black",  # Color del texto
            font=("Arial", 16, "bold"),
            borderwidth=0,  # Eliminar el borde
            relief="flat"  # Eliminar el relieve (bordes)
        )
        estilo.map("botonEstilo.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#7668d0"), ("active", "#948ad1")]  # Cambia el color de fondo al presionar
                   )

        # para el boton de reembolso
        estilo.configure(
            "botonReembolso.TButton",
            background="#ffb2a2",  # Color de fondo normal
            foreground="black",  # Color del texto
            font=("Arial", 16, "bold"),
            borderwidth=0,  # Eliminar el borde
            relief="flat"  # Eliminar el relieve (bordes)
        )
        estilo.map("botonReembolso.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#c87644"), ("active", "#e5b79b")]  # Cambia el color de fondo al presionar
                   )

        # Estilos para las tablas
        estilo.configure('Treeview',
                         font=("Helvetica", 14),

                         rowheight=30)
        estilo.map('Treeview', background=[('selected', '#948ad1')])

        # Creacion del frame 2
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        # Configuración de las filas y columnas
        self.Frame2.rowconfigure(0, weight=1)
        self.Frame2.rowconfigure(1, weight=1)
        self.Frame2.rowconfigure(2, weight=8)
        self.Frame2.rowconfigure(3, weight=1)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)
        self.Frame2.columnconfigure(2, weight=1)

        # Etiqueta titulo
        self.titulo = ttk.Label(self.Frame2, text="HISTORIAL DE VENTAS", style="etiquetaTitulo.TLabel")
        self.titulo.grid(row=0, column=0,columnspan=3)

        # Cargar la imagen
        self.agregar_imagen()

        # Crear la entrada del buscador
        self.entrada_buscador = ttk.Entry(self.Frame2)
        self.entrada_buscador.grid(row=1, column=1, padx=10, pady=10,sticky="w")

        # Boton buscar
        self.boton_buscar = ttk.Button(self.Frame2, text="Buscar ID", command=self.buscar_por_id, style="botonEstilo.TButton")
        self.boton_buscar.grid(row=1, column=2, padx=10, pady=10,sticky="w")

        # Boton reembolso
        self.BotonReembolso = ttk.Button(self.Frame2, text="Reembolso", command=self.solicitar_reembolso_vista, style="botonReembolso.TButton")
        self.BotonReembolso.grid(row=3, column=1, padx=5, pady=5)

        # Agregar tabla
        self.cargar_tabla_historial()

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
        label_imagen.grid(row=1, column=0, padx=5, pady=5)

    def buscar_por_id(self):
        dato = int(self.entrada_buscador.get())

        if dato > 0:
            producto = self.Administrador.buscar_historial_por_id(dato)

            # Verificar si el producto es None
            if producto is not None:
                ide, nombre, precioU, cantidad, precioT, fecha, hora = producto
                self.limpiar_tabla()
                self.tabla.insert("", "end", values=(ide, nombre, cantidad, precioU, precioT, fecha, hora))
            else:
                tk.messagebox.showerror("Error", "Producto no encontrado.")
        else:
            tk.messagebox.showerror("Error", "Ingrese un id valido")

    def cargar_tabla_historial(self):
        self.tabla = ttk.Treeview(self.Frame2, columns=("ID", "Nombre", "Cantidad", "Precio","Precio Total", "Fecha", "Hora"), show="headings")
        self.tabla.grid(row=2, column=0, sticky="nsew", padx=10, pady=5,columnspan=3)

        # Configuración de las columnas de la tabla
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Precio Total", text = "Precio total")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Hora", text="Hora")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=150, anchor="w")
        self.tabla.column("Cantidad", width=100, anchor="center")
        self.tabla.column("Precio", width=100, anchor="e")

        # Cargar los datos de la tabla
        self.cargar_tabla()



    def cargar_tabla(self):
        from BookManager.Data.ConexionBD import ConexionBD
        self.conexion_bd = ConexionBD()
        conexion = self.conexion_bd.conexion_ventas()
        cursor = conexion.cursor()

        cursor.execute('SELECT * FROM ventas')
        self.ListaProductos = cursor.fetchall()

        # Agregar algunas filas a la tabla (por ejemplo)
        for id, nombre, cantidad, precio, preciototal, fecha, hora in self.ListaProductos:
            self.tabla.insert("", "end", values=(id, nombre, cantidad, precio, preciototal, fecha, hora))

    def limpiar_tabla(self):
        # Elimina todos los elementos de la tabla
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

    def solicitar_reembolso_vista(self):
        # Verificar selección
        seleccion = self.tabla.selection()
        if not seleccion:
            tk.messagebox.showwarning("Advertencia", "Por favor, selecciona una venta para solicitar reembolso.")
            return
        # Obtener ID de pedido
        id_pedido = self.tabla.item(seleccion[0])["values"][0]
        # Llamar al controlador
        try:
            respuesta = tk.messagebox.askyesno("Confirmacion", "Estas seguro que deseas continuar", )
            if respuesta:
                self.controlador.solicitar_reembolso(id_pedido)
                self.controlador.realizar_reembolso()
                tk.messagebox.showinfo("Éxito", f"Reembolso solicitado para el pedido con ID {id_pedido}.")
                self.actualizarTabla()
            else:
                return
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al solicitar reembolso: {str(e)}")

    def actualizarTabla(self):
        for item in self.tabla.get_children():  # Obtener todos los elementos de la tabla
            self.tabla.delete(item)  # Eliminar cada elemento
        self.cargarTabla()

if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Historial() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos