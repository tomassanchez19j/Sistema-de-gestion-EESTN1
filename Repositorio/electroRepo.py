from Conexiones.conexion import Conexion
from Modelos.electro import herramientas_stock, herramientas_unicas
from Modelos.registro import Registro, RegistroBase
from Repositorio import repositorio

class HerramientasStockRepo(repositorio):
    def __init__(self, esquema,conexion : Conexion):
        super().__init__(esquema, conexion)
        self.cur = conexion.cursor()
    def crear_tabla_herramientas_stock(self):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.esquema}.herramientas_stock (id_element_stock SERIAL PRIMARY KEY,  nombre VARCHAR(30) NOT NULL, descripcion TEXT, estado TEXT, ubicacion TEXT, ubicacion_interna TEXT, tipo TEXT , cantidad  INTEGER, disponibles INTEGER, reusable BOOLEAN)")
                self.conexion.commit()
        except Exception as e:
                self.conexion.rollback()
                raise RuntimeError(f"hubo un error al crear la tabla: {e}")
    def crear_herramienta_stock(self, data: dict):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"INSERT INTO {self.esquema}.herramientas_stock(nombre, descripcion, estado, ubicacion, ubicacion_interna ,tipo,cantidad,disponibles, reusable) VALUES (%(nombre)s, %(descripcion)s,%(estado)s,%(ubicacion)s,%(ubicacion_interna)s,%(tipo)s,%(cantidad)s,%(disponibles)s,%(reusable)s) RETURNING id_element_stock", 
                                data)
                id_element_stock = cur.fetchone()[0]
            self.conexion.commit()
            return id_element_stock
        except Exception as e:
            self.conexion.rollback()
            raise RuntimeError(f"hubo un error en la base de datos herramientas_inventario al crear una nueva herramienta: {e}")
    def ver_herramientas_stock(self):
            try:
                with self.conexion.cursor() as cur:
                  
                    cur.execute(f"SELECT * FROM {self.esquema}.herramientas_stock")
                    registros = cur.fetchall()
                    if registros is None:
                        return None
                    lista_heramientas_stock = []
                    for registro in registros:
                        herramientas = herramientas_stock( 
                                id_element= registro[0],
                                nombre= registro[1],
                                descripcion=registro[2],
                                estado= registro[3],
                                ubicacion=registro[4],
                                ubicacion_interna=registro[5],
                                tipo=registro[6],
                                cantidad=registro[7],
                                disponibles=registro[8],
                                isReusable= registro[9]
                                )
                    lista_heramientas_stock.append(herramientas)
                        
                    return lista_heramientas_stock
            except Exception as e:
                raise RuntimeError (f"hubo un error en la base de datos al querer recuperar las herramientas: {e}")
    def ver_herramienta_stock_nombre(self, nombre: str):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.esquema}.herramientas_stock WHERE nombre = %s", (nombre,))
                registro = cur.fetchone()
                if registro is None:
                    return None
                herramienta = herramientas_stock( 
                    id_element=registro[0], 
                    nombre=registro[1], 
                    descripcion=registro[2], 
                    estado=registro[3], 
                    ubicacion=registro[4], 
                    ubicacion_interna=registro[5],  
                    tipo=registro[6],
                    cantidad= registro[7],
                    disponibles = registro[8],
                    isReusable=registro[9]
                        )
                return herramienta
            
        except Exception as e:
            raise RuntimeError(f"hubo un error en la base de datos al querer recuperar una herramienta: {e}")
    
        pass
    def actualizar_cantidad_stock(self,id_element_stock:int, nCantidad: int):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"UPDATE {self.esquema}.herramientas_stock SET cantidad = %s WHERE id_element_stock = %s",(nCantidad, id_element_stock))
                self.conexion.commit()
        except Exception as e:
             raise RuntimeError(f"hubo un error en la base de datos al actualizar la cantidad: {e}")
    def actualizar_estado_id_stock(self,id_herramienta_stock : int, nEstado: str):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"UPDATE {self.esquema}.herramientas_stockSET estado = %s WHERE id_element_stock = %s",(nEstado, id_herramienta_stock))
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise RuntimeError(f"error al alctualizar estado en la tabla herramientas_stock: {e}")
    def ver_estado_herramienta_stock(self, id_element_stock: int):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT estado FROM {self.esquema}.herramientas_stockWHERE id_element_stock = %s",(id_element_stock,))
                estado_herramienta_stock = cur.fetchone()[0]
                return estado_herramienta_stock
        except Exception as e:
            raise ValueError(f"ocurrio un error en la consulta de estado: {e}")
    def eliminar_herramienta_stock(self,id_herramienta_stock:int):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"DELETE FROM {self.esquema}.herramientas_stockWHERE id_element_stock = %s",(id_herramienta_stock,))
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise ValueError(f"error al eliminar una herramienta: {e}")



