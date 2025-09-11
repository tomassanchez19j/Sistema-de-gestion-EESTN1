#Cada cosa que se preste va a saltar como registro. Si queremos ver que cosas se sacaron al mismo tiempo por una persona hacemos un join
#Estado es para saber si ya se entregaron o no(capazbuscar otro nombre mas especifico)

#Expiracion: las cosas del pañol tendrian que tener de expiracion el tiempo que falte para que se cierren los
#pañoles o y la biblioteca (entregar antes de las 21:30, 17:20) 


#ver si se puede agregar un atributo "Destino" que diga hacia donde va,
#en el caso del alumno es facil identificar el destino(tiene un atributo curso)
#pero en el caso de un profesor es una relacion de uno a muchos cursos

#clase abstracta
class Registro:
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado):
        self.usuario_id = usuario_id
        self.elemento_id = elemento_id
        self.hora = hora
        self.expiracion = expiracion
        self.estado = estado
        self.destino = destino

class RegistroStock(Registro):
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado, cantidad):
        super().__init__(self, usuario_id, elemento_id, hora, expiracion, estado)
        self.cantidad = cantidad


#Para items unicos: computadoras, libros, etc
class RegistroItem(Registro):
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado):
        super().__init__(self, usuario_id, fecha, hora, expiracion, estado):

