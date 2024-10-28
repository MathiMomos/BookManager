import sqlite3
import hashlib

def connect_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL)''')
    connection.commit()
    return connection

# HASH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# LOGIN
def login(username, password):
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = hash_password(password)
        if result[0] == hashed_password:
            print(f"Inicio de sesion exitoso. Bienvenido {username} ({result[1]})")
            connection.close()
            return True
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no encontrado")
    
    connection.close()
    return False

# NUEVO USUARIO (ADMIN)
def add_user(admin, new_user, password, role):
    if check_role(admin, 'admin'):
        connection = connect_db()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (new_user, hash_password(password), role))
            connection.commit()
            print(f"Se anadio al usuario {new_user} con rol {role}.")
        except sqlite3.IntegrityError:
            print("Error: El usuario ya existe.")
        
        connection.close()
    else:
        print("Solo los administradores pueden agregar usuarios.")

# BORRAR USUARIO (ADMIN)
def delete_user(admin, user_to_delete):
    if check_role(admin, 'admin'):
        connection = connect_db()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
        if cursor.rowcount > 0:
            connection.commit()
            print(f"El usuario {user_to_delete} fue eliminado.")
        else:
            print("Error: El usuario no existe.")
        
        connection.close()
    else:
        print("Solo los administradores pueden eliminar usuarios.")

# CAMBIAR CONTRASENA
def change_password(username, current_password, new_password):
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_current_password = hash_password(current_password)
        if result[0] == hashed_current_password:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", 
                           (hash_password(new_password), username))
            connection.commit()
            print(f"La contrasena para {username} se cambio.")
        else:
            print("Contrasena actual incorrecta.")
    else:
        print("Usuario no encontrado.")
    
    connection.close()

# MOSTRAR USUARIOS
def show_users(admin):
    if check_role(admin, 'admin'):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        
        for username, role in users:
            print(f"Usuario: {username}, Rol: {role}")
        
        connection.close()
    else:
        print("Solo los administradores pueden ver la lista de usuarios.")

# COMPROBAR ROL
def check_role(username, required_role):
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    connection.close()
    
    if result and result[0] == required_role:
        return True
    return False

# ADMIN USER inicial
def create_initial_admin():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', hash_password('admin123'), 'admin'))
        connection.commit()
        print("Initial admin created: username 'admin', password 'admin123'")

    connection.close()
