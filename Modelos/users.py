from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    apellido: str

class Alumno(User):
    curso: str
    especialidad: str

class Profesor(User):
    pass

class Personal(User):
    rol: str
    password: str
