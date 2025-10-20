from datetime import datetime, timedelta, timezone
import os
import jwt
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type:str

class PayloadData():
    def __init__(self, id, email):
        self.id = id
        self.email = email
        #expiracion
        self.exp = datetime.now(timezone.utc) + timedelta(minutes=30)
        #emision
        self.iat = datetime.now(timezone.utc)


class TokenManager:
    def __init__(self, algorithm, secret_key):
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.expiracion = 30
        
    def tokenResponse(self, user_id, email):
        try:
            payload_data=PayloadData(id=user_id, email=email)
            payload_data_dict=payload_data.__dict__

            token_jwt=jwt.encode(
                payload=payload_data_dict,
                key=self.secret_key,
                algorithm=self.algorithm
            )
        
            return Token(acces_token=token_jwt, token_type="bearer")
        except Exception as e:
            raise e
        
    
    def validarToken(self, token:str):
        try:
            payload=jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            return {"success": False, "message":"Token expirado"}
        
        except jwt.InvalidTokenError:
            return {"succes": False, "message": "Token invalido"}
    
