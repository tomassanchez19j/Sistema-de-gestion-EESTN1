import pyscopg2
import os
from dotenv import load_dotenv

load_dotenv()

class ConexionUser:

    def __init__(self):
        self.dsn = os.getenv("DSNUSER")
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor()
        
    def cur(self):
        return self.cursor

    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()
    
        
