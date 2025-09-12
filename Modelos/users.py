from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    apellido: str

class Alumno(User):
    curso: str
    orientacion: str

class Profesor(User):
    cursos: List[str]

class Personal(User):
    rol: str
