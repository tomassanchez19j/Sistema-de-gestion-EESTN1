from Conexiones.conexion import Conexion
from Modelos.biblioteca import Libro, Stock_biblioteca, UniqueI_biblioteca
from Modelos.registro import Registro
class BiblioRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = conexion.cur()

    def crearLibro(self, nLibro: Libro):
        #me retorno el id q crea cuando lo ingreso a la tabla
        #necesito ese id para poder crear ingresar el libro en la tabla libros pq esta como fk
        self.cur.execute("""
            INSERT INTO inventario (nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo)
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING element_id""", (
            nLibro.nombre,
            nLibro.descripcion,
            nLibro.estado,
            nLibro.ubicacion,
            nLibro.ubicacion_interna,
            nLibro.tipo
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
                    tipo=registro[7],
                    ISBN=registro[8],
                    autor=registro[9], 
                    editorial=registro[10],
                    categoria=registro[11], 
                    publicacion_year=registro[12], 
                    impresion_year=registro[13], 
                    pais=registro[13] )
            
            libros.append(nLibro)

        return libros
    
    def buscarLibro(self, libro_id):
        self.cur.execute("""
        SELECT i.element_id, i.nombre, i.descripcion, i.estado, i.ubicacion, i.ubicacion_interna, i.tipo,
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
                    tipo=res[7],
                    ISBN=res[8],
                    autor=res[9], 
                    editorial=res[10],
                    categoria=res[11], 
                    publicacion_year=res[12], 
                    impresion_year=res[13], 
                    pais=res[14] )
        
        return nLibro
    
    def buscarElemento(self, id_element):
        #Necesito una funcion q me retorne el elemento q se esta solicitando
        #Tengo q hacer un Left Join
        #Hago un select de todas las tablas q me interesan(inventario, libros, stockItem, uniqueItem (i,l,s,u))

        self.cur.execute("""
        SELECT i.*, l.*, s.*, u*
        FROM inventario i
        LEFT JOIN libros l ON l.inventario_id = i.element_id
        LEFT JOIN stockitem_library s on s.inventario_id = i.element_id
        LEFT JOIN uniqueitem_library u on u.inventario_id = i.element_id
        WHERE element_id = (%s)
        """, (id_element))

        res = self.cur.fetchone()

        idElement = res[0]
        nombre = res[1]
        descripcion = res[2]
        estado = res[3]
        ubicacion = res[4]
        ubicacion_interna = res[5]
        tipo = res[6]

        if (tipo == "Libro"):

            nLibro = Libro(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            codigo_interno=res[8],
            ISBN=res[9],
            autor=res[10], 
            editorial=res[11],
            categoria=res[12], 
            publicacion_year=res[13], 
            impresion_year=res[14], 
            pais=res[15])
        
            return nLibro
        
        elif(tipo =="UniqueI_biblioteca"):
            nUniqueI_Biblioteca = UniqueI_biblioteca(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            codigo_interno=res[8],

            )
            return nUniqueI_Biblioteca
        
        elif(tipo=="Stock_biblioteca"):
            nStock_biblioteca = Stock_biblioteca(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            cantidad=res[8],
            disponibles=res[9],
            isReusable= res[10]
            )

            return nStock_biblioteca
        



    
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

    
