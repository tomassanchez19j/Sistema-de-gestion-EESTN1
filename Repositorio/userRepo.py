from Conexiones.conexion import Conexion
from Modelos.users import User, Alumno, Profesor, Personal

class UserRepo:
    def __init__(self, esquema ,conexion: Conexion):
        self.esquema = esquema
        self.conexion = conexion
        self.cur = self.conexion.cur()


    #Revisar este metodo y que devuevla un array de usuarios pero cada uno con su respectiva clase
    def ver_usuarios(self):
        self.cur.execute(f"""SELECT u.id, u.nombre, u.apellido, a.curso, a.especialidad, p.rol, p.password
                            FROM {self.esquema}.usuarios as u
                            INNER JOIN {self.esquema}.alumnos AS a ON a.user_id = u.id
                            INNER JOIN {self.esquema}.personal AS p ON p.user_id = u.id""")
        
        registros = self.cur.fetchall()
        usuarios = []

        for registro in registros:
            nUsuario = User(

                nombre=registro[1],
                apellido=registro[2],
                id_usuario=registro[0]
                
            )
            usuarios.append(nUsuario)

        return usuarios
    
    

    #Funcion crear usuario q vale
    def crearUsuario(self, nUsuario):
        try:
            nombre = nUsuario.nombre
            apellido = nUsuario.apellido
            self.cur.execute(f"""
            INSERT INTO {self.esquema}.usuarios(nombre, apellido) 
            VALUES (%s, %s) 
            RETURNING id""", (nombre, apellido))
        
            user_id = self.cur.fetchone()[0]
            self.conexion.commit()
        
            if isinstance(nUsuario, Alumno):
                curso = nUsuario.curso
                especialidad = nUsuario.especialidad
                self.cur.execute(f"""
                INSERT INTO {self.esquema}.alumnos(user_id, curso, especialidad)
                VALUES (%s, %s, %s)
                """, (user_id, curso, especialidad))
                self.conexion.commit()

            elif isinstance(nUsuario, Profesor):
                self.cur.execute(f"""
                INSERT INTO {self.esquema}.profesores(user_id)
                VALUES (%s)""", (user_id,))
                self.conexion.commit()

            elif isinstance(nUsuario, Personal):
                rol = nUsuario.rol
                password = nUsuario.password
                self.cur.execute(f"""
                INSERT INTO {self.esquema}.personal(user_id, rol, password)
                VALUES (%s,%s,%s)""", (user_id, rol, password))
                self.conexion.commit()
            return user_id
            
        except Exception as e:
            self.conexion.rollback()
            raise e
            

    def borrar_usuario(self, id_usuario):
        try:
            self.cur.execute(f"DELETE FROM {self.esquema}.usuarios WHERE id = (%s)", (id_usuario,))
            self.conexion.commit()
            self.conexion.close()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def buscar_usuario(self, id_usuario):
        self.cur.execute(f"""
        SELECT id, nombre, apellido 
        FROM {self.esquema}.usuarios WHERE id = (%s)""", (id_usuario,))
        registro = self.cur.fetchone()
        if registro:
            return User(registro[1], registro[2], registro[0])
        return None
    
    def vincularCursoProfesor(self, curso_id, profesor_id, materia):
        try:

            self.cur.execute("""
            INSERT INTO profesores_cursos(profesor_id, curso_id, materia)
            VALUES (%s,%s, %s)
            """, (profesor_id, curso_id, materia))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            raise e

    #Funcion para actualizar la jerarquia del usuario(ej: de alumno a pasante(administrador))
    #Considerar que un usuario puede tener varias jerarquias
    #Pensar cual sera el superadministrador
    #Nota: un alumno puede pasar a profesor, tiene sentido ese pasaje en el sistema?

    #Dos metodos para actualizar jerarquia
    #at_jerarquia para los casos de: 
    #-Alumno a personal
    #-Profesor a personal
    #Pq necesitan necesaramente una contrasña de acceso
    def crearJerarquia(self, id_user, rol, npassword):
        #Roles: Directivo, pasante, administrador, bibliotecario
        #Pasante: pañolero/pañolera

        try: 
            usuario = self.buscar_usuario(id_user)
            self.cur.execute(f"""
            INSERT INTO {self.esquema}.personal(user_id, rol, password)
            VALUES (%s,%s,%s)
            """, (usuario.id_usuario, rol, npassword))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            raise e

    #Este es mas general, funciona si el usuario ya esta creado
    #Actualizar jerarquia personal(ya tiene un usuario - contraseña creado)
    def actJerarquia(self, id_user, jerarquia):
        usuario = self.buscar_usuario(id_user)
        password = usuario.password
        try:            
            self.cur.execute(f"""
            INSERT INTO {self.esquema}.personal(user_id, rol, password)
            VALUES (%s, %s, %s)
            """, (password, jerarquia))
        except Exception as e:
            self.conexion.rollback()
            raise e

    
    def buscarRelacionProfesorCurso(self, nombre_del_curso, profesor_id):

        self.cur.execute(f"""
        SELECT id FROM {self.esquema}.cursos
        WHERE nombre = (%s)
        """,(nombre_del_curso,))

        cursoId = self.cur.fetchone()
        cursoId = cursoId[0]


        self.cur.execute(f"""
        SELECT * FROM {self.esquema}.profesores_cursos
        WHERE profesor_id = (%s) 
            AND curso_id = (%s)
        """, (profesor_id, cursoId))

        x = self.cur.fetchone()
        if (x):
            return True
        else:
            return False

