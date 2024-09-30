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
            print(f"Login successful. Welcome {username} ({result[1]})")
            connection.close()
            return True
        else:
            print("Incorrect password")
    else:
        print("User not found")
    
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
            print(f"User {new_user} with role {role} added successfully.")
        except sqlite3.IntegrityError:
            print("Error: The user already exists.")
        
        connection.close()
    else:
        print("Only admins can add new users.")

# BORRAR USUARIO (ADMIN)
def delete_user(admin, user_to_delete):
    if check_role(admin, 'admin'):
        connection = connect_db()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
        if cursor.rowcount > 0:
            connection.commit()
            print(f"User {user_to_delete} deleted successfully.")
        else:
            print("User does not exist.")
        
        connection.close()
    else:
        print("Only admins can delete users.")

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
            print(f"Password successfully changed for user {username}.")
        else:
            print("Current password is incorrect.")
    else:
        print("User not found.")
    
    connection.close()

# MOSTRAR USUARIOS
def show_users(admin):
    if check_role(admin, 'admin'):
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        
        for username, role in users:
            print(f"User: {username}, Role: {role}")
        
        connection.close()
    else:
        print("Only admins can view the list of users.")

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
