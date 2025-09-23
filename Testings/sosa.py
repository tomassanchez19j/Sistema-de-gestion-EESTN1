from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from Repositorio.biblioRepo import BiblioRepo
from Modelos.users import User, Alumno, Profesor, Personal
from Modelos.registro import RegistroBase
from Modelos.biblioteca import Libro
from Controller.biblioController import BiblioController



#Cambie todas las tablas a:
#inventario, uniqueitems, stockitems
#puedo hacer un repositorioGeneral, los demas heredan de el


from fastapi import FastAPI


from Servicio.biblioService import BiblioService

from datetime import datetime, time
from dotenv import load_dotenv
import os

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library

load_dotenv()
var = os.getenv("DSNUSER")
var1 = os.getenv("DSNLIBRARY")
var2 = os.getenv("")


#ACAAAA
cBiblioteca = Conexion(var1)
cUsarios = Conexion(var)
cElectro = Conexion(var2)
rep_usuarios = UserRepo(cUsarios)

repositorio = BiblioRepo(cBiblioteca)
servicio = BiblioService(repositorio, rep_usuarios)

app = FastAPI()

controller = BiblioController(servicio)
controller.rutas(app)





Conexion_usuarios = Conexion(var)
repositorio = UserRepo(Conexion_usuarios)

Conexion_biblioteca = Conexion(var1)
repositorio_biblioteca = BiblioRepo(Conexion_biblioteca)

biblioteca_servicio = BiblioService(repositorio_biblioteca, repositorio)

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


"""registro_base = RegistroBase(
    element_id=4, 
    cantidad=1, 
    destino="7mo 5ta")
"""
#print(repositorio.crearUsuario(nUsuario))

#print(biblioteca_servicio.prestar(nUsuario, registro_base))

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



#repositorio_biblioteca.crearLibro(nlibro1)
#repositorio_biblioteca.crearLibro(nlibro)
"""
#cursor.execute("""
#CREATE TABLE IF NOT EXISTS inventario (
#    element_id SERIAL PRIMARY KEY,
#    nombre TEXT NOT NULL,
#    descripcion TEXT,
#   estado TEXT NOT NULL,
#    ubicacion TEXT,
#    ubicacion_interna TEXT
#);
#""")

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS libros (
#    codigo_interno TEXT PRIMARY KEY,
#    inventario_id INT NOT NULL,
#    ISBN TEXT NOT NULL,
#    autor TEXT,
#    editorial TEXT NOT NULL,
#    categoria TEXT,
#    publicacion_year INT NOT NULL,
#    impresion_year INT NOT NULL,
#    pais TEXT NOT NULL,
#    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS uniqueItem_library (
#    codigo_interno TEXT PRIMARY KEY,
#    inventario_id INT NOT NULL,
#    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS stockItem_library (
#    inventario_id INT PRIMARY KEY,
#    cantidad INT NOT NULL,
#    disponibles INT NOT NULL,
#    isReusable BOOLEAN NOT NULL,
#    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS registros (
#    registro_id SERIAL PRIMARY KEY,
#    usuario_id INT NOT NULL,
#    element_id INT NOT NULL,
#    cantidad INT NOT NULL,
#    fecha DATE NOT NULL,
#    hora TIME(0) NOT NULL,
#    expiracion TIMESTAMP(0) NOT NULL,
#    estado TEXT NOT NULL,
#    destino TEXT NOT NULL,
#    FOREIGN KEY (element_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")


#cursor.execute("""
#    ALTER TABLE profesores_cursos
#    ALTER COLUMN expiracion DROP NOT NULL
#""")

#Conexion_biblioteca.commit()

#cursor.execute("""
#DELETE FROM inventario
#WHERE element_id IN (1, 2);
#""")


#cursor.execute("""
#ALTER TABLE profesores_cursos
#ADD COLUMN materia TEXT;
#""")



"""ahora = datetime.now()
hora = ahora.time()
turnos = [
            (time(7,40), time(11,40)),
            (time(13,10), time(17,20)),
            (time(17,40), time(21,30))
        ]


for inicio, fin in turnos:
    print(inicio.strftime("%H:%M"), " a ", fin.strftime("%H:%M"))
    
    if( inicio < hora < fin):
        print(hora)
        print(f"Es en este turno")
        
    else:
        print(hora)
        print(f"No es en este turno")"""


#Conexion_biblioteca.commit()



"""
libros = repositorio_biblioteca.verLibros()
for libro in libros:
    print(f"Id:{libro.id_element} Titulo: {libro.nombre}, Autor: {libro.autor}, Pais: {libro.pais}")

libro = repositorio_biblioteca.buscarLibro(2)
estado = repositorio_biblioteca.buscarEstado(2)

print(f"JSAKKKKKKKKKKK {estado}")
print(f"jUASJUASJUAS Id:{libro.id_element} Titulo: {libro.nombre}, Autor: {libro.autor}, Pais: {libro.pais}")"""


"""usuarios = repositorio.ver_usuarios()


for user in usuarios:
    print(f"id_usuario: {user.id_usuario} \n nombre: {user.nombre} \n apellido: {user.apellido}\n")"""


