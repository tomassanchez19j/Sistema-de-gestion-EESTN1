from Conexiones.conexion import Conexion
from Modelos.element import StockItem, UniqueItem, Element
from Modelos.registro import RegistroBase

#Ver que seria mejor para el metodo actualizar elemento(volver a pasar un elemento ya con los nuevos valores y que se recargue)
#o simplemente actualizar por campos

class ElectroRepo:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = conexion.cur()

    def crearElement(self, elemento: Element):
        nombre = elemento.nombre
        descripcion = elemento.descripcion
        estado = elemento.estado
        ubicacion= elemento.ubicacion
        ubicacion_interna = elemento.ubicacion_interna
        tipo = elemento.ubicacion_interna

        self.cur.execute("""
        INSERT INTO inventario(nombre, descripcion, estado, ubicacion, ubicacion_interna)
        VALUES (%s,%s,%s,%s,%s)
        RETURNING element_id
        """, (nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo))

        #me trago el id para poder poner el objeto en su respectiva tabla
        element_id = self.cur.fetchone()[0]
        self.conexion.commit()

        if isinstance(elemento, StockItem):
            cantidad= elemento.cantidad
            disponibles= elemento.disponibles
            isReusable= elemento.isReusable

            self.cur.execute("""
            INSERT INTO stockitem_electro(inventario_id, cantidad, disponibles isreusable)
            VALUES (%s,%s,%s,%s)
            """, (element_id, cantidad, disponibles, isReusable))

            self.conexion.commit()

        else:
            codigo_interno = elemento.codigo_interno
            self.cur.execute("""
            INSERT INTO uniqueitem_electro(inventario_id, codigo_interno)
            VALUES (%s, %s)                
            """, (element_id, codigo_interno))

            self.conexion.commit()

    
    #Recibe el campo a cambiarse y el nuevo valor de ese campo
    def borrarElement(self, element_id):
        
        self.cur.execute("""
        DELETE * FROM inventario
        WHERE element_id = (%s)
        """, (element_id,))
    

    #capaz lo cambio pero es buena la idea de q me vuelva a llegar del frontened el objeto
    def actElemento(self, elemento: Element):
        nombre = elemento.nombre
        descripcion = elemento.descripcion
        estado = elemento.estado
        ubicacion= elemento.ubicacion
        ubicacion_interna = elemento.ubicacion_interna
        tipo = elemento.ubicacion_interna
        
        id_element = elemento.id_element

        self.cur.execute("""
        UPDATE inventario
        SET nombre = (%s)
        SET descripcion = (%s)
        SET estado = (%s)
        SET ubicacion = (%s)
        SET ubicacion_interna = (%s)
        SET tipo = (%s)
        WHERE id_element = (%s)
                         
        """, (nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo, id_element))
        
        self.conexion.commit()

        if isinstance(elemento, StockItem):

            cantidad = elemento.cantidad
            disponibles = elemento.disponibles
            isReusable = elemento.isReusable

            self.cur.execute("""
            UPDATE inventario
            SET cantidad = (%s)
            SET disponibles = (%s)
            SET isreusable = (%s)
            WHERE id_element = (%s)
            """, (cantidad, disponibles, isReusable, id_element))

            self.conexion.commit()

        else:

            codigo_interno = elemento.codigo_interno
            self.cur.execute("""
            UPDATE uniqueitem_electro
            SET codigo_interno = (%s)
            """, (codigo_interno,))

            self.conexion.commit()

    def buscarElemento(self, id_elemento):

        self.cur.execute("""
        SELECT * FROM inventario
        WHERE id_element = (%s)
        """, (id_elemento))

        resp = self.cur.fetchone()[0]
        
    