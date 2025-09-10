from conexion.conexion import Conexion

class UserRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()

    def ver_usuarios(self):
        self.cur.execute("SELECT * FROM usuarios;")
        return self.cur.fetchall()
