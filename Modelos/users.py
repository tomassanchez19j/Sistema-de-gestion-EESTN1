from pydantic import BaseModel
from typing import List, Optional

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
    password: Optional[str] = None
    email: str
    zonas_acceso:List[str]=[]
