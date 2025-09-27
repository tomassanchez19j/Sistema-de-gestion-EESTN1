from Conexiones.conexion import Conexion
from Modelos.element import Element, StockItem
from Modelos.registro import Registro

#Me sirve para los metodos que comparten todos los repositorios
#Metodos como los selects quizas los hago aparte.

#Clase general de repositorio, las demas clases reposotioro heredan del el
#contiene los metodos q todos los repositorios tienen en genral
#considerar el hipermorfismos de los repositorios
#vease el caso de crearElement que puede instanciar elemento unicos o de stock pero en el caso de una bd como biblioteca
#se necesita la instancia del objeto LIbro  si o si

class Repositorio:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion
        self.cur = self.conexion.cur()


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

        #Me traigo el id para poder poner el objeto en su respectiva tabla
        element_id = self.cur.fetchone()[0]
        self.conexion.commit()

        if isinstance(elemento, StockItem):
            cantidad= elemento.cantidad
            disponibles= elemento.disponibles
            isReusable= elemento.isReusable

            self.cur.execute("""
            INSERT INTO stockitems(inventario_id, cantidad, disponibles isreusable)
            VALUES (%s,%s,%s,%s)
            """, (element_id, cantidad, disponibles, isReusable))

            self.conexion.commit()

        else:
            codigo_interno = elemento.codigo_interno
            self.cur.execute("""
            INSERT INTO uniqueitems(inventario_id, codigo_interno)
            VALUES (%s, %s)                
            """, (element_id, codigo_interno))

            self.conexion.commit()

    
    #Funcion para actualizar el estado de cualquier elemento
    def actEstado(self, id_element, nEstado):
        self.cur.execute("""
        UPDATE inventario
        SET estado = (%s)
        WHERE element_id = (%s)               
        """, (nEstado, id_element))

        self.conexion.commit()

    def buscarEstado(self, id_element):
        self.cur.execute("""
        SELECT estado FROM inventario
        WHERE element_id = (%s)
        """, (id_element,))

        res = self.cur.fetchone()
        return res[0]
    
    #Funcion para actualizar cantidad y disponibles
    #Si el se trata de un objeto que no es reusable se descuenta la cantidad
    #Si se trata de un ojeto reusable solo se descuentan los disponibles

    def actDisponibles(self, id_element, pCantidad):
        self.cur.execute("""
        SELECT cantidad, disponibles, isreusable
        FROM stockitems
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
                UPDATE stockitems
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
                UPDATE stockitems
                SET disponibles = (%s)
                WHERE inventario_id = (%s)
                """, (disponibles, id_element))
                
                self.cur.execute("""
                UPDATE stockitems
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

    






