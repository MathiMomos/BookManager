# fabien
from archivosAnteriores import user_management
class Usuario:
    def __init__(self, nombreUsuario, contraseña, rol="user"):
        self.nombreUsuario = nombreUsuario
        self.contraseñaHash = user_management.hash_password(contraseña)
        self.rol = rol
        self.sesion_activa = False

    # Método para obtener el nombre de usuario
    def getUsuario(self):
        return self.nombreUsuario

    # Método para cambiar el nombre de usuario
    def setNombreUsuario(self, nombreUsuario):
        self.nombreUsuario = nombreUsuario

    # Método para obtener el rol
    def getRol(self):
        return self.rol

    # Método para cambiar la contraseña
    def setContraseña(self, nueva_contraseña):
        self.contraseñaHash = user_management.hash_password(nueva_contraseña)
        user_management.change_password(self.nombreUsuario, nueva_contraseña, nueva_contraseña)
        print("Contraseña actualizada.")

    # Método para iniciar sesión
    def iniciarSesion(self):
        if user_management.login(self.nombreUsuario, self.contraseñaHash):
            self.sesion_activa = True
            return True
        else:
            self.sesion_activa = False
            return False

    # Método para cerrar sesión
    def cerrarSesion(self):
        if self.sesion_activa:
            self.sesion_activa = False
            print(f"{self.nombreUsuario} ha cerrado sesión.")
        else:
            print("La sesión ya está cerrada.")