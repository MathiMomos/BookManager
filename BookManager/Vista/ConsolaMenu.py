from BookManager.Controlador.AdministradorControlador import Administrador
#from BookManager.Controlador.UsuarioControlador import Usuario
from BookManager.Controlador.VentasControlador import VentasControlador
#INTEGRACIÓN INVENTARIO CONTROLADOR:
from BookManager.Controlador.InventarioControlador import InventarioControlador

class ConsolaMenu:
    def __init__(self):
        self.controlador = VentasControlador()  # Inicializar el controlador

    def consolaLogin(self):
        
        global rol
        
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
    
    #INVENTARIO CONTROLADOR:
    def __init__(self):
        self.controlador_inventario = InventarioControlador()  # Inicializar controlador de inventario

    def gestionarInventario(self):
        while(True):
            print("1. Agregar producto")
            print("2. Eliminar producto")
            print("3. Modificar producto")
            print("4. Buscar producto")
            print("0. Volver")
            try:
                opcion = int(input("Ingrese su opcion: "))
            except ValueError as error:
                print(f"Opcion invalida. Error {error}")
        
            if opcion == 1:
                self.agregarProducto()
            elif opcion == 2:
                self.eliminarProducto()
            elif opcion == 3:
                self.modificarProducto()
            elif opcion == 4:
                self.buscarProducto()
            elif opcion == 0:
                print("Volviendo")
                break

    def agregarProducto(self):
        nombre = input("Nombre del producto: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        descripcion = input("Descripción: ")
        self.controlador_inventario.agregarProducto(nombre, cantidad, precio, descripcion)

    def eliminarProducto(self):
        nombre = input("Nombre del producto a eliminar: ")
        self.controlador_inventario.eliminarProducto(nombre)

    def modificarProducto(self):
        nombre = input("Nombre del producto a modificar: ")
        nueva_cantidad = int(input("Nueva cantidad: "))
        self.controlador_inventario.modificarProducto(nombre, nueva_cantidad)

    def buscarProducto(self):
        nombre = input("Nombre del producto a buscar: ")
        self.controlador_inventario.buscarProducto(nombre)
    
    # ----------------------------------------------------------------
    
    # Administrador
    
    def menuAdministrador(self):
        
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
        administrador = Administrador("Admin_1,", "Apellido_1")
        administrador.venderProducto()
    
    # Opcion 2
    def verHistorialDeVentas(self):
        pass
    
    # Opcion 3
    def verEstadisticas(self):
        print("Generando reporte de estadísticas...")
        self.controlador.generar_reporte_ventas()
        print("Reporte generado exitosamente: 'reporte_ventas.pdf'")

    # Opcion 4
    def gestionarInventario(self):
        
        while(True):
            print("1. Agregar producto")
            print("2. Eliminar producto")
            print("3. Modificar producto")
            print("4. Buscar producto")
            print("0. Volver")
            try:
                opcion = int(input("Ingrese su opcion: "))
            except ValueError as error:
                print(f"Opcion invalida. Error {error}")
        
            if opcion == 1:
                self.agregarProducto()
            elif opcion == 2:
                self.eliminarProducto()
            elif opcion == 3:
                self.modificarProducto()
            elif opcion == 4:
                self.buscarProducto()
            elif opcion == 0:
                print("Volviendo")
                break
        
    # Opcion 4.1
    def agregarProducto(self):
        print("Agregar producto")
    def eliminarProducto(self):
        print("Eliminar producto")
    def modificarProducto(self):
        print("Modificar producto")
    def buscarProducto(self):
        print("Buscar producto")
    
    # Opcion 5
    def verDisponibilidad(self):
        pass
    
    # Opcion 6
    def reembolso(self):
        pass
    
    # Opcion 7
    def crearUsuario(self):
        pass
    
    # --------------------------------------------------------
    # Vendedor
    
    def menuVendedor(self):
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
                self.venderProducto()
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
        
    
    