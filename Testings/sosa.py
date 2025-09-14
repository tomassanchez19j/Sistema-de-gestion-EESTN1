from Conexiones.conexion import Conexion
from Repositorio.userRepo import UserRepo
from Repositorio.biblioRepo import BiblioRepo
from Modelos.users import User
from Modelos.biblioteca import Libro
from dotenv import load_dotenv
import os

#tengo que crear tabla libros, tabla registros, tabla, uniqueItem_library, stockItem_library

load_dotenv()
var = os.getenv("DSNUSER")
var1 = os.getenv("DSNLIBRARY")


Conexion_usuarios = Conexion(var)
repositorio = UserRepo(Conexion_usuarios)

Conexion_biblioteca = Conexion(var1)
repositorio_biblioteca = BiblioRepo(Conexion_biblioteca)


cursor = Conexion_biblioteca.cur()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (
    element_id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT NOT NULL,
    ubicacion TEXT,
    ubicacion_interna TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    codigo_interno TEXT PRIMARY KEY,
    inventario_id INT NOT NULL,
    ISBN TEXT NOT NULL,
    autor TEXT,
    editorial TEXT NOT NULL,
    categoria TEXT,
    publicacion_year INT NOT NULL,
    impresion_year INT NOT NULL,
    pais TEXT NOT NULL,
    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS uniqueItem_library (
    codigo_interno TEXT PRIMARY KEY,
    inventario_id INT NOT NULL,
    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stockItem_library (
    inventario_id INT PRIMARY KEY,
    cantidad INT NOT NULL,
    disponibles INT NOT NULL,
    isReusable BOOLEAN NOT NULL,
    FOREIGN KEY (inventario_id) REFERENCES inventario(element_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    registro_id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    element_id INT NOT NULL,
    cantidad INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME(0) NOT NULL,
    expiracion TIMESTAMP(0) NOT NULL,
    estado TEXT NOT NULL,
    destino TEXT NOT NULL,
    FOREIGN KEY (element_id) REFERENCES inventario(element_id) ON DELETE CASCADE
);
""")

Conexion_biblioteca.commit()
"""
nlibro = Libro(
    nombre="El principito",
    descripcion="Libro del principito",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 8",
    codigo_interno = "COMP-33",
    ISBN="233209320",
    autor="Saint-Exupéry",
    editorial="Losada",
    categoria="Infantil",
    publicacion_year=1928,
    impresion_year=2015,
    pais="Francia"
)

nlibro1= Libro(
    nombre="El Gatopardo",
    descripcion="Libro del gatopardo",
    estado="Disponible",
    ubicacion="Biblioteca",
    ubicacion_interna="Estand 10",
    codigo_interno = "COMP-21",
    ISBN="2332122",
    autor="Giuseppe Tomasi di Lampedusa",
    editorial="Losada",
    categoria="Misterio",
    publicacion_year=1928,
    impresion_year=2015,
    pais="Italia"
)



repositorio_biblioteca.crearLibro(nlibro1)

"""



libros = repositorio_biblioteca.verLibros()
for libro in libros:
    print(f"Id:{libro.id_element} Titulo: {libro.nombre}, Autor: {libro.autor}, Pais: {libro.pais}")

libro = repositorio_biblioteca.buscarLibro(2)
estado = repositorio_biblioteca.buscarEstado(2)

print(f"JSAKKKKKKKKKKK {estado}")
print(f"jUASJUASJUAS Id:{libro.id_element} Titulo: {libro.nombre}, Autor: {libro.autor}, Pais: {libro.pais}")


"""usuarios = repositorio.ver_usuarios()


for user in usuarios:
    print(f"id_usuario: {user.id_usuario} \n nombre: {user.nombre} \n apellido: {user.apellido}\n")"""


