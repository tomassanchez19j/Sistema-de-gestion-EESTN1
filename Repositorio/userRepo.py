from conexion.conexion import Conexion


#El unico atributo que van a tener los repositorios es un objeto conexion
#Se arma todo en el main
class UserRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()

    def ver_usuarios(self):
        self.cur.execute("SELECT * FROM usuarios;")
        usuarios = self.cur.fetchall()
        return usuarios

