from Conexiones.conexion import Conexion
from Modelos.users import User

#El unico atributo que van a tener los repositorios es un objeto conexion
#Se arma todo en el main
class UserRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()

    def ver_usuarios(self):
        self.cur.execute("SELECT * FROM users;")
        registros = self.cur.fetchall()
        usuarios = []
        
        for registro in registros:
            nUsuario = User(registro[0], registro[1])
            usuarios.append(nUsuario)

        return usuarios

    def crear_usuario(self, nUsuario):
        nombre = nUsuario.nombre
        apellido = nUsuario.apellido

        self.cur.execute("INSERT INTO users (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
        self.cur.commit()
        self.cur.close()

    def borrar_usuario(self, id):
        self.cur.execute("DELETE * FROM users WHERE id = %s", (id))
        self.cur.commit()

    def buscar_usuario(self, id):
        self.cur.execute("SELECT * FROM users WHERE id = %s", (id))
        self.cur.commit()

    


