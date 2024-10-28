import sqlite3

class ConexionBD:
    
    def conexion_usuarios(self):
        pass
    
    def conexion_inventario(self):
        pass
    
    def conexion_ventas(self):
        conexion = sqlite3.connect("BookManager\\Data\\ventas.db")
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
objeto = ConexionBD()
db = objeto.conexion_ventas()
cursor = db.cursor()
sql = "INSERT INTO ventas VALUES (?,?,?,?,?,?)"
valores = (None, "CUADERNO", 240,1200,"27/10/2024","20:15")
cursor.execute(sql,valores)
db.commit()
cursor.close()
db.close()