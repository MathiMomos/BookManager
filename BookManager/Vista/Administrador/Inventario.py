from BookManager.Vista.Administrador.PlantillaAdministrador import *
import tkinter as tk

class Inventario(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.ListaProductos = None
        self.conexion_bd = None
        self.Frame2 = None
        self.tabla = None
        self.agregar_mas_widgets()

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

        # Estilos para las tablas
        estilo.configure('Treeview',
                         font=("Helvetica", 14),

                          rowheight=30)
        estilo.map('Treeview', background=[('selected', '#948ad1')])
        #Creacion del frame2 -------------------------------------------

        # Este frame será para las tablas y etiquetas
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0, column=1, sticky="nsew")

        # El frame 2 tendrá 3 filas y 3 columnas
        self.Frame2.rowconfigure(0,weight=1)
        self.Frame2.rowconfigure(1,weight=1)
        self.Frame2.rowconfigure(2,weight=7)
        self.Frame2.rowconfigure(3, weight=1)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1, weight=1)
        self.Frame2.columnconfigure(2, weight=1)

        #Creacion de etiquetas ------------------------------------------

        etiqueta_titulo1 = ttk.Label(self.Frame2, text="Inventario", style="etiquetaTitulo.TLabel",anchor="center")
        etiqueta_titulo1.grid(row=0, column=1, sticky="nsew")

        #Creacion de botones --------------------------------------------

        nombre_boton_crud = ["Añadir producto", "Modificar producto", "Eliminar producto"]
        nombre_metodo_boton = [self.agregar, self.modificar, self.eliminar]

        for i, texto, comando in zip(range(0,2+1),nombre_boton_crud,nombre_metodo_boton):
            self.boton = ttk.Button(self.Frame2, text=texto,command=comando, style="botonEstilo.TButton")
            self.boton.grid(row=1,column=i,sticky="nsew", padx=10,pady=10)

        # Boton de exportar
        self.boton_exportar = ttk.Button(self.Frame2, text="Exportar inventario", command=self.exportar_inventario,style="botonEstilo.TButton")
        self.boton_exportar.grid(row=3,column=1,padx=10,pady=10,sticky="nsew")

        # Creacion de tabla ----------------------------------------------------
        self.tabla = ttk.Treeview(self.Frame2, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings")
        self.tabla.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10,pady=5)

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

    def mostrar_ventana_formulario(self, modo="agregar",datos=None):
        if datos is None:
            messagebox.showinfo("Notificacion", "Primero debe escoger una celda")
            return

        def guardar_datos():
            nombre = entrada1.get()
            cantidad = int(entrada2.get())
            precio = entrada3.get()
            if modo == "agregar":
                from BookManager.Controlador.AdministradorControlador import Administrador
                if nombre and cantidad and precio:
                    admin = Administrador()
                    admin.agregarProducto(nombre,cantidad,precio)
                    self.actualizarTabla()
            elif modo == "modificar":
                if nombre == datos[1] and cantidad == datos[2] and precio == datos[3]:
                    messagebox.showinfo("Sin cambios", "No se realizaron cambios en los datos.")
                    return
                if nombre and cantidad and precio:

                    from BookManager.Data.ConexionBD import ConexionBD

                    self.conexion_bd = ConexionBD().conexion_inventario()
                    if not self.conexion_bd:
                        print("Conexión a la base de datos fallida.")

                    cursor = self.conexion_bd.cursor()
                    cursor.execute("UPDATE inventario SET nombre=?, cantidad = ?, precio=? WHERE idProducto = ?", (nombre, cantidad, precio, datos[0]))
                    self.conexion_bd.commit()
                    cursor.close()
                    print(f"Cantidad actualizada para el producto '{nombre}'.")
                    self.actualizarTabla()
                else:
                    print("Ha ocurrido un error")

            ventana_formulario.destroy()  # Cerrar la ventana


        ventana_formulario = tk.Toplevel(self)
        ventana_formulario.title("Formulario de Inventario")

        # Configurar tamaño de la ventana
        ventana_formulario.geometry("400x300")

        # Etiquetas y campos de entrada
        etiquetas = ["Nombre", "Cantidad", "Precio"]
        for i,etiqueta in zip(range(1,len(etiquetas)+1),etiquetas):
            boton = ttk.Button(ventana_formulario, text=etiqueta)
            boton.grid(row=i,column=0)

        entrada1 = ttk.Entry(ventana_formulario,font=("Arial", 14)) # Entrada
        entrada1.grid(row=1,column=1)
        entrada2 = ttk.Entry(ventana_formulario, font=("Arial", 14)) # Cantidad
        entrada2.grid(row=2, column=1)
        entrada3 = ttk.Entry(ventana_formulario, font=("Arial", 14)) # Precio
        entrada3.grid(row=3, column=1)

        if modo == "modificar":
            entrada1.insert(0, datos[1])
            entrada2.insert(0, datos[2])
            entrada3.insert(0, datos[3])

        boton_guardar = ttk.Button(ventana_formulario, text="Guardar datos", command=guardar_datos)
        boton_guardar.grid(row=4, column=1, sticky="ew")

        # Botón para guardar los datos

    def agregar(self):
        self.mostrar_ventana_formulario(modo="agregar")
    def modificar(self):
        valores = self.obtener_fila_seleccionada()
        self.mostrar_ventana_formulario(modo="modificar", datos=valores)
    def eliminar(self):
        pass
    def exportar_inventario(self):
        pass

    def obtener_fila_seleccionada(self):
        # Obtiene la fila seleccionada en la tabla
        seleccion = self.tabla.focus()  # Obtiene la clave del elemento seleccionado
        if seleccion:
            valores = self.tabla.item(seleccion, "values")  # Obtiene los valores de la fila seleccionada
            return valores
        return None

    def actualizarTabla(self):
        for item in self.tabla.get_children():  # Obtener todos los elementos de la tabla
            self.tabla.delete(item)  # Eliminar cada elemento
        self.cargarTabla()



if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Inventario() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos