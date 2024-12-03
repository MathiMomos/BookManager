from tkinter import ttk

from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador
import tkinter as tk
from tkinter import messagebox

class Vendedores(PlantillaAdministrador):
    def __init__(self):
        super().__init__()
        self.agregar_mas_widgets()

    def agregar_mas_widgets(self):
        # Aqui van los estilos
        estilo = ttk.Style()
        estilo.theme_use("clam")
        # Estilos para las etiquetas de titulo
        estilo.configure(
            "etiquetaTitulo.TLabel",
            foreground="Gray",  # Color del texto

            font=("Helvetica", 16, "bold"),  # Tipo de fuente, tamaño, y estilo (negrita)
        )
        # Este es para el boton de agregar
        estilo.configure(
            "botonAgregar.TButton",
            background="#f0f0f0",  # Color de fondo normal (Verde)
            foreground="black",  # Color del texto
            font=("Arial", 16, "bold"),
            borderwidth=0,  # Eliminar el borde
            relief="flat"  # Eliminar el relieve (bordes)
        )
        estilo.map("botonAgregar.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#88c659"), ("active", "#b8d7a1")]  # Cambia el color de fondo al presionar
        )
        # Para el boton de eliminar
        estilo.configure(
            "botonEliminar.TButton",
            background="#ffb2a2",  # Color de fondo normal
            foreground="black",  # Color del texto
            font=("Arial", 16, "bold"),
            borderwidth=0,  # Eliminar el borde
            relief="flat"  # Eliminar el relieve (bordes)
        )
        estilo.map("botonEliminar.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#c87644"), ("active", "#e5b79b")]  # Cambia el color de fondo al presionar
        )
        # para el boton de editar
        estilo.configure(
            "botonEditar.TButton",
            background="#edab64",  # Color de fondo normal
            foreground="black",  # Color del texto
            font=("Arial", 16, "bold"),
            borderwidth=0,  # Eliminar el borde
            relief="flat"  # Eliminar el relieve (bordes)
        )
        estilo.map("botonEditar.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#bd7629"), ("active", "#d39756")]  # Cambia el color de fondo al presionar
                   )
        # Estilos para las tablas
        estilo.configure('Treeview',
                         font=("Helvetica", 14),
                         rowheight=30)
        estilo.map('Treeview', background=[('selected', '#948ad1')])
        #Para el combobox
        estilo.configure(
            "EstiloComboBox.TCombobox",
            foreground="#000000",  # Verde para el texto
            background="#F5F5F5",  # Gris claro para el desplegable
            fieldbackground="#FFFFFF",  # Blanco para el campo de texto
            font=("Arial", 12),
            padding=5,
            borderwidth=2,
            relief="solid"  # Tipo de borde (solid, groove, etc.)
        )
        # para etiquetas de texto
        estilo.configure(
            "etiquetaTexto.TLabel",
            foreground="black",  # Color del texto
            background="#e1f5d2",  # Fondo verde
            font=("Helvetica", 14),  # Fuente, tamaño
            padding=10  # Relleno interno
        )

        # Creacion del frame 2
        self.Frame2 = ttk.Frame(self)
        self.Frame2.grid(row=0,column=1, sticky="nsew")

        self.Frame2.rowconfigure(0, weight=1)
        self.Frame2.rowconfigure(1,weight=8)
        self.Frame2.rowconfigure(2,weight=1)
        self.Frame2.columnconfigure(0, weight=1)
        self.Frame2.columnconfigure(1,weight=1)
        self.Frame2.columnconfigure(2,weight=1)

        # Cargando etiquetas
        self.etiquetaUsuarios = ttk.Label(self.Frame2, text = "Usuarios",style="etiquetaTitulo.TLabel")
        self.etiquetaUsuarios.grid(row = 0, column = 0, columnspan=3)

        #Cargando boton de agregar Usuarios
        self.botonUsuarios = ttk.Button(self.Frame2,text="Agregar usuarios", command=self.agregarUsuarios, style="botonAgregar.TButton")
        self.botonUsuarios.grid(row=2,column=2, sticky="nsew", padx=10,pady=10)

        #Cargando boton de eliminar Usuarios
        self.eliminarUsuarios = ttk.Button(self.Frame2,text="Eliminar Usuario", command =  self.eliminarUsuario, style="botonEliminar.TButton")
        self.eliminarUsuarios.grid(row=2,column=1, sticky="nsew", padx=10,pady=10)
        # cargando boton de editar usuario
        self.editarUsuarios = ttk.Button(self.Frame2, text="Editar Usuario", command=self.editarUsuario, style="botonEditar.TButton")
        self.editarUsuarios.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        # Cargar la tabla usuarios
        self.crear_tabla_usuarios()

    def crear_tabla_usuarios(self):
        self.tabla = ttk.Treeview(self.Frame2,
                                  columns=("ID", "Usuario", "Contraseña", "Rol"),
                                  show="headings")
        self.tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5, columnspan=3)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Usuario", text="Usuario")
        self.tabla.heading("Contraseña", text="Contraseña")
        self.tabla.heading("Rol", text="Rol")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Usuario", width=150, anchor="w")
        self.tabla.column("Contraseña", width=100, anchor="w")
        self.tabla.column("Rol", width = 75, anchor="center")

        # Cargar los datos de la tabla
        self.cargar_tabla()

        # falta crear botones de agregar y modificar

    def cargar_tabla(self):
        from BookManager.Data.ConexionBD import ConexionBD
        self.conexion_bd = ConexionBD()
        conexion = self.conexion_bd.conexion_usuarios()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM users")
        self.ListaUsuarios = cursor.fetchall()

        # Agregar algunas filas a la tabla (por ejemplo)
        for id, nombre, contra, rol in self.ListaUsuarios:
            self.tabla.insert("", "end", values=(id, nombre, contra, rol))

    def agregarUsuarios(self):
        from archivosAnteriores.user_management import connect_db,add_user

        # Funciones para los botones
        def cancelar():
            mini_ventana.destroy()

        def agregarUsuario():
            admin_username = 'adminHoja'
            usuario = self.EntradaUsuario.get()
            password = self.EntradaPassword.get()
            rol = self.comboRol.get()

            if usuario and password and rol:
                add_user(admin_username, usuario, password, rol)
                messagebox.showinfo("Usuario", "Se ha agregado correctamente al usuario")
                mini_ventana.destroy()
                self.actualizarTabla()
            else:
                messagebox.showerror("Usuario", "Error al agregar al usuario")


        # Se creará una miniventana
        mini_ventana = tk.Toplevel(self)
        mini_ventana.title("Registrar usuario")
        mini_ventana.geometry("300x500")

        # Configurar el espacio de trabajo de la mini_ventana
        mini_ventana.rowconfigure(0,weight=1)
        mini_ventana.rowconfigure(1,weight=1)
        mini_ventana.rowconfigure(2,weight=1)
        mini_ventana.rowconfigure(3,weight=1)
        mini_ventana.columnconfigure(0,weight=1)
        mini_ventana.columnconfigure(1,weight=2)


        # Agregar widgets

        # Etiquetas
        self.lblUsuario = ttk.Label(mini_ventana, text="Nombre: ", style="etiquetaTexto.TLabel")
        self.lblUsuario.grid(row=0,column=0)

        self.lblPassword = ttk.Label(mini_ventana, text = "Contraseña: ", style="etiquetaTexto.TLabel")
        self.lblPassword.grid(row=1,column=0)

        self.lblRol = ttk.Label(mini_ventana, text="Escoja el rol: ", style="etiquetaTexto.TLabel")
        self.lblRol.grid(row=2,column=0)

        #       Combobox
        opciones = ["admin","usuario"]
        self.comboRol = ttk.Combobox(mini_ventana,values=opciones, state="readonly", style="EstiloComboBox.TCombobox")
        self.comboRol.set(opciones[1])
        self.comboRol.grid(row=2, column=1)

        #       Entradas
        self.EntradaUsuario = ttk.Entry(mini_ventana)
        self.EntradaUsuario.grid(row=0,column=1)

        self.EntradaPassword = ttk.Entry(mini_ventana, show="*")
        self.EntradaPassword.grid(row=1,column=1)



        #       Botones
        self.BotonAgregar = ttk.Button(mini_ventana, text="Agregar usuario", command=agregarUsuario)
        self.BotonAgregar.grid(row=3,column=1)

        self.BotonCancelar = ttk.Button(mini_ventana, text = "Cancelar", command=cancelar)
        self.BotonCancelar.grid(row=3,column=0)

    def actualizarTabla(self):
        for item in self.tabla.get_children():  # Obtener todos los elementos de la tabla
            self.tabla.delete(item)  # Eliminar cada elemento
        self.cargar_tabla()

    def editarUsuario(self):

        valores = self.obtener_fila_seleccionada()
        print(valores)
        if valores is None:
            messagebox.showinfo("Notificacion", "Primero debe escoger una celda")
            return

        def modificar():
            usuario = valores[1]
            contrasenia = EntradaPassword.get()
            nuevaContrasenia = EntradaNuevoPassword.get()


            if usuario and contrasenia:
                from archivosAnteriores.user_management import change_password

                change_password(usuario, contrasenia,nuevaContrasenia)
                messagebox.showinfo("Informacion", "Se ha cambiado la contraseña correctamente")
            else:
                messagebox.showerror("Error", "Intentelo otra vez")

        def cancelar():
            return

        # Se creará una miniventana
        mini_ventana = tk.Toplevel(self)
        mini_ventana.title("Registrar usuario")
        mini_ventana.geometry("300x500")

        # Configurar el espacio de trabajo de la mini_ventana
        mini_ventana.rowconfigure(0, weight=1)
        mini_ventana.rowconfigure(1, weight=1)
        mini_ventana.rowconfigure(2, weight=1)
        mini_ventana.rowconfigure(3, weight=1)
        mini_ventana.rowconfigure(4,weight=1)
        mini_ventana.columnconfigure(0, weight=1)
        mini_ventana.columnconfigure(1, weight=2)


        # Agregar widgets

        #       Etiquetas
        lblUsuario = ttk.Label(mini_ventana, text=f"Nombre: {valores[1]}", style="etiquetaTexto.TLabel")
        lblUsuario.grid(row=0, column=0)

        lblPassword = ttk.Label(mini_ventana, text="Contraseña actual: ", style="etiquetaTexto.TLabel")
        lblPassword.grid(row=1, column=0)

        lblNewPassword = ttk.Label(mini_ventana, text="Nueva contraseña: ", style="etiquetaTexto.TLabel")
        lblNewPassword.grid(row=2,column=0)

        EntradaPassword = ttk.Entry(mini_ventana)
        EntradaPassword.grid(row=1, column=1)


        EntradaNuevoPassword = ttk.Entry(mini_ventana)
        EntradaNuevoPassword.grid(row=2,column=1)

        #       Botones
        BotonAgregar = ttk.Button(mini_ventana, text="Guardar cambios", command=modificar)
        BotonAgregar.grid(row=3, column=1)

        BotonCancelar = ttk.Button(mini_ventana, text="Cancelar", command=cancelar)
        BotonCancelar.grid(row=3, column=0)


    def eliminarUsuario(self):
        from archivosAnteriores.user_management import delete_user
        seleccion = self.tabla.focus()  # Obtiene el ID de la fila seleccionada
        if seleccion:  # Verifica si hay una fila seleccionada
            valores = self.obtener_fila_seleccionada()
            respuesta = messagebox.askyesno("Confirmacion", "Esta seguro que desea eliminar?")
            if respuesta:
                self.tabla.delete(seleccion)  # Elimina la fila seleccionada
                delete_user('admin', valores[1])
                self.actualizarTabla()
            else:
                return

        else:
            messagebox.showwarning("Notificacion","No se ha seleccionado una celda")


    def obtener_fila_seleccionada(self):
        # Obtiene la fila seleccionada en la tabla
        seleccion = self.tabla.focus()  # Obtiene la clave del elemento seleccionado
        if seleccion:
            valores = self.tabla.item(seleccion, "values")  # Obtiene los valores de la fila seleccionada
            return valores
        return None





if __name__ == "__main__":
    root = tk.Tk()  #
    root.withdraw()
    app = Vendedores()
    app.mainloop()