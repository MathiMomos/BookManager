from tkinter import Tk, StringVar
from tkinter import ttk
from BookManager.BookManager.Vista.Vendedor.Vender import Vender

import sqlite3
import hashlib

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")

        self.var_rol = StringVar(value="Vendedor")

        ttk.Label(self, text="Usuario:").pack(pady=5)
        self.entrada_usuario = ttk.Entry(self)
        self.entrada_usuario.pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=5)
        self.entrada_contrasenia = ttk.Entry(self, show="*")
        self.entrada_contrasenia.pack(pady=5)

        ttk.Label(self, text="Rol:").pack(pady=5)
        ttk.Radiobutton(self, text="Administrador", variable=self.var_rol, value="admin").pack()
        ttk.Radiobutton(self, text="Vendedor", variable=self.var_rol, value="usuario").pack()

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.entrada_usuario.get()
        password = self.entrada_contrasenia.get()
        role = self.var_rol.get()

        if self.validar_credenciales(username, password, role):
            self.withdraw()  # Oculta la ventana de Login en lugar de destruirla
            if role == "admin":
                print("Administrador")
            elif role == "usuario":
                self.abrir_interfaz_vendedor()
            else:
                print("Rol no válido")

    def validar_credenciales(self, username, password, role):
        # Conexión a la base de datos
        conexion = sqlite3.connect(r'C:\Users\USER\PortafolioUNMSM\Estructura de datos\Proyecto\BookManager\BookManager\Data\users.db')
        cursor = conexion.cursor() #Para poder ejecutar los comandos

        # Consulta a la base de datos
        cursor.execute("SELECT * FROM users WHERE username = ? AND role = ?", (username, role))
        resultado = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        if resultado :
            contrasenia_almacenada = resultado[2]
            # Comparamos la contraseña ingresada con la almacenada
            contrasenia_hash = hashlib.sha256(password.encode()).hexdigest()
            if contrasenia_hash == contrasenia_almacenada:
                return True
        return False

    def abrir_interfaz_vendedor(self):
        app = Vender()
        app.mainloop()

if __name__ == "__main__":
    login_app = Login()
    login_app.mainloop()
