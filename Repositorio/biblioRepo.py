from Conexiones.conexion import Conexion
from Modelos.biblioteca import Libro
from Modelos.registro import Registro
class BiblioRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = conexion.cur()

    def crearLibro(self, nLibro: Libro):
        #me retorno el id q crea cuando lo ingreso a la tabla
        #necesito ese id para poder crear ingresar el libro en la tabla libros pq esta como fk
        self.cur.execute("""
            INSERT INTO inventario (nombre, descripcion, estado, ubicacion, ubicacion_interna)
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING element_id""", (
            nLibro.nombre,
            nLibro.descripcion,
            nLibro.estado,
            nLibro.ubicacion,
            nLibro.ubicacion_interna
        ))
        element_id = self.cur.fetchone()[0]

        self.cur.execute("""
            INSERT INTO libros (inventario_id, codigo_interno, ISBN, autor, editorial, categoria, publicacion_year, impresion_year, pais) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (

            element_id,
            nLibro.codigo_interno,
            nLibro.ISBN,
            nLibro.autor,
            nLibro.editorial,
            nLibro.categoria,
            nLibro.publicacion_year,
            nLibro.impresion_year,
            nLibro.pais

        ))

        self.conexion.commit()

    def verLibros(self):
        self.cur.execute("""
        SELECT i.element_id, i.nombre, i.descripcion, i.estado, i.ubicacion, i.ubicacion_interna,
        l.codigo_interno, l.ISBN, l.autor, l.editorial, l.categoria, l.publicacion_year, l.impresion_year, l.pais
        FROM libros l
        JOIN inventario i ON l.inventario_id = i.element_id          
        """)

        registros = self.cur.fetchall() 
        libros = [] 
        
        for registro in registros: 
            nLibro = Libro( 
                    id_element=registro[0], 
                    nombre=registro[1], 
                    descripcion=registro[2], 
                    estado=registro[3], 
                    ubicacion=registro[4], 
                    ubicacion_interna=registro[5], 
                    codigo_interno=registro[6], 
                    ISBN=registro[7],
                    autor=registro[8], 
                    editorial=registro[9],
                    categoria=registro[10], 
                    publicacion_year=registro[11], 
                    impresion_year=registro[12], 
                    pais=registro[13] )
            
            libros.append(nLibro)

        return libros
    
    def buscarLibro(self, libro_id):
        self.cur.execute("""
        SELECT i.element_id, i.nombre, i.descripcion, i.estado, i.ubicacion, i.ubicacion_interna,
        l.codigo_interno, l.ISBN, l.autor, l.editorial, l.categoria, l.publicacion_year, l.impresion_year, l.pais
        FROM libros l
        JOIN inventario i ON l.inventario_id = i.element_id
        WHERE i.element_id = (%s)         
        """, (libro_id,))

        res = self.cur.fetchone()
        nLibro = Libro( 
                    id_element=res[0], 
                    nombre=res[1], 
                    descripcion=res[2], 
                    estado=res[3], 
                    ubicacion=res[4], 
                    ubicacion_interna=res[5], 
                    codigo_interno=res[6], 
                    ISBN=res[7],
                    autor=res[8], 
                    editorial=res[9],
                    categoria=res[10], 
                    publicacion_year=res[11], 
                    impresion_year=res[12], 
                    pais=res[13] )
        
        return nLibro
    
    def buscarEstado(self, id_element):
        self.cur.execute("""
        SELECT estado FROM inventario
        WHERE element_id = (%s)
        """, (id_element,))

        res = self.cur.fetchone()
        return res[0]
    
    #Funcion para actualizar el estado de cualquier elemento
    def actEstado(self, id_element, nEstado):
        self.cur.execute("""
        UPDATE inventario
        SET estado = (%s)
        WHERE element_id = (%s)               
        """, (nEstado, id_element))
    
    def crearRegistro(self, registro: Registro):
        self.cur.execute("""
        INSERT INTO registros(usuario_id, element_id, cantidad, fecha, hora, expiracion, estado, destino)
        VALUES (%s,%s,%s,%s,%s,%s,%s, %s)""", (
            registro.usuario_id,
            registro.element_id,
            registro.cantidad,
            registro.fecha,
            registro.hora,
            registro.expiracion,
            registro.estado,
            registro.destino

        ))

        self.conexion.commit()

    
