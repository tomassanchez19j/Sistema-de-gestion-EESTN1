import pyscopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Conexion:

    def __init__(self,dsn):
        #Va a ser una  misma clase conexion para todo crea una conexion en tu repositorio y desde el  constructor pasaletu DSN que necesites
        #definido en .env 
        #mira de ejemplo userRepo
        
        self.dsn = self.dsn
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor()
        
    def cur(self):
        return self.cursor

    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()
    
        
