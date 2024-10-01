import pandas as pd
import hashlib
import os

# Archivo Excel
FILENAME = 'users.xlsx'

# HASH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# CARGAR EXCEL
def load_users():
    if os.path.exists(FILENAME):
        return pd.read_excel(FILENAME, index_col=0)
    else:
        return pd.DataFrame(columns=['username', 'password', 'role'])

# GUARDAR
def save_users(users_df):
    users_df.to_excel(FILENAME)

# LOGIN
def login(username, password):
    users_df = load_users()
    if username in users_df.index:
        hashed_password = hash_password(password)
        if users_df.loc[username, 'password'] == hashed_password:
            print(f"Inicio de sesión exitoso. Bienvenido {username} ({users_df.loc[username, 'role']})")
            return True
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no encontrado")
    return False

# NUEVO USUARIO (ADMIN)
def add_user(admin, new_user, password, role):
    if check_role(admin, 'admin'):
        users_df = load_users()
        if new_user not in users_df.index:
            users_df.loc[new_user] = [hash_password(password), role]
            save_users(users_df)
            print(f"Se añadió al usuario {new_user} con rol {role}.")
        else:
            print("Error: El usuario ya existe.")
    else:
        print("Solo los administradores pueden agregar usuarios.")

# BORRAR USUARIO (ADMIN)
def delete_user(admin, user_to_delete):
    if check_role(admin, 'admin'):
        users_df = load_users()
        if user_to_delete in users_df.index:
            users_df.drop(user_to_delete, inplace=True)
            save_users(users_df)
            print(f"El usuario {user_to_delete} fue eliminado.")
        else:
            print("Error: El usuario no existe.")
    else:
        print("Solo los administradores pueden eliminar usuarios.")

# CAMBIAR CONTRASEÑA
def change_password(username, current_password, new_password):
    users_df = load_users()
    if username in users_df.index:
        hashed_current_password = hash_password(current_password)
        if users_df.loc[username, 'password'] == hashed_current_password:
            users_df.loc[username, 'password'] = hash_password(new_password)
            save_users(users_df)
            print(f"La contraseña para {username} se cambió.")
        else:
            print("Contrasena actual incorrecta.")
    else:
        print("Usuario no encontrado.")

# MOSTRAR USUARIOS
def show_users(admin):
    if check_role(admin, 'admin'):
        users_df = load_users()
        for username, row in users_df.iterrows():
            print(f"Usuario: {username}, Rol: {row['role']}")
    else:
        print("Solo los administradores pueden ver la lista de usuarios.")

# COMPROBAR ROL
def check_role(username, required_role):
    users_df = load_users()
    if username in users_df.index and users_df.loc[username, 'role'] == required_role:
        return True
    return False

# ADMIN USER inicial
def create_initial_admin():
    users_df = load_users()
    if 'admin' not in users_df.index:
        users_df.loc['admin'] = [hash_password('admin123'), 'admin']
        save_users(users_df)
        print("Initial admin created: username 'admin', password 'admin123'")