class HerramientasUnicasRepo(repositorio):
    def __init__(self, esquema,conexion : Conexion):
        super().__init__(esquema, conexion)
        self.cur = conexion.cursor()
    def crear_tabla_herramientas_unicas(self):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.esquema}.herramientas_unicas  (id_element_unicos SERIAL PRIMARY KEY,  nombre VARCHAR(30) NOT NULL, descripcion TEXT, estado TEXT, ubicacion TEXT, ubicacion_interna TEXT, tipo TEXT , codigo_interno   TEXT)")
                self.conexion.commit()
        except Exception as e:
                self.conexion.rollback()
                raise RuntimeError(f"hubo un error al crear la tabla herramientas_unicas: {e}")
    def crear_herramientas_unicas(self, data : dict):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"INSERT INTO {self.esquema}.herramientas_unicas (nombre, descripcion, estado, ubicacion, ubicacion_interna ,tipo,codigo_interno) VALUES (%(nombre)s, %(descripcion)s,%(estado)s,%(ubicacion)s,%(ubicacion_interna)s,%(tipo)s,%(codigo_interno)s) RETURNING id_element_unicos", 
                                data)
                id_element_unicos = cur.fetchone()[0]
                self.conexion.commit()
                return id_element_unicos
        except Exception as e:
            self.conexion.rollback()
            raise  RuntimeError(f"hubo un error en la base de datos {self.esquema}.herramientas_unicas al crear una nueva herramienta: {e}")
    def ver_herramientas_unicas(self):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.esquema}.herramientas_unicas")
                registros = cur.fetchall()
                if registros is None:
                        return None
                lista_herramientas_unicas = []
                for registro in registros:
                
                    herramientas = {self.esquema}.herramientas_unicas( 
                            id_element= registro[0],
                            nombre= registro[1],
                            descripcion=registro[2],
                            estado= registro[3],
                            ubicacion=registro[4],
                            ubicacion_interna=registro[5],
                            tipo=registro[6],
                            codigo_interno= registro[7]
                            )
                    lista_herramientas_unicas.append(herramientas)
                return lista_herramientas_unicas
        except Exception as e:
            raise RuntimeError(f"error al traer los elementos de herramientas_unicas: {e}")
    def ver_herramientas_unicas_nombre(self,nombre: str):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.esquema}.herramientas_unicas WHERE nombre = %s",(nombre,))
                registro = cur.fetchone()
                if registro is None:
                    return None
                herramientaUnicas = herramientas_unicas( 
                    id_element=registro[0], 
                    nombre=registro[1], 
                    descripcion=registro[2], 
                    estado=registro[3], 
                    ubicacion=registro[4], 
                    ubicacion_interna=registro[5],  
                    tipo=registro[6],
                    codigo_interno = registro[7]
                        )
                return herramientaUnicas
        except Exception as e:
            raise RuntimeError(f"error al traer la herramienta unica: {e}")
   
        pass
    def actualizar_estado_id_unicos(self, id_element_unicos: int ,nEstado: str):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"UPDATE {self.esquema}.herramientas_unicas SET estado =%s WHERE id_element_unicos = %s" ,(nEstado, id_element_unicos))
                self.conexion.commit()
        except Exception as e:
            raise RuntimeError(f"error al actualizar estado de herremientas_unicas: {e}")
    def ver_estado_herramienta_unicos(self, id_element_unicos: int):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT estado FROM {self.esquema}.herramientas_unicas WHERE = %(id_element_unicos)s",(id_element_unicos))
                estado_herramient_unica = cur.fetchone()
                return estado_herramient_unica
        except Exception as e:
            raise ValueError("ocurrio un error en la consulta de estado")
    def eliminar_herrmienta_unica(self,id_herramienta_unica: int):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"DELETE * FROM {self.esquema}.herramientas_unicas WHERE id_element_unicos = %(id_herramienta_unica)s",(id_herramienta_unica))
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            raise ValueError(f"error al eliminar una herramienta unica: {e}")




class RegistroElectromecanicaRepo(repositorio):
    def __init__(self, esquema,conexion : Conexion):
        super().__init__(esquema, conexion)
        self.cur = conexion.cursor()
    def crear_tabla_id_herramientas(self):
        try: 
            with self.conexion.cursor() as cur:
                cur.execute("CREATE TABLE herramientas_ids (id SERIAL PRIMARY KEY,id_stock REFERENCES herramientas_stock(id_element_stock), id_unica REFERENCES {self.esquema}.herramientas_unicas(id_element_unicos), CHECK ((id_stock IS NOT NULL AND id_unica IS NULL) OR (id_stock IS NULL AND id_unica IS NOT NULL)))")
        except Exception as e:
            raise RuntimeError(f"error al crear las base de datos: {e}")
    def crear_tabla_registro_electromecanicas(self):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f'CREATE TABLE {self.esquema}.registro_electromecanica (registro_id INTEGER PRIMARY KEY,element_id INTEGER ,cantidad INTEGER, destino TEXT, id_user INTEGER,fecha TEXT, hora TEXT, expiracion TEXT, estado TEXT)')
            print("Intentando guardar cambios...")
            self.conexion.commit()
            print("Commit realizado correctamente.")
        except Exception as e:
            raise RuntimeError(f"error al crear las base de datos: {e}")
    def crear_registro_stock(self, data:dict):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"INSERT INTO {self.esquema}.registro_electromecanica (element_id,usuario_id,cantidad, fecha, hora,expiracion, estado, destino ) VALUES (%(element_id)s, %(usuario_id)s,%(cantidad)s,%(fecha)s,%(hora)s,%(expirencia)s, %(estado)s,%(destino)s)",( data))
                self.conexion.commit()
        except Exception as e:
            raise RuntimeError(f"error al crear un registro")
    def crear_registro_unica(self, data:dict):
        try: 
            with self.conexion.cursor() as cur:
                cur.execute(f"INSERT INTO {self.esquema}.registro_electromecanica (usuario_id, element_id,cantidad, fecha, hora,expiracion, estado, destino ) VALUES (%(usuario_id)s, %(eleament_id)s,%(cantidad)s,%(fecha)s,%(hora)s,%(expirencia)s, %(estado)s,%(destino)s)",(data))
                self.conexion.commit()
        except Exception as e:
            raise RuntimeError(f"error al crear un registro")
    def mostrar_registros(self):
        try:
            with self.conexion.cursor() as cur:
                cur.execute(f"SELECT * FROM {self.esquema}.registro_electromecanica")
                registros = cur.fetchall()
                lista_de_registro=[]
                for registro in registros:
                    registro_herramienta = Registro(
                        registro_id= registro[0],
                        element_id= registro[1],
                        cantidad=registro[2],
                        destino= registro[3],
                        usuario_id=registro[4],
                        fecha=registro[5],
                        hora= registro[6],
                        expiracion= registro[7],
                        estado= registro[8],
                    )
                    lista_de_registro.append(registro_herramienta)
                return lista_de_registro
        except Exception as e:
            raise RuntimeError(f"error al traer la los datos de registros: {e}")