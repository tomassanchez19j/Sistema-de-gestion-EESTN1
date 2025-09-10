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



cur.execute(
    "INSERT INTO users (nombre, apellido) VALUES (%s, %s) RETURNING id",
    ("Lautaro", "Sosa")
)

user_id = cur.fetchone()[0]
conexion.commit()


cur.execute("SELECT id, nombre, apellido FROM users")
usuarios = cur.fetchall()

for u in usuarios:
    print(f"ID: {u[0]}, Nombre: {u[1]}, Apellido: {u[2]}")






conexion.commit()
conexion.close()
