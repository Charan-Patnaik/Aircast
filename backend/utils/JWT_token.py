from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from schemas.User import TokenData
from typing import List, Optional, Union

load_dotenv()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm = os.environ.get('ALGORITHM'))
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,  os.environ.get('SECRET_KEY'), algorithms=os.environ.get('ALGORITHM'))
        email: str = payload.get("email")

        
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(id = payload.get("id"), email=email)
        return token_data
    except (JWTError):
        raise credentials_exception
    