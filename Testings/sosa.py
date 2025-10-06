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

from datetime import datetime, time
from dotenv import load_dotenv
import os

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library
#27/9 voy a probar los metodos de repositorio creo q ya lo termino hoy y empiezo el service
load_dotenv()
var = os.getenv("DSNUSER")
var1 = os.getenv("DSNLIBRARY")
var2 = os.getenv("DSNELECTRO")
var3 = os.getenv("DSNPROGRAMACION")




cBiblioteca = Conexion(var1)
cUsarios = Conexion(var)
cProgramacion = Conexion(var3)




rep_usuarios = UserRepo(cUsarios)
repositorio = BiblioRepo(cBiblioteca)
servicio = BiblioService(repositorio, rep_usuarios)
rep = Repositorio(cProgramacion)



repositorio.actElemento(3, "editorial", "Estrada")


app = FastAPI()

controller = BiblioController(servicio)
controller.rutas(app)




"""rep = Repositorio(cProgramacion)
mouses = StockItem(nombre="Mouse",
                   descripcion="Mouse RDX 600",
                    estado="Disponible", 
                    ubicacion="Programacion", 
                    ubicacion_interna="Stand-8",
                    tipo="Stockitem", 
                    cantidad=12, 
                    disponibles=12,
                    isReusable= True)
rep.crearElement(mouses)
"""

"""nUsuario = Alumno(
        id_usuario=26,  
        nombre="Juan", 
        apellido="Salmon", 
        curso="7mo 5ta", 
        especialidad="Programacion")

profesor = Profesor(
        nombre="Deborah",
        apellido="Cabezas"
)"""


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


# ---------- Aca dejo como cree las tablas(me sirve por si debo hacer otras) ------------

#cProgramacion.cursor.execute("""
#CREATE TABLE IF NOT EXISTS inventario (
#element_id SERIAL PRIMARY KEY,
#nombre TEXT NOT NULL,
#descripcion TEXT,
#estado TEXT NOT NULL,
#ubicacion TEXT,
#ubicacion_interna TEXT,
#tipo TEXT
#);""")


#cProgramacion.cursor.execute("""
#CREATE TABLE IF NOT EXISTS uniqueitems (
#    codigo_interno TEXT PRIMARY KEY,
#    inventario_id INT NOT NULL,
#    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")

#cProgramacion.cursor.execute("""
#CREATE TABLE IF NOT EXISTS stockitems (
#    inventario_id INT PRIMARY KEY,
#    cantidad INT NOT NULL,
#    disponibles INT NOT NULL,
#    isReusable BOOLEAN NOT NULL,
#    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
#);
#""")

#cElectro.cursor.execute("""
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
#cElectro.commit()
#cProgramacion.commit()


#cursor.execute("""
#    ALTER TABLE profesores_cursos
#    ALTER COLUMN expiracion DROP NOT NULL
#""")


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



"""
libros = repositorio_biblioteca.verLibros()
for libro in libros:
    print(f"Id:{libro.id_element} Titulo: {libro.nombre}, Autor: {libro.autor}, Pais: {libro.pais}")



for user in usuarios:
    print(f"id_usuario: {user.id_usuario} \n nombre: {user.nombre} \n apellido: {user.apellido}\n")"""


