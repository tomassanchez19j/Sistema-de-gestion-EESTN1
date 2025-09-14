from Repositorio.biblioRepo import BiblioRepo
from Repositorio.userRepo import UserRepo

from Modelos.element import StockItem
from Modelos.users import User, Alumno, Profesor, Personal
from Modelos.registro import Registro, RegistroBase

from datetime import datetime, time

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
        turnos = [
            (time(7,40), time(11,40)),
            (time(13,10), time(17,20)),
            (time(17,40), time(21,30))
        ]

        for inicio, fin in turnos:
        
    
            if( inicio < hora < fin):
                return fin
        


        

        
            

    def prestar(self, usuario: User, registro_base: RegistroBase):

        #Esto me tiene que devolver Disponible, No disponible
        estado = self.biblioteca.buscarEstado(registro_base.element_id)
        if(estado == "Disponible"):
            elemento = self.biblioteca.buscarElemento()
            cantidad = registro_base.cantidad

            ahora = datetime.now()
            fecha = ahora.date()
            hora = ahora.time()


            if(usuario.id):
                
                if isinstance(elemento, StockItem):
                    #Esto es un booleano
                    isReusable = elemento.isReusable

                    if(isReusable):
                        estado = "En curso"
                        expiracion = self.calcularExpiracion(hora)

                        nRegistro = Registro(
                            element_id=registro_base.element_id,
                            cantidad = cantidad,
                            destino = registro_base.destino,
                            usuario_id=usuario.id,
                            fecha=fecha,
                            hora=hora,
                            expiracion=expiracion,
                            estado=estado

                        )
                        self.biblioteca.crearRegistro(nRegistro)
                        
                    #Porque si no es reusable es consumible y no lo voy a tener que esperar a que sea devuelto
                    else:
                        estado = "Consumido"
                        expiracion = None

                        nRegistro = Registro(
                            element_id=registro_base.element_id,
                            cantidad = cantidad,
                            destino = registro_base.destino,
                            usuario_id=usuario.id,
                            fecha=fecha,
                            hora=hora,
                            expiracion=expiracion,
                            estado=estado

                        )
                        self.biblioteca.crearRegistro(nRegistro)

                    
                
            else:
                self.usuarios.crear_usuario(usuario)
                self.biblioteca.crearRegistro(Registro)




                
