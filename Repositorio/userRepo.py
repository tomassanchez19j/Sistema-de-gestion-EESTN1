from Conexiones.conexion import Conexion
from Modelos.users import User

class UserRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()

    def ver_usuarios(self):
        self.cur.execute("SELECT id, nombre, apellido FROM users;")
        registros = self.cur.fetchall()
        usuarios = []

        for registro in registros:
            nUsuario = User(

                nombre=registro[1],
                apellido=registro[2],
                id_usuario=registro[0]
                
            )
            usuarios.append(nUsuario)

        return usuarios


    def crear_usuario(self, nUsuario):
        nombre = nUsuario.nombre
        apellido = nUsuario.apellido
 
        self.cur.execute("INSERT INTO users (nombre, apellido) VALUES (%s, %s);", (nombre, apellido))
        self.conexion.commit()

    def borrar_usuario(self, id_usuario):
        self.cur.execute("DELETE FROM users WHERE id = %s;", (id_usuario,))
        self.conexion.commit()

    def buscar_usuario(self, id_usuario):
        self.cur.execute("SELECT id, nombre, apellido FROM users WHERE id = %s;", (id_usuario,))
        registro = self.cur.fetchone()
        if registro:
            return User(registro[1], registro[2], registro[0])
        return None

