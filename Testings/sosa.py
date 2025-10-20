from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from Repositorio.biblioRepo import BiblioRepo
from Repositorio.repositorio import Repositorio
from Modelos.users import User, Alumno, Profesor, Personal
from Modelos.registro import RegistroBase
from Modelos.element import StockItem, UniqueItem
from Modelos.biblioteca import Libro
from Controller.biblioController import BiblioController
#30/9 ver funciones insert into(prevenir inyecciones sql)
#Cambiar de 

#Cambie todas las tablas a:
#inventario, uniqueitems, stockitems
#puedo hacer un repositorioGeneral, los demas heredan de el

#Notas para hacer el servicio:
#Considerar el caso de que se ingresa un nuevo elemento, el objeto que se ingresa se carga como disponible
from fastapi import FastAPI
from Servicio.biblioService import BiblioService
from Servicio.servicio import Servicio
from datetime import datetime, time
from dotenv import load_dotenv
import os

#Your identification has been saved in C:\Users\Lautaro/.ssh/id_rsa
#Your public key has been saved in C:\Users\Lautaro/.ssh/id_rsa.pub
#The key fingerprint is:
#SHA256:DhgSm9rYxu+WoHwaG0mRbLCGdodIWk8og9ZdRCnUUbo lautaro@DESKTOP-4NOI3F4

from cryptography.hazmat.primitives import serialization
# read and load the key
file_path = r'C:\Users\Lautaro/.ssh/id_rsa'
file_path1 = r'C:\Users\Lautaro/.ssh/id_rsa.pub'
private_key = open(file_path, 'r').read()
public_key = open(file_path1)
key = serialization.load_ssh_public_key(public_key.encode())

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library
#27/9 voy a probar los metodos de repositorio creo q ya lo termino hoy y empiezo el service
load_dotenv()
var= os.getenv("DATABASE_URL")
conexion=Conexion(var)



repositorio = Repositorio("biblioteca", conexion)
rep_usuarios = UserRepo("usuarios", conexion)

servicio = Servicio(repositorio, rep_usuarios)
app = FastAPI()
controller = BiblioController(servicio)
controller.rutas(app)



