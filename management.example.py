# Importar las funciones del módulo user_management
from user_management import login, add_user, delete_user, change_password, show_users, create_initial_admin

# Crear el usuario admin inicial
create_initial_admin()

# Ejemplo de uso de funciones
username = input("Ingresa tu nombre de usuario: ")
password = input("Ingresa tu contrasena: ")

# Iniciar sesión
if login(username, password):
    print("Sesión iniciada.")
else:
    print("Error al iniciar sesión.")

# Agregar un nuevo usuario (solo si es admin)
admin_username = 'admin'  # Suponiendo que el admin ya ha iniciado sesión
new_user = input("Ingresa un nuevo nombre de usuario: ")
new_password = input("Ingresa la contrasena para el nuevo usuario: ")
role = input("Ingresa el rol para el nuevo usuario (admin/user): ")
add_user(admin_username, new_user, new_password, role)

# Mostrar todos los usuarios
show_users(admin_username)

# Cambiar la contraseña de un usuario
username_to_change = input("Ingresa el nombre de usuario para cambiar la contraseña: ")
current_password = input("Ingresa la contraseña actual: ")
new_password = input("Ingresa la nueva contrasena: ")
change_password(username_to_change, current_password, new_password)

# Borrar un usuario
user_to_delete = input("Ingresa el nombre de usuario para eliminar: ")
delete_user(admin_username, user_to_delete)
