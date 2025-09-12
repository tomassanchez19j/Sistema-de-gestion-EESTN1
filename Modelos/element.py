class Element:
    #ubicacion interna es en que stand lo ponen, ubicacion es el area(biblioteca, pañol, laboratorio, etc)
    #Estado: disponible, en uso, no disponible
    def __init__(self, nombre, descripcion, estado, ubicacion, ubicacion_interna, id_element=None):
        self.id_element = id_element
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.ubicacion = ubicacion
        self.ubicacion_interna = ubicacion_interna
        

#UniqueItem es para los ojetos unicos como las computadoras o herramientas
#StockItem para objetos que tengan mucha cantidad(escofinas, destornilladores, etc)
#En categoria hay que clasificar ej para herramientas(heramienta  de mano, de electricidad, etc)
class UniqueItem(Element):
    def __init__( self, nombre, descripcion, estado, ubicacion, ubicacion_interna, id_element=None):
        super().__init__( nombre, descripcion, estado, ubicacion, ubicacion_interna,  id_element)



#El isReusable es para las cosas que son reusables(es bool) o no
#Es reusable una escofina, una sierra. No es reusable un clavo, los guantes descartables del laboratorio, etc


#Disponible es un int, cuantas cantidades quedan disponibles de esa cosa
class StockItem(Element):
    def __init__(self, nombre, descripcion, estado, ubicacion, ubicacion_interna, cantidad, disponibles, isReusable, id_element=None):
        super().__init__( nombre, descripcion, estado, ubicacion, ubicacion_interna, id_element)    
        self.cantidad = cantidad
        self.disponibles = disponibles
        self.isReusable = isReusable

