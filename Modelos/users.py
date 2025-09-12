class User:
    def __init__(self,  nombre, apellido, id: int = None):
        self.nombre = nombre
        self.apellido = apellido
    

class Alumno(User):
    def __init__(self, nombre, apellido, curso, orientacion):
        super().__init__(nombre, apellido)
        self.curso = curso
        self.orientacion = orientacion

class Profesor(User):
    def __init__(self, nombre, apellido, cursos):
        super().__init__(nombre, apellido)
        self.cursos = cursos

class Personal(User):
    def __init__(self, nombre, apellido, rol):
        super().__init__(nombre, apellido)
        self.rol = rol
