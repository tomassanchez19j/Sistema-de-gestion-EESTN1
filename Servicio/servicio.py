from Repositorio.repositorio import Repositorio
from Repositorio.userRepo import UserRepo
from datetime import datetime, time, timedelta
from Modelos.biblioteca import Libro
from Modelos.element import StockItem
from Modelos.registro import Registro, RegistroBase
from Modelos.users import User, Profesor

class Servicio:
    def __init__(self, repositorio: Repositorio, usuarios: UserRepo):
        self.repositorio = repositorio
        self.usuarios = usuarios


    #considerar si esta funcion basta para la expiracion
    #ejemplo: 
    def calcularExpiracion(self, ahora):
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
            
    
    def prestar(self, usuario: User, registro_base: RegistroBase):

        #esto me tiene que devolver Disponible, No disponible
        estado = self.repositorio.buscarEstado(registro_base.element_id)

        #pensar q retornar aca
        if (estado != "Disponible"):
            return {"No esta disponible"}

        
        if (usuario.id_usuario == None):
            usuario.id_usuario = self.usuarios.crearUsuario(usuario)
            print(f"Usuario creado", usuario.id_usuario) 
            
        #acordarme de hacerle un alter table a la tabla esta de relacion para agreegarle la columna materia
        if isinstance(usuario, Profesor):
            if not (self.usuarios.buscarRelacionProfesorCurso(registro_base.destino, usuario.id_usuario)):
                self.usuarios.vincularCursoProfesor(registro_base.destino ,usuario.id_usuario)




        elemento = self.repositorio.buscarElemento(registro_base.element_id)
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

        self.repositorio.crearRegistro(nRegistro)

        #Si es un stockitem le tengo q restar las cantidades q estan en uso, y actualizar los disponibles
        #ver funcion en el repo

        #si es un uniqueitem directamente pasa aestar No disponible(pq esta en uso)
        if isinstance(elemento, StockItem):
            self.repositorio.actDisponibles(registro_base.element_id, cantidad)
        else:
            self.repositorio.actEstado(registro_base.element_id, "No disponible")
