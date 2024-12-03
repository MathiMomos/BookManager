import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class PlantillaAdministrador(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.imagenes_cargadas = None
        self.configurar_interfaz()
        self.crear_widgets()

    def configurar_interfaz(self):
        ancho = 1000
        alto = 600

        # Esto es para centrar la pantalla
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        # Configurar la ventana principal

        posicion_x = int((pantalla_ancho - ancho) / 2)
        posicion_y = int((pantalla_alto - alto) / 2)

        self.title("ADMINISTRADOR")
        self.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")  # Tamaño de la ventana
        self.configure(background="white")

        # Definimos la grilla de la ventana
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=5)

    def crear_widgets(self):
        # Crear widgets ttk y colocarlos

        # CREANDO ESTILOS ---------------------------------------------------
        estilo = ttk.Style()
        estilo.theme_use("clam")
            # Crear un estilo para cambiar el fondo del Frame1

        estilo.configure("MiFrame.TFrame", background=("#%02x%02x%02x" % (224,224,224)))

            # Crear un estilo para los botones del panel de opciones

        # Configurar el estilo normal
        estilo.configure("MiBoton.TButton",
                         background="#f0f2fa",  # Color de fondo normal
                         foreground="black",  # Color del texto
                         font=("Arial", 16, "bold"),
                        borderwidth = 0,  # Eliminar el borde
                        relief = "flat" # Eliminar el relieve (bordes)
                         )
        estilo.configure("MiBoton_salir.TButton",
                         background="#f0f2fa",  # Color de fondo normal
                         foreground="black",  # Color del texto
                         font=("Arial", 16, "bold"),
                         borderwidth=0,  # Eliminar el borde
                         relief="flat"  # Eliminar el relieve (bordes)
                         )

        # Configurar el estilo cuando el botón es presionado (estado 'pressed')
        estilo.map("MiBoton.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#9090fa"), ("active", "#d0d0ff")] # Cambia el color de fondo al presionar
                   )
        estilo.map("MiBoton_salir.TButton",
                   foreground=[("pressed", "black"), ("active", "black")],  # Cambia el color del texto al presionar
                   background=[("pressed", "#ff8080"), ("active", "#ffd0d0")] # Cambia el color de fondo al presionar
                   )
        #CREANDO WIDGETS ---------------------------------------------

        #Creacion de Frame1 --------------------------- donde estara el panel de opciones
        self.Frame1 = ttk.Frame(self,style="MiFrame.TFrame")
        self.Frame1.grid(row=0, column=0, sticky="nsew")

        # El frame tendra 9 filas y 1 columna
        for i in range(0,9,1):
            self.Frame1.rowconfigure(i,weight=1)
        self.Frame1.columnconfigure(0,weight=1)


        #Creacion de los botones -----------------------------------------

        self.cargar_imagenes_panel_opciones()
        lista_nombres_botones = ["Inicio", "Inventario", "Vender", "Historial de ventas", "Estadisticas", "Vendedores"]
        lista_nombres_comandos = [self.goInicio,self.goInventario,self.goVender,self.goHistorialDeVentas,self.goEstadisticas,self.goVendedores]

        # Generando los botones del panel de opciones
        for i,nombre,comando in zip(range(1,len(lista_nombres_botones)+1),lista_nombres_botones,lista_nombres_comandos):
            self.Boton = ttk.Button(self.Frame1,text=nombre,style="MiBoton.TButton",compound="left",image = self.imagenes_cargadas[i-1],command=comando)
            self.Boton.grid(row=i,column=0,sticky="nsew")

        self.Boton7 = ttk.Button(self.Frame1, text="Salir", style="MiBoton_salir.TButton", compound="left",image = self.imagenes_cargadas[6],command=self.goSalir)
        self.Boton7.grid(row=7, column=0, sticky="nsew")

        # CREACION DE LAS ETIQUETAS ------------------------------------

        self.Label1 = ttk.Label(self.Frame1, text="Libreria La Hoja", font=("Comic Sans", 12, "bold"), foreground="#757575")
        self.Label1.grid(row=0,column=0)

    def cargar_imagenes_panel_opciones(self):

        directorio_base = os.path.dirname(os.path.abspath(__file__))
        ruta_base = os.path.join(directorio_base, "Iconos", "panel_de_opciones")

        # Lista con los nombres de archivos de las imágenes
        imagenes_nombres = ["Inicio.png", "Inventario.png", "Vender.png",
                            "Historial.png", "Estadisticas.png", "Vendedores.png", "Salir.png"]

        self.imagenes_cargadas = []  # Lista para almacenar las imágenes cargadas

        for nombre in imagenes_nombres:
            try:
                ruta_imagen = os.path.join(ruta_base, nombre)
                print(f"Cargando: {ruta_imagen}")  # Línea para depuración
                img = Image.open(ruta_imagen).resize((24, 24), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.imagenes_cargadas.append(img_tk)
            except Exception as e:
                print(f"Error al cargar la imagen '{nombre}': {e}")

        return self.imagenes_cargadas
    def goInicio(self):
        from BookManager.Vista.Administrador.Inicio import Inicio
        self.destroy()
        objetoInicio = Inicio()
        objetoInicio.mainloop()

    def goInventario(self):
        from BookManager.Vista.Administrador.Inventario import Inventario
        self.destroy()
        objetoInventario = Inventario()
        objetoInventario.mainloop()

    def goVender(self):
        from BookManager.Vista.Administrador.Vender import Vender
        self.destroy()
        objetoVender = Vender()
        objetoVender.mainloop()

    def goHistorialDeVentas(self):
        from BookManager.Vista.Administrador.Historial import Historial
        self.destroy()
        objetoHistorial = Historial()
        objetoHistorial.mainloop()

    def goEstadisticas(self):
        from BookManager.Vista.Administrador.Estadisticas import Estadisticas
        self.destroy()
        objetoEstadistica = Estadisticas()
        objetoEstadistica.mainloop()

    def goVendedores(self):
        from BookManager.Vista.Administrador.Vendedores import Vendedores
        self.destroy()
        objetoVendedores = Vendedores()
        objetoVendedores.mainloop()

    def goSalir(self):
        respuesta = messagebox.askyesno("Confirmación", "¿Está seguro que desea salir?")
        if respuesta:
            self.destroy()
            from BookManager.Vista.Login import Login
            inicio_login = Login()
            inicio_login.mainloop()
        else:
            return





if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = PlantillaAdministrador()  # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos

