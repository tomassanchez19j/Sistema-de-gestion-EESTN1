#Cada cosa que se preste va a saltar como registro. Si queremos ver que cosas se sacaron al mismo tiempo por una persona hacemos un join
#Estado es para saber si ya se entregaron o no(capazbuscar otro nombre mas especifico)

#Expiracion: las cosas del pañol tendrian que tener de expiracion el tiempo que falte para que se cierren los
#pañoles o y la biblioteca (entregar antes de las 21:30, 17:20) 


#ver si se puede agregar un atributo "Destino" que diga hacia donde va,
#en el caso del alumno es facil identificar el destino(tiene un atributo curso)
#pero en el caso de un profesor es una relacion de uno a muchos cursos

#clase abstracta
#11/9 Agrego id a todas las clases, les pongo 


class Registro:
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado, destino, registro_id=None):
        self.registro_id = registro_id
        self.usuario_id = usuario_id
        self.elemento_id = elemento_id
        self.fecha = fecha
        self.hora = hora
        self.expiracion = expiracion
        self.estado = estado
        self.destino = destino


class RegistroStock(Registro):
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado, destino, cantidad, registro_id=None):
        super().__init__(usuario_id, elemento_id, fecha, hora, expiracion, estado, destino, registro_id)
        self.cantidad = cantidad


class RegistroItem(Registro):
    def __init__(self, usuario_id, elemento_id, fecha, hora, expiracion, estado, destino, registro_id=None):
        super().__init__(usuario_id, elemento_id, fecha, hora, expiracion, estado, destino, registro_id)
