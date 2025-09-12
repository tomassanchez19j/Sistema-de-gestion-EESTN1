from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from Modelos.users import User
from dotenv import load_dotenv
import os


load_dotenv()
var = os.getenv("DSNUSER")


Conexion_usuarios = Conexion(var)
repositorio = UserRepo(Conexion_usuarios)


usuarios = repositorio.ver_usuarios()

for user in usuarios:
    print(f"id_usuario: {user.id_usuario} \n nombre: {user.nombre} \n apellido: {user.apellido}\n")
