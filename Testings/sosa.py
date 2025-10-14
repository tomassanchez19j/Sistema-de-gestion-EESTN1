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

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library
#27/9 voy a probar los metodos de repositorio creo q ya lo termino hoy y empiezo el service
load_dotenv()
var= os.getenv("DATABASE_URL")
conexion=Conexion(var)

#Ejecutar esto cuando llegue a casa
conexion.cursor.execute("ALTER TABLE usuarios.personal ADD COLUMN email TEXT NOT NULL")
conexion.commit()
conexion.close()


"""mouses = StockItem(nombre="Mouse",
                   descripcion="Mouse RDX 600",
                    estado="Disponible", 
                    ubicacion="Programacion", 
                    ubicacion_interna="Stand-8",
                    tipo="Stockitem", 
                    cantidad=12, 
                    disponibles=12,
                    isReusable= True)
"""
nlibro = Libro(
    nombre="El Decameron",
    descripcion="Libro el decameron",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 12",
    tipo = "Libro",
    codigo_interno = "COMP-334",
    ISBN="2332091221",
    autor=" Giovanni Boccaccio",
    editorial="Losada",
    categoria="Novela",
    publicacion_year=1349,
    impresion_year=1999,
    pais="Italia"
)

nlibro1= Libro(
    nombre="Don Quijote de la Mancha",
    descripcion="Libro del Quijote",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 1",
    tipo = "Libro",
    codigo_interno = "COMP-212",
    ISBN="234556662",
    autor="Miguel de Cervantes",
    editorial="Booket",
    categoria="Novela",
    publicacion_year=1605,
    impresion_year=2015,
    pais="España"
)





repositorio = Repositorio("biblioteca", conexion)
rep_usuarios = UserRepo("usuarios", conexion)




servicio = Servicio(repositorio, rep_usuarios)
app = FastAPI()
controller = BiblioController(servicio)
controller.rutas(app)

nUsuario = Alumno(
        id_usuario=26,  
        nombre="Juan", 
        apellido="Salmon", 
        curso="7mo 5ta", 
        especialidad="Programacion")

profesor = Profesor(
        nombre="Deborah",
        apellido="Cabezas"
)


registro_base = RegistroBase(
    element_id=4, 
    cantidad=1, 
    destino="7mo 5ta")



nlibro = Libro(
    nombre="El Decameron",
    descripcion="Libro el decameron",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 12",
    tipo = "Libro",
    codigo_interno = "COMP-334",
    ISBN="2332091221",
    autor=" Giovanni Boccaccio",
    editorial="Losada",
    categoria="Novela",
    publicacion_year=1349,
    impresion_year=1999,
    pais="Italia"
)

nlibro1= Libro(
    nombre="Don Quijote de la Mancha",
    descripcion="Libro del Quijote",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 1",
    tipo = "Libro",
    codigo_interno = "COMP-212",
    ISBN="234556662",
    autor="Miguel de Cervantes",
    editorial="Booket",
    categoria="Novela",
    publicacion_year=1605,
    impresion_year=2015,
    pais="España"
)


