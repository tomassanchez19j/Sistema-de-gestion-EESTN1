from Modelos.element import Element, UniqueItem, StockItem


#Pensar si nombre = Titulo 
class Libro(StockItem):
    def __init__(self, 
                id_element, 
                nombre, 
                descripcion, 
                estado, 
                ubicacion, 
                ISBN,
                ubicacion_interna, 
                autor,
                titulo, 
                editorial, 
                categoria, 
                publicacion_year,
                pais):
        