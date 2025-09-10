from Conexiones.conexion import Conexion
from dotenv import load_dotenv
import os


load_dotenv()
var = os.getenv("DSNUSER")


conexion = Conexion(var)
cur = conexion.cur()


cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS personal (
    user_id INTEGER PRIMARY KEY,
    rol TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")



#cur.execute("""
#ALTER TABLE personal
#ADD COLUMN password TEXT NOT NULL
#""")


cur.execute("""
CREATE TABLE IF NOT EXISTS profesores (
    user_id INTEGER PRIMARY KEY,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS alumnos (
    user_id INTEGER PRIMARY KEY,
    curso TEXT NOT NULL,
    especialidad TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS CURSOS(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    año INTEGER NOT NULL,
    division INTEGER NOT NULL,
    ciclo TEXT NOT NULL,
    especialidad TEXT

)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS profesores_cursos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    profesor_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores (user_id),
    FOREIGN KEY (curso_id) REFERENCES cursos (ID)

)
""")


"""cur.execute(
    "INSERT INTO users (nombre, apellido) VALUES (%s, %s) RETURNING id",
    ("Tomaz", "Sanchez")
)"""


"""user_id = cur.fetchone()[0]

"""

cur.execute("""
CREATE TABLE IF NOT EXISTS cursos(


)""")



cur.execute("SELECT id, nombre, apellido FROM users")
usuarios = cur.fetchall()

for u in usuarios:
    print(f"ID: {u[0]}, Nombre: {u[1]}, Apellido: {u[2]}")






conexion.commit()
conexion.close()
