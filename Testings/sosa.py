#agregar atributo entregado al registro
from conexion.conexion import Conexion
from dotenv import load_dotenv
import os

load.dotenv()

var = os.getenv("DSNUSER")

conexion = conexion(var)
cur = conexion.cur()


cur.execute("""
CREATE TABLE IF NOT EXISTS users  (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    
)
""")

CUR.EXECUTE("""
    CREATE TABLE IF NOT EXISTS staff ()
""")

cur.execute(
    "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
    ("Tostadora", 35000, 100)
)

conexion.commit() 
conexion.close()