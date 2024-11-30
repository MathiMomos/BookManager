import sqlite3
import os

class ConexionBD:

    def conexion_usuarios(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "users.db")
        conexion = sqlite3.connect(db_path)

        cursor = conexion.cursor()

        cursor.close()
        return conexion

    #CONEXION A BD INVENTARIO.DB:
    def conexion_inventario(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "inventario.db")
        conexion = sqlite3.connect(db_path)

        cursor = conexion.cursor()
        
        # Crear tabla productos si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            descripcion TEXT
        )""")
        
        cursor.close()
        return conexion
    
    def conexion_ventas(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "ventas.db")
        conexion = sqlite3.connect(db_path)
        
        cursor = conexion.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ventas (
            idPedido INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            cantidad INT,
            fecha TEXT NOT NULL,  -- formato 'YYYY-MM-DD',
            hora TEXT NOT NULL    -- formato 'HH:MM:SS
        )""")
        
        cursor.close()
        return conexion

# esto es para conectarse a la base de datos de ventas    
