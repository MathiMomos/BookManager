from tkinter import Tk, StringVar
from tkinter import ttk
from BookManager.BookManager.Vista.Vendedor.Vender import Vender

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")

        self.role_var = StringVar(value="Vendedor")

        ttk.Label(self, text="Usuario:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Label(self, text="Rol:").pack(pady=5)
        ttk.Radiobutton(self, text="Administrador", variable=self.role_var, value="Administrador").pack()
        ttk.Radiobutton(self, text="Vendedor", variable=self.role_var, value="Vendedor").pack()

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if self.validate_credentials(username, password, role):
            self.withdraw()  # Oculta la ventana de Login en lugar de destruirla
            if role == "Administrador":
                print("Administrador")
            else:
                self.open_vendedor_interface()

    def validate_credentials(self, username, password, role):
        # Aquí puedes agregar la lógica para validar las credenciales
        return True

    def open_vendedor_interface(self):
        app = Vender()
        app.mainloop()

if __name__ == "__main__":
    login_app = Login()
    login_app.mainloop()
