from Conexiones.conexion import Conexion
from Modelos.biblioteca import Libro, Stock_biblioteca, UniqueI_biblioteca

class biblioRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = conexion.cur()

    def crearLibro(self, nLibro: Libro):
        titulo = nLibro.nombre
        descripcion = nLibro.descripcion
        estado = nLibro.estado
        ubicacion = nLibro.ubicacion
        ubicacion_interna = nLibro.ubicacion_interna
        isbn = nLibro.ISBN
        autor = nLibro.autor
        editorial = nLibro.editorial
        categoria = nLibro.categoria
        publicacion_year = nLibro.publicacion_year
        impresion_year = nLibro.impresion_year
        pais  = nLibro.pais

        self.cur.execute("""
                 INSERT INTO libros 
                 (titulo, 
                 descripcion, 
                 estado, 
                 ubicacion, 
                 ubicacion_interna, 
                 ISBN, 
                 autor, 
                 editorial, 
                 categoria, 
                 publicacion_year, 
                 impresion_year, 
                 pais)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
                 """,
                 
                 (titulo,
                  descripcion, 
                  estado, 
                  ubicacion, 
                  ubicacion_interna, 
                  isbn, 
                  autor, 
                  editorial, 
                  categoria, 
                  publicacion_year, 
                  impresion_year, 
                  pais))
        self.conexion.commit()
