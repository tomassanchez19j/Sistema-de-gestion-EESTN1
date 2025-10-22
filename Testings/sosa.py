from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from Repositorio.biblioRepo import BiblioRepo
from Repositorio.repositorio import Repositorio
from Modelos.users import User, Alumno, Profesor, Personal
from Modelos.registro import RegistroBase
from Modelos.element import StockItem, UniqueItem
from Modelos.biblioteca import Libro
from Controller.biblioController import BiblioController
from Controller.controller import Controller
from Servicio.pwdManager import PasswordManager
from Servicio.tokenManager import TokenManager
#30/9 ver funciones insert into(prevenir inyecciones sql)

#Cambie todas las tablas a:
#inventario, uniqueitems, stockitems
#puedo hacer un repositorioGeneral, los demas heredan de el

#Notas para hacer el servicio:
#Considerar el caso de que se ingresa un nuevo elemento, el objeto que se ingresa se carga como disponible
from fastapi import FastAPI
from Servicio.biblioService import BiblioService
from Servicio.servicio import Servicio
from Servicio.userService import Userservice
from datetime import datetime, time
from dotenv import load_dotenv
import os
#uvicorn Testings.sosa:app --reload --host 0.0.0.0 --port 8000

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library
#27/9 voy a probar los metodos de repositorio creo q ya lo termino hoy y empiezo el service

#Para tabla areas
# (id: 1) Biblioteca
# (id: 2) Laboratorio
# (id: 3) Electromecanica
# (id: 4) Programacion

load_dotenv()
var= os.getenv("DATABASE_URL")
conexion=Conexion(var)
algoritmo = os.getenv("ALGORITHM")
secret_key = os.getenv("JWT_SECRET_KEY")



repositorio = Repositorio("programacion", conexion)
rep_usuarios = UserRepo("usuarios", conexion)

pm = PasswordManager()
tm = TokenManager(algoritmo, secret_key)


serviceUser = Userservice(conexion, rep_usuarios, pm, tm)
toto = Alumno(nombre="Marcos", apellido="Rodriguez", curso="7mo 3ra", especialidad="electromecanica")

profesor = Profesor(nombre="Maria", apellido="Walsh")
servicio = Servicio(repositorio, rep_usuarios)

#Que cuando se devuelva se vuelva a sumar el disponibles
print(servicio.devolver(2))



#print(serviceUser.crearJerarquia(8, "marquitos", "Pasante", "marquitos@gmail.com", accesos))
#print(serviceUser.actJerarquia(8, "Administrador", accesos))
#print(serviceUser.bajaPersonal(8))

"""monitor = StockItem(nombre="Monitor MMR", 
                    descripcion="Monitor MMR", 
                    estado="Disponible", 
                    ubicacion="Programacion", 
                    ubicacion_interna="Stand-10",
                    tipo="Stockitem", 
                    cantidad=5, 
                    disponibles=5,
                    isReusable=True)"""

app = FastAPI()
#controller = BiblioController(servicio)
#controller.rutas(app)

controller = Controller(servicio, "/programacion")
controller.rutas(app)


