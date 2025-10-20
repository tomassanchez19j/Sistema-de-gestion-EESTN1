from typing import Any
from Conexiones.conexion import Conexion
from Modelos.users import User, Alumno, Profesor, Personal
from Repositorio.userRepo  import UserRepo
from Servicio.pwdManager import PasswordManager
from Servicio.tokenManager import TokenManager
class Userservice:
    def __init__(self, conexion: Conexion, repo: UserRepo, pm: PasswordManager, tm: TokenManager):
        self.conexion = conexion
        self.repo = repo
        self.pm = pm
        self.tm = tm

    def res(estado: bool, mensaje: str, data: Any):
        return {
            "success": estado,
            "message": mensaje,
            "data": data
        }


    #Atento aca, validar intentos de ingreso de sesion
    #Crear Tokens Managers
    def login(self, email, password):
        try:
            usuario = self.repo.usuario_email(email)
            if not usuario:
                return self.res(False, "Email o contraseña incorrectos", None)
            
            if not self.pm.verify_pwd(password, usuario.password):
                return self.res(False, "Email o contraseña incorrectos", None)
            
            token_response= self.tm.tokenResponse(usuario.id_usuario, usuario.email)
            return self.res(True, "Acceso", token_response.model_dump())
        except Exception as e:
            raise e
    
    #token str no Objeto Token
    def validarUsuario(self, token:str):
        res = self.tm.validarToken(token)

        if res:
            return self.res(True, "Validado", res)

        else:
            return self.res(res.succes, f"{res.message}", None)

    def crearUsuario(self, usuario: User):
        try:
            if isinstance(usuario, Personal):
                usuario.password = self.pm.hash_password(usuario.password)
                id = self.repo.crearUsuario(usuario)
            else:
                id = self.repo.crearUsuario(usuario)
            
            return (self.res(True, f"Usuario creado exitosamente con id: {id}", id ))

        except Exception as e:
            self.conexion.rollback()
            return (self.res(False, f"Error al crear usuario error: {e}", None))
        
    

    def crearJerarquia(self, id_user, npassword, jerarquia):
        jerarquias = ["Directivo", "Pasante", "Administrador", "Bibliotecario"]
        try:
            if(jerarquia.capitalize in jerarquias):
                n = self.pm.hash_pwd(npassword)
                self.repo.crearJerarquia(id_user, n, jerarquia)
            return (self.res(True, f"Usuario ascendido a jerarquia {jerarquia}", None))
            
        except Exception as e:
            self.conexion.rollback()
            return (self.res(False, f"Error al crear usuario error: {e}", None))

    def actJerarquia(self, id_user, jerarquia):
        jerarquias = ["Directivo", "Pasante", "Administrador", "Bibliotecario"]
        try:
            if(jerarquia.capitalize in jerarquias):
                self.repo.actJerarquia(id_user, jerarquia)
                self.repo.conexion.close()
                return (self.res(True, f"Usuario con id {id_user} ascendio a {jerarquia}", None))
            else:
                return(self.res(False, f"Error jerarquia inexistente"))
        except Exception as e:
            self.conexion.rollback()
            return (self.res(False, f"Error al ascende usuario a {jerarquia}: {e}", None))
        
    def borrar_usuario(self, id_user):
        try:
            self.repo.borrar_usuario(id_user)
            return (self.res(True, f"Usuario borrado exitosamente", None))
        
        except Exception as e:
            self.conexion.rollback()
            return (self.res(False, f"Error al eliminar usuario error: {e}", None))
    
    def agCurso_profesor(self, id_profesor, id_curso, materia):
        try:
            self.repo.vincularCursoProfesor(id_profesor, id_curso, materia)
            return(self.res(True, f"Profesor id {id_profesor} vinculado al curso con id {id_curso}", None))
        except Exception as e:
            self.conexion.rollback()
            return (self.res(False, f"Error al eliminar usuario error: {e}", None))
        
    def buscar_usuario(self, id_usuario):
        return (self.repo.buscar_usuario(id_usuario))
    
    def ver_usuarios(self):
        return(self.repo.ver_usuarios())


    