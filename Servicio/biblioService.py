from Repositorio.biblioRepo import BiblioRepo
from Repositorio.userRepo import UserRepo

from Modelos.element import StockItem
from Modelos.users import User, Alumno, Profesor, Personal
from Modelos.registro import Registro, RegistroBase
from Modelos.biblioteca import Libro
from datetime import datetime, time, timedelta

class BiblioService:
    def __init__(self, biblioteca: BiblioRepo, usuarios: UserRepo):
        self.biblioteca = biblioteca
        self.usuarios = usuarios

    #Yo  recibiria de la api, en un json el id del element que se quiere prestar
    #Para solicitar una prestacion se necesiten las siguientes cosas:
    #El id_element del elemento que se quiere prestar, un objeto Usuario con o sin id dependiendo de si es la primera vez que pide
    #Un objeto registro.
    #Toda la estructura de objetos viene desde el frontened como json y 
    #luego en los Controller se transforman en los respectivos objetos usando pydantic

    #aca se pasa algo como ahora = datetime.now()
    #Esta funcion retorna lo q va en expiracion que puede ser 11:40, 17:20,21:30
    #Es decir el tiempo limite q se tiene para entregar

    def calcularExpiracion(ahora):
        hora = ahora.time()
        fecha = ahora.date()
        turnos = [
            (time(7,40), time(11,40)),
            (time(13,10), time(17,20)),
            (time(17,40), time(21,30))
        ]

        for inicio, fin in turnos:
        
    
            if( inicio < hora < fin):

                return datetime.combine(fecha, fin)
        


        

        
            
    #yo debo de recibir del frontened, un usuario(alumno, profesor, etc) y un registro base
    #si el usuario viene sin id es pq no esta en la bd (hacer funcion para eso), entonces lo creo
    def prestar(self, usuario: User, registro_base: RegistroBase):

        #esto me tiene que devolver Disponible, No disponible
        estado = self.biblioteca.buscarEstado(registro_base.element_id)

        #pensar q retornar aca
        if (estado != "Disponible"):
            return {"No esta disponible"}

        
        if (usuario.id_usuario == None):
            usuario.id_usuario = self.usuarios.crearUsuario(usuario)
            print("usuario.id_usuario asignado:", usuario.id_usuario) 
            
        #acordarme de hacerle un alter table a la tabla esta de relacion para agreegarle la columna materia
        if isinstance(usuario, Profesor):
            if not (self.usuarios.buscarRelacionProfesorCurso(registro_base.destino, usuario.id_usuario)):
                self.usuarios.vincularCursoProfesor(registro_base.destino ,usuario.id_usuario)




        elemento = self.biblioteca.buscarElemento(registro_base.element_id)
        cantidad = registro_base.cantidad
        ahora = datetime.now()
        fecha = ahora.date()
        hora = ahora.time()
        

        #si es un libro la expiracion se realiza de +7 dias(es ejemplificativo)
        if isinstance(elemento, Libro):
            expiracion = fecha + timedelta(days=7)
        else:
            expiracion = self.calcularExpiracion(ahora)

        #si es un stock y es reusable el estado es En curso
        #pero si es un elemento q no es reusable(osea q es descartable), nunca voy a tener q esperar a que se devuelva
        #directamente lo marco como consumido
        #lo mismo aplica para su expiracion, es un registro q nace "expirado" pq nunca se debe devolver
        if isinstance(elemento, StockItem) and elemento.isReusable:
            estado = "En curso"
        
        elif isinstance(elemento, StockItem):
            estado = "Consumido"
            expiracion = None
        else:
            estado = "En curso"

        nRegistro = Registro(
            element_id=registro_base.element_id,
            cantidad=cantidad,
            destino=registro_base.destino,
            usuario_id=usuario.id_usuario,
            fecha=fecha,
            hora=hora,
            expiracion=expiracion,
            estado=estado
        )

        self.biblioteca.crearRegistro(nRegistro)

        #Si es un stockitem le tengo q restar las cantidades q estan en uso, y actualizar los disponibles
        #ver funcion en el repo

        #si es un uniqueitem directamente pasa aestar No disponible(pq esta en uso)
        if isinstance(elemento, StockItem):
            self.biblioteca.actDisponibles(registro_base.element_id, cantidad)
        else:
            self.biblioteca.actEstado(registro_base.element_id, "No disponible")




                
