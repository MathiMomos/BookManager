import os
from tkinter import Tk, StringVar, messagebox
from tkinter import ttk
from BookManager.Vista.Vendedor.Vender import Vender

import sqlite3
import hashlib

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")
        self.center_window()

        ttk.Label(self, text="Usuario:").pack(pady=5)
        self.entrada_usuario = ttk.Entry(self)
        self.entrada_usuario.pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=5)
        self.entrada_contrasenia = ttk.Entry(self, show="*")
        self.entrada_contrasenia.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        username = self.entrada_usuario.get()
        password = self.entrada_contrasenia.get()

        rol = self.validar_credenciales(username, password)
        if rol:
            self.withdraw()  # Oculta la ventana de Login en lugar de destruirla
            if rol == "admin":
                # Parte de Luis (Administrador)
                print("Administrador")
            elif rol == "usuario":
                self.abrir_interfaz_vendedor()
            else:
                print("Rol no válido")
        else:
            messagebox.showerror("Error de Login", "Credenciales inválidas. Por favor, inténtelo de nuevo.")

    def validar_credenciales(self, username, password):
        # Obtener la ruta de la base de datos
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_ruta = os.path.join(base_dir, "..", "Data", "users.db")

        # Conexión a la base de datos
        conexion = sqlite3.connect(db_ruta)
        cursor = conexion.cursor()  # Para poder ejecutar los comandos

        # Consulta a la base de datos
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        resultado = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        if resultado:
            contrasenia_almacenada = resultado[2]
            rol = resultado[3]
            # Comparamos la contraseña ingresada con la almacenada
            contrasenia_hash = hashlib.sha256(password.encode()).hexdigest()
            if contrasenia_hash == contrasenia_almacenada:
                return rol
        return None

    def abrir_interfaz_vendedor(self):
        app = Vender()
        app.mainloop()

if __name__ == "__main__":
    login_app = Login()
    login_app.mainloop()
