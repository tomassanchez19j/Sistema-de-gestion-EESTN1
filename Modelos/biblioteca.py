from Modelos.element import UniqueItem, StockItem

#Nombre = Titulo del libro
#En la tabla libros va titulo en vez de nombre.
class Libro(UniqueItem):
    ISBN: str
    autor: str
    editorial: str
    categoria: str
    publicacion_year: int
    impresion_year: int
    pais: str

#Stock_biblioteca = calculadoras, mapas, reglas, etc
#UniqueI_biblioteca = objetos unicos como las compus, cargadores, teles








