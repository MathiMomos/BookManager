from BookManager.Vista.Administrador.PlantillaAdministrador import PlantillaAdministrador
import tkinter as tk

# Esta clase dejó de funcionar por que los ingresos se pueden ver en estadistica

class Caja(PlantillaAdministrador):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana raíz
    root.withdraw()  # Oculta la ventana principal si no quieres mostrarla
    app = Caja() # Crear la ventana `InicioAdministrador`
    app.mainloop()  # Ejecutar el bucle de eventos