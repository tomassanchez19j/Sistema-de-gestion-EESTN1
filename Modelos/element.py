class Element:
    #ubicacion interna es en que stand lo ponen, ubicacion es el area(biblioteca, pañol, laboratorio, etc)
    def __init__(self, id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna ):
        self.id = id_element
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.ubicacion = ubicacion
        self.ubicacion_interna = ubicacion_interna

#UniqueItem es para los ojetos unicos como las computadoras o herramientas unicas
#StockItem para objetos que tengan mucha cantidad(escofinas, destornilladores, etc)
#En categoria hay que clasificar ej para herramientas(heramienta  de mano, de electricidad, etc)
class UniqueItem(self, marca, categoria, modelo):
    def __init__(Self, marca, categoria, modelo):
        self.marca = marca
        self.categoria = categoria
        self.modelo = modelo



class StockItem(self, marca, categoria, modelo, cantidad, disponible, isReusable):

