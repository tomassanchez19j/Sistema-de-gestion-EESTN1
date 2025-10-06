from Conexiones.conexion import Conexion
from Modelos.users import User, Alumno, Profesor, Personal

class UserRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()

    def ver_usuarios(self):
        self.cur.execute("""SELECT id, nombre, apellido FROM users""")
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

    #Dejo la funcion porq me sirve para crear usuarios rapidos(despues la borro)
    def crear_usuario(self, nUsuario):
        nombre = nUsuario.nombre
        apellido = nUsuario.apellido
 
        self.cur.execute("""INSERT INTO users (nombre, apellido) VALUES (%s, %s)""", (nombre, apellido))
        self.conexion.commit()

    #Funcion crear usuario q vale
    def crearUsuario(self, nUsuario):
        try:
            nombre = nUsuario.nombre
            apellido = nUsuario.apellido
            self.cur.execute("""
            INSERT INTO users(nombre, apellido) 
            VALUES (%s, %s) 
            RETURNING id""", (nombre, apellido))
        
            user_id = self.cur.fetchone()[0]
            self.conexion.commit()
        
            if isinstance(nUsuario, Alumno):
                curso = nUsuario.curso
                especialidad = nUsuario.especialidad
                self.cur.execute("""
                INSERT INTO alumnos(user_id, curso, especialidad)
                VALUES (%s, %s, %s)
                """, (user_id, curso, especialidad))
                self.conexion.commit()

            elif isinstance(nUsuario, Profesor):
                self.cur.execute("INSERT INTO profesores(user_id) VALUES (%s)", (user_id,))
                self.conexion.commit()

            elif isinstance(nUsuario, Personal):
                rol = nUsuario.rol
                password = nUsuario.password
                self.cur.execute("INSERT INTO personal(user_id, rol, password) VALUES (%s,%s)", (user_id, rol, password))
                self.conexion.commit()
            return user_id
            
        except Exception as e:
            self.conexion.rollback()
            raise e
            

            



    def borrar_usuario(self, id_usuario):
        try:
            self.cur.execute("DELETE FROM users WHERE id = (%s)", (id_usuario,))
            self.conexion.commit()
            self.conexion.close()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def buscar_usuario(self, id_usuario):
        self.cur.execute("SELECT id, nombre, apellido FROM users WHERE id = (%s)", (id_usuario,))
        registro = self.cur.fetchone()
        if registro:
            return User(registro[1], registro[2], registro[0])
        return None
    
    def vincularCursoProfesor(self, nombre_del_curso, profesor_id):
        try:
            self.cur.execute("""
            SELECT id FROM cursos
            WHERE nombre = (%s)
            """,(nombre_del_curso,))

            cursoId = self.cur.fetchone()
            cursoId = cursoId[0]


            self.cur.execute("""
            INSERT INTO profesores_cursos(profesor_id, curso_id)
            VALUES (%s,%s)
            """, (profesor_id, cursoId))

            self.conexion.commit()
            self.conexion.close()

        except Exception as e:
            self.conexion.rollback()
            raise e

    

    def buscarRelacionProfesorCurso(self, nombre_del_curso, profesor_id):

        self.cur.execute("""
        SELECT id FROM cursos
        WHERE nombre = (%s)
        """,(nombre_del_curso,))

        cursoId = self.cur.fetchone()
        cursoId = cursoId[0]


        self.cur.execute("""
        SELECT * FROM profesores_cursos
        WHERE profesor_id = (%s) 
            AND curso_id = (%s)
        """, (profesor_id, cursoId))

        x = self.cur.fetchone()
        if (x):
            return True
        else:
            return False

