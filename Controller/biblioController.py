from fastapi import FastAPI
from Servicio.biblioService import BiblioService
from Modelos.biblioteca import Libro

class BiblioController:
    def __init__(self, servicio: BiblioService):
        self.servicio = servicio

    def rutas(self, app: FastAPI):

        @app.get("/")
        def corriendose():
            return {"Mensaje": "Corriendose"}

        @app.get("/biblioteca/verlibros")
        def ver_libros():
            return self.servicio.verLibros()
        
        @app.get("/biblioteca/buscarelemento/{element_id}")
        def buscar_libro(element_id: int):
            elemento = self.servicio.buscarObjeto(element_id)

            return elemento
        
        @app.post("/biblioteca/crearlibro")
        def crear_libro(libro: Libro):
            self.servicio.crearLibro(libro)
        return {"mensaje": "creado"}
            