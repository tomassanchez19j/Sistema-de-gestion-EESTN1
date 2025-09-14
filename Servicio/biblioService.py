from Repositorio.biblioRepo import BiblioRepo
from Repositorio.userRepo import UserRepo
from Modelos.users import User, Alumno, Profesor, Personal
class BiblioService:
    def __init__(self, biblioteca: BiblioRepo, usuarios: UserRepo):
        self.biblioteca = biblioteca
        self.usuarios = usuarios

    #Yo  recibiria de la api, en un json el id del element que se quiere prestar
    def prestar(self, id_element, usuario: User):
        estado = self.biblioteca.buscarEstado()
        if(estado == "Disponible"):
            
            if isinstance(usuario, Alumno):
                
