from Modelos.element import UniqueItem, StockItem


#Pensar si nombre = Titulo 
class Libro(UniqueItem):
    def __init__(self, 
                id_element, 
                nombre, 
                descripcion, 
                estado, 
                ubicacion, 
                ubicacion_interna, 
                ISBN,
                autor,
                titulo, 
                editorial, 
                categoria, 
                publicacion_year,
                impresion_year,
                pais):

        super().__init__(id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna)
        self.ISBN = ISBN
        self.autor = autor
        self.titulo = titulo
        self.editorial = editorial
        self.categoria = categoria
        self.publicacion_year = publicacion_year
        self.impresion_year = impresion_year

#Stock_biblioteca = calculadoras, mapas, reglas,etc
class Stock_biblioteca(StockItem):
    def __init__(id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna, cantidad, disponibles, isReusable):
        super().__init__(id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna, cantidad, disponibles, isReusable)

class UniqueI_bibioteca(UniqueItem):
    def __init(id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna):
        super().__init__(id_element, nombre, descripcion, estado, ubicacion, ubicacion_interna)



        