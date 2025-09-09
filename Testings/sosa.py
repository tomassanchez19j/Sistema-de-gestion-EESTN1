#agregar atributo entregado al registro
from conexion.userConexion import ConexionUser

conexion = ConexionPG()
cur = conexion.cur()


cur.execute("""
CREATE TABLE IF NOT EXISTS users  (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    
)
""")

cur.execute(
    "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
    ("Tostadora", 35000, 100)
)

conexion.commit() 
conexion.close()