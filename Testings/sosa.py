from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from dotenv import load_dotenv
import os


load_dotenv()
var = os.getenv("DSNUSER")

Conexion_usuarios = Conexion(var)
repositorio = UserRepo(Conexion_usuarios)

usuarios = repositorio.ver_usuarios()

for user in usuarios:
    print(user)


