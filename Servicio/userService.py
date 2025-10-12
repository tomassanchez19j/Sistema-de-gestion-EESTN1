from Conexiones.conexion import Conexion
from Modelos.users import Alumno, Profesor
from Repositorio.userRepo  import UserRepo
class Userservice:
    def __init__(self, conexion: Conexion, repo: UserRepo):
        self.conexion = conexion
        self.repo = repo

    def crearJerarquia(self, id_user, npassword, jerarquia):
        jerarquias = ["Directivo", "Pasante", "Administrador", "Bibliotecario"]
        if(jerarquia.capitalize in jerarquias):
            self.repo.crearJerarquia(id_user, npassword, jerarquia)
            self.repo.conexion.close()

            return {"Mensaje": f"Usuario con id {id_user} ascendido a {jerarquia}"}

    def actJerarquia(self, id_user, jerarquia):
        jerarquias = ["Directivo", "Pasante", "Administrador", "Bibliotecario"]
        if(jerarquia.capitalize in jerarquias):
            self.repo.actJerarquia(id_user, jerarquia)
            self.repo.conexion.close()
            return {"Mensaje": f"El usuario de id {id_user} ha sido ascendido al {jerarquia}"}
        else:
            return{"Mensaje": f"Jerarquia inexistente"}

    