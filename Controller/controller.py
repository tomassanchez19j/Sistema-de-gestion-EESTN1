from fastapi import FastAPI, HTTPException
from Servicio.servicio import Servicio
from Modelos.element import Element
#ver como se hace un prefix en fastapi
#200 ok
#201 creado
#400 Bad request(dato invalido)
#404 not found
#401 Unauthorized
#500 Internal error
class Controller:
    def _init__(self, servicio: Servicio, prefix):
        self.servicio = servicio
        self.prefix = prefix

    def rutas(self, app: FastAPI):
        @app.get("/")
        def corriendose():
            return {"Mensaje": "Corriendose"}
        
        @app.get(f"{self.prefix}/inventario")
        def verElementos(self):
            try:
                res = self.servicio.verInventarioAll()
                return res
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"{res["message"]}")

        @app.get(f"{self.prefix}/elemento/{{id_element}}")
        def verElemento(id_element):
           try:
                res = self.servicio.buscarElemento(id_element)
                #recordar que res es un diccionario succes:bool
                if res["success"]:
                    return res
                else:
                    raise HTTPException(status_code=404, detail=res["message"])

           except Exception as e:
               raise HTTPException(status_code=500, detail=f"Error al obtener elemento: {str(e)}")
        
        @app.post(f"{self.prefix}/nuevoitem")
        def crearElement(elemento: Element):
            try:
                res = self.servicio.crearElement(elemento)
                if res["success"]:
                    return res
                else:
                    raise HTTPException(status_code=404, detail=f"{res["message"]}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al cargar elemento: {str(e)}")
            
        @app.delete(f"{self.prefix}/elemento/{{id_element}}")
        def borrarElement(id_element):
            try:
                res = self.servicio.borrarElemento(id_element)
                if res["message"]:
                    return res
                else:
                    raise HTTPException(status_code=404, detail=f"{res["message"]}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al eliminar elemento: {str(e)}")
            

            
    