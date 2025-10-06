from Conexiones.conexion import Conexion
from Modelos.element import Element, StockItem, UniqueItem
from Modelos.registro import Registro

#30/9 Las funciones que me faltan son la de actualizar campo y testear todo este repo
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

    #  Ver como puedo implementar este  metodo en bibliotecaRepo(aplicar hipermorfismo)
    #  biblioteca deberia ver hacer un if instance para Libro, buscar como realizarlo
    def crearElement(self, elemento: Element):
        try:
            nombre = elemento.nombre
            descripcion = elemento.descripcion
            estado = elemento.estado
            ubicacion= elemento.ubicacion
            ubicacion_interna = elemento.ubicacion_interna
            tipo = elemento.ubicacion_interna

            self.cur.execute("""
            INSERT INTO inventario(nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo)
            VALUES (%s,%s,%s,%s,%s, %s)
            RETURNING element_id
            """, (nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo))

            #-- Me traigo el id para poder poner el objeto en su respectiva tabla --
            element_id = self.cur.fetchone()[0]
            self.conexion.commit()

            if isinstance(elemento, StockItem):
                cantidad= elemento.cantidad
                disponibles= elemento.disponibles
                isReusable= elemento.isReusable

                self.cur.execute("""
                INSERT INTO stockitems(inventario_id, cantidad, disponibles, isreusable)
                VALUES (%s,%s,%s,%s)
                """, (element_id, cantidad, disponibles, isReusable))

                self.conexion.commit()
                return element_id

            else:
                codigo_interno = elemento.codigo_interno
                self.cur.execute("""
                INSERT INTO uniqueitems(inventario_id, codigo_interno)
                VALUES (%s, %s)                
                """, (element_id, codigo_interno))

                self.conexion.commit()
                return element_id
            
        except Exception as e:
            self.conexion.rollback()
            raise e
        


    #Nota: hago un metodo buscarElemento general, todos los elementos del sistema pueden ser
    def buscarElemento(self, id_element):
        #Necesito una funcion q me retorne el elemento q se esta solicitando
        #Tengo q hacer un Left Join
        #Hago un select de todas las tablas q me interesan(inventario, stockItem, uniqueItem (i,l,s,u))

        self.cur.execute("""
        SELECT i.*, s.*, u.*
        FROM inventario i
        LEFT JOIN stockitems s on s.inventario_id = i.element_id
        LEFT JOIN uniqueitems u on u.inventario_id = i.element_id
        WHERE element_id = (%s);
        """, (id_element,))

        res = self.cur.fetchone()

        idElement = res[0]
        nombre = res[1]
        descripcion = res[2]
        estado = res[3]
        ubicacion = res[4]
        ubicacion_interna = res[5]
        tipo = res[6]

        
        if(tipo =="Uniqueitem"):
            nUniqueitem= UniqueItem(
            id_element=idElement,
            nombre=nombre,
            descripcion=descripcion,
            estado=estado,
            ubicacion=ubicacion,
            ubicacion_interna=ubicacion_interna,
            tipo=tipo,
            codigo_interno=res[7],

            )
            return nUniqueitem
        
        elif(tipo=="Stockitem"):
            nStockitem = StockItem(
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

            return nStockitem
        
        
    def borrarElemento(self, element_id):
        try:
            self.cur.execute("DELETE FROM inventario WHERE element_id = (%s)", (element_id))

        except Exception as e:
            self.conexion.rollback()
            raise e
    
    #Funcion para actualizar el estado de cualquier elemento
    def actEstado(self, id_element, nEstado):
        try:
            self.cur.execute("""
            UPDATE inventario
            SET estado = (%s)
            WHERE element_id = (%s);             
            """, (nEstado, id_element))

            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise e

    def buscarEstado(self, id_element):
        try:
            self.cur.execute("""
            SELECT estado FROM inventario
            WHERE element_id = (%s)
            """, (id_element,))

            res = self.cur.fetchone()
            return res[0]

        except Exception as e:
            self.conexion.rollback()
            raise e
    
    
    #Funcion para actualizar cantidad y disponibles
    #Si el se trata de un objeto que no es reusable se descuenta la cantidad
    #Si se trata de un ojeto reusable solo se descuentan los disponibles

    def actDisponibles(self, id_element, pCantidad):
        try:
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

        except Exception as e:
            self.conexion.rollback()
            raise e
        

    #   Dejo varios metodos para poder traerme los registros
    #   Esto es me trae todo lo del invnteraio(sin las relaciones de demas lados)
    #   Ver que hacer aca en para luego implementarlo en biblioteca(ver caso con libros)
    def verInventarioAll(self):
        self.cur.execute("""
        SELECT element_id, nombre, descripcion, estado, ubicacion, ubicacion_interna, tipo FROM inventario;""")

        res = self.cur.fetchall()
        inventario = []

        for i in res:
            if(i[6] == "Uniqueitem"):
                n = UniqueItem(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
            elif(i[6] == "Stockitem"):
                n = StockItem(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])

            inventario.append(n)
        
        return inventario

    

        
    def crearRegistro(self, registro: Registro):
        try:
            self.cur.execute("""
            INSERT INTO registros(usuario_id, element_id, cantidad, fecha, hora, expiracion, estado, destino)
            VALUES (%s,%s,%s,%s,%s,%s,%s, %s);""", (
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

        except Exception as e:
            self.conexion.rollback()
            raise e
        


    def verRegistros(self):
        self.cur.execute("""
        SELECT registro_id, usuario_id, element_id, cantidad, fecha, hora, expiracion, estado, destino FROM registros
        """)

        res = self.cur.fetchall()
        registros = []

        for i in res:
            n = Registro(
                registro_id=i[0], 
                element_id=i[1],
                cantidad=i[2], 
                destino=i[3], 
                usuario_id=i[4],
                fecha=i[5], 
                hora=i[6],
                expiracion=i[7], 
                estado=i[8])
            
            registros.append(n)

        return registros
    

        #Metodo para manejar la devolucion de prestamos
    def devolver(self, registro_id):
        #Terminado?Devuelto? no se me ocurre nada mas entendible
        try:

            self.cur.execute("""
            UPDATE registros
            SET estado = (%s)
            WHERE registro_id = (%s)
            ;""", ("Terminado", registro_id))

            self.conexion.commit()
        
        except Exception as e:
            self.conexion.rollback()

    




    #Tengo un problema q es q dependiendo el atributo q se quiera cambiar
    #Varia la tabla en la q esta inventario > (stockitem, uniqueitem)
        def actElemento(self, id_element, campo, nvalor):
            try:
                elemento = self.buscarElemento(id_element)
                #hasattr se fija si el elemento tiene ese atributo
                if hasattr(elemento, campo):
                    if campo in ["nombre", "descripcion", "estado", "ubicacion", "ubicacion_interna", "tipo"]:
                        self.cur.execute(f"""
                            UPDATE inventario
                            SET {campo} = %s
                            WHERE element_id = %s
                        """, (nvalor, id_element))

                    elif isinstance(elemento, StockItem) and campo in ["cantidad", "disponibles", "isReusable"]:
                        self.cur.execute(f"""
                            UPDATE stockitems
                            SET {campo} = %s
                            WHERE inventario_id = %s
                        """, (nvalor, id_element))

                    elif isinstance(elemento, UniqueItem) and campo == "codigo_interno":
                        self.cur.execute("""
                            UPDATE uniqueitems
                            SET codigo_interno = %s
                            WHERE inventario_id = %s
                        """, (nvalor, id_element))

                    else:
                        raise ValueError(f"Campo '{campo}' no valido para el elemento")

                    self.conexion.commit()
                else:
                    raise AttributeError(f"El elemento no tiene el campo {campo}")

            except Exception as e:
                self.conexion.rollback()
                raise e


        
    
    






