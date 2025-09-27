from Modelos import element
from Modelos.element import Element
from Repositorio.repositorio import Repositorio
from Conexiones.conexion import Conexion
from Modelos.biblioteca import Libro, Stock_biblioteca, UniqueI_biblioteca
from Modelos.registro import Registro
class BiblioRepo(Repositorio):
    def __init__(self, conexion: Conexion):
        super().__init__(conexion)
        
    def crearLibro(self, nLibro):
       
        element_id = super().crearElement()
        self.cur.execute(f"""
            INSERT INTO {"Libros"} (inventario_id, codigo_interno, ISBN, autor, editorial, categoria, 
            publicacion_year, impresion_year, pais)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        return element_id


    def verLibros(self):
        self.cur.execute("""
        SELECT i.element_id, i.nombre, i.descripcion, i.estado, i.ubicacion, i.ubicacion_interna, i.tipo,
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
                    pais=registro[14] )
            
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
        SELECT i.*, l.*, s.*, u.*
        FROM inventario i
        LEFT JOIN libros l ON l.inventario_id = i.element_id
        LEFT JOIN stockitem_library s on s.inventario_id = i.element_id
        LEFT JOIN uniqueitem_library u on u.inventario_id = i.element_id
        WHERE element_id = (%s)
        """, (id_element,))

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
            codigo_interno=res[7],
            ISBN=res[9],
            autor=res[10], 
            editorial=res[11],
            categoria=res[12], 
            publicacion_year=res[13], 
            impresion_year=res[14], 
            pais=res[15])
        
            return nLibro
        
        elif(tipo =="Uniqueitem"):
            nUniqueI_Biblioteca = UniqueI_biblioteca(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            codigo_interno=res[7],

            )
            return nUniqueI_Biblioteca
        
        elif(tipo=="Stockitem"):
            nStock_biblioteca = Stock_biblioteca(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            cantidad=res[7],
            disponibles=res[8],
            isReusable= res[9]
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

        self.conexion.commit()

    #Funcion para actualizar cantidad y disponibles
    #Si el se trata de un objeto que no es reusable se descuenta la cantidad
    #Si se trata de un ojeto reusable solo se descuentan los disponibles
    def actDisponibles(self, id_element, pCantidad):
        self.cur.execute("""
        SELECT cantidad, disponibles, isreusable
        FROM stockitem
        WHERE inventario_id = (%s)
        """, (id_element,))

        res = self.cur.fetchone()
        cantidad = res[0]
        disponibles = res[1]
        #Booleano
        isReusable = res[2]

        if(isReusable):

            if(disponibles - pCantidad  >= 0 ):
                disponibles = disponibles - pCantidad

                self.cur.execute("""
                UPDATE stockitem
                SET disponibles = (%s)
                WHERE inventario_id = (%s)
                """, (disponibles, id_element))
                self.conexion.commit()

                if(disponibles == 0):
                    self.actEstado(id_element, "No disponible")
        else:
            if(disponibles + pCantidad  >= 0):
                disponibles = disponibles - pCantidad
                nCantidad = cantidad - pCantidad

                self.cur.execute("""
                UPDATE stockitem
                SET disponibles = (%s)
                WHERE inventario_id = (%s)
                """, (disponibles, id_element))
                
                self.cur.execute("""
                UPDATE stockitem
                SET cantidad = (%s)
                WHERE inventario_id = (%s)
                """, (nCantidad, id_element))

                if(disponibles == 0):
                    self.actEstado(id_element, "No disponible")

                self.conexion.commit()

        
            
    
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

    
