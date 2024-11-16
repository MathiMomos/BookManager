# MenuLateral.py
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font

class MenuLateral(tk.Frame):
    def __init__(self, parent, cambiar_pestaña_callback, directorio_base):
        super().__init__(parent, bg="#e0e0e0")

        # Colores y fuente del menú
        self.color_menu_predeterminado = "#e0e0e0"
        self.color_menu_activo = "#d0d0ff"
        self.fuente_menu = font.Font(family="Arial", size=12, weight="bold")

        # Cargar los íconos
        rutas_iconos = {
            "Inicio": os.path.join(directorio_base, "iconos", "casa.png"),
            "Vender": os.path.join(directorio_base, "iconos", "carrito-de-compras.png"),
            "Historial de ventas": os.path.join(directorio_base, "iconos", "notas.png"),
            "Ver inventario": os.path.join(directorio_base, "iconos", "caja.png"),
            "Salir": os.path.join(directorio_base, "iconos", "salir.png")
        }

        self.icons = {}
        for key, path in rutas_iconos.items():
            if os.path.exists(path):
                self.icons[key] = ImageTk.PhotoImage(Image.open(path).resize((24, 24)))
            else:
                print(f"Error: El archivo de ícono '{path}' no existe.")
                self.icons[key] = None

        # Crear botones de menú
        self.cambiar_pestaña_callback = cambiar_pestaña_callback
        elementos_menu = ["Inicio", "Vender", "Historial de ventas", "Ver inventario"]
        self.botones_menu = {}

        for item in elementos_menu:
            button = tk.Button(
                self,
                text=item,
                image=self.icons.get(item),
                compound="left",
                bg=self.color_menu_predeterminado,
                relief="flat",
                anchor="w",
                padx=20,
                font=self.fuente_menu,
                command=lambda i=item: self.cambiar_pestaña_callback(i)
            )
            button.pack(fill="x", pady=5, ipady=5, anchor="center")
            self.botones_menu[item] = button

        # Botón de salir
        salir_button = tk.Button(
            self,
            text="Salir",
            image=self.icons.get("Salir"),
            compound="left",
            bg=self.color_menu_predeterminado,
            relief="flat",
            anchor="w",
            padx=10,
            font=self.fuente_menu,
            command=self.volver_a_login
        )
        salir_button.pack(side="bottom", fill="x", pady=5, ipady=5)

    def cambiar_color_pestaña(self, pestaña):
        # Restaurar el color de todas las pestañas
        for item, button in self.botones_menu.items():
            button.config(bg=self.color_menu_predeterminado)

        # Cambiar el color de la pestaña activa
        if pestaña in self.botones_menu:
            self.botones_menu[pestaña].config(bg=self.color_menu_activo)

    def volver_a_login(self):
        self.master.destroy()
        from BookManager.BookManager.Vista.Login import Login
        login_app = Login()
        login_app.mainloop()
