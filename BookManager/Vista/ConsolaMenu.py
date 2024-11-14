from BookManager.Controlador.VentasControlador import VentasControlador
from BookManager.Controlador.VendedorControlador import VendedorControlador
from BookManager.Controlador.AdministradorControlador import Administrador


class ConsolaMenu:
    
    def __init__(self):
        self.objetoVendedor = VendedorControlador()
        self.objetoAdministrador = Administrador()
    
    def consolaLogin(self):
        
        while(True):
            print("Iniciar sesion")
            
            #usuario_objeto = Usuario() # Esto viene de usuario controlador
            
            # Simular un login por consola
                
            contrasenia = input("Ingresa tu contrasenia: ")
            rol = input("Ingresa tu rol: ")
            contra_bd = "admin123"
                
            if contrasenia == contra_bd and rol == "administrador" :
                print("Bienvenido Administrador (Nombre)")
                break
            elif contrasenia == contra_bd and rol == "vendedor":
                print("Inicio sesion como vendedor")
                break
            else:
                print("Credenciales incorrectas, intente nuevamente :)")
            
        # Depende del rol abrirá una consola que le corresponda
        if rol == "administrador":
            self.menuAdministrador()
        elif rol == "vendedor":
            self.menuVendedor()
        else:
            print("Rol no existe")

    
    
    # ----------------------------------------------------------------
    
    # Administrador
    
    def menuAdministrador(self):
        
        global opcion
        while(True):
            print("1. Vender Producto")
            print("2. Ver historial de ventas")
            print("3. Ver estadisticas")
            print("4. Gestionar inventario")
            print("5. Ver disponibilidad de productos") # Ver productos
            print("6. Reembolso")
            print("7. Crear usuario")
            print("0. Salir")
            try:
                opcion = int(input("Digite una opcion: "))
            except ValueError as error:
                print(f"Error...Ingresa un numero. {error}")
            
            if opcion == 1:
                print("Vender producto")
                self.venderProducto()
            elif opcion == 2:
                print("Ver historial de ventas")
                self.verHistorialDeVentas()
            elif opcion == 3:
                print("Ver estadisticas")
                self.verEstadisticas()
            elif opcion == 4:
                print("Gestionar inventario")
                self.gestionarInventario()
            elif opcion == 5:
                print("Ver disponibilidad")
                self.verDisponibilidad()
            elif opcion == 6:
                print("Reembolso")
                self.reembolso()
            elif opcion == 7:
                print("Crear cuenta vendedor")
                self.crearUsuario()
            elif opcion == 0:
                print("Saliendo del programa")
                break
            else:
                print("Opcion no válida...")
                
        # menu con while
    
    # Opcion 1
    def venderProducto(self):
        self.objetoAdministrador.mostrar_productos()
        id_producto = int(input("Ingrese el ID del producto: "))
        cantidad = int(input("Ingrese la cantidad a vender: "))
        self.objetoAdministrador.vender_producto(id_producto, cantidad)
        
    # Opcion 2
    def verHistorialDeVentas(self):
        print("===============Ventas================")
        self.objetoAdministrador.ver_historial_ventas()
        
    # Opcion 3
    def verEstadisticas(self):
        print("Generando reporte de estadísticas...")
        
        objetoVentasControlador = VentasControlador()
        objetoVentasControlador.generar_reporte_ventas()
        
        print("Reporte generado exitosamente: 'reporte_ventas.pdf'")

    # Opcion 4
    def gestionarInventario(self):
        self.objetoAdministrador.gestionarInventario()
    
    # Opcion 5
    def verDisponibilidad(self):
        id_producto = int(input("Ingrese el ID del producto: "))
        producto = self.objetoAdministrador.ver_disponibilidad(id_producto)
        idex,cantidad,precio,nombre = producto
        
        print(f"El producto {nombre} cuenta con {cantidad} unidade(s)")
    
    # Opcion 6
    def reembolso(self):
        pass
    
    # Opcion 7
    def crearUsuario(self):
        pass
    
    # --------------------------------------------------------
    # Vendedor
    
    def menuVendedor(self):
        global opcion
        while(True):
            print("1. Vender Producto")
            print("2. Ver historial de ventas")
            print("3. Ver disponibilidad de productos") # Ver productos
            print("4. Reembolso")
            print("0. Salir")
            try:

                opcion = int(input("Digite una opcion: "))
            except ValueError as error:
                print(f"Error... Ingresa un numero: {error}")
            
            if opcion == 1:
                print("Vender producto")
                self.venderProductoVendedor()
            elif opcion == 2:
                print("Ver historial de ventas")
                self.verHistorialDeVentas()
            elif opcion == 3:
                print("Ver disponibilidad")
                self.verDisponibilidad()
            elif opcion == 4:
                print("Reembolso")
                self.reembolso()
            elif opcion == 0:
                print("Saliendo del programa")
                break
            else:
                print("Opcion no válida...")
                
        # menu con while
        
    def venderProductoVendedor(self):
        
        self.objetoVendedor.mostrar_productos()
        id_producto = int(input("Ingrese el ID del producto: "))
        cantidad = int(input("Ingrese la cantidad a vender: "))
        
        self.objetoVendedor.vender_producto(id_producto, cantidad)

    def verHistorialVendedor(self):
        print("===============Ventas================")
        self.objetoVendedor.ver_historial_ventas()

    def verDisponibilidadVendedor(self):
        id_producto = int(input("Ingrese el ID del producto: "))
        self.objetoVendedor.ver_disponibilidad(id_producto)

    def reembolsarVendedor(self):
        self.verHistorialVendedor()
        id_venta = int(input("Ingrese la ID de la venta realizada a reembolsar para añadir a la cola"))
        self.objetoVendedor.solicitar_reembolso(id_venta)
        self.objetoVendedor.realizar_reembolso()



        