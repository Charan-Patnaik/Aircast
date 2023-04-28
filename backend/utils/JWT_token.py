from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from schemas.User import TokenData
from typing import List, Optional, Union

# Load the environment variables from .env file
load_dotenv()

# Create an access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    # Copy the data to encode it
    to_encode = data.copy()

    # Set the token expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    # Encode the JWT token with the secret key and algorithm from environment variables
    encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm = os.environ.get('ALGORITHM'))
    return encoded_jwt

# Verify the access token
def verify_token(token:str, credentials_exception):
    try:
        # Decode the JWT token with the secret key and algorithm from environment variables
        payload = jwt.decode(token,  os.environ.get('SECRET_KEY'), algorithms=os.environ.get('ALGORITHM'))

        # Get the email from the payload
        email: str = payload.get("email")

        # Get the token scopes and data        
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(id = payload.get("id"), email=email)
        return token_data
    except (JWTError):
        # Raise an exception if the token is invalid
        raise credentials_exception
    


def verify_token_v2(token:str) -> TokenData|None:
    try:
        # Decode the JWT token with the secret key and algorithm from environment variables
        payload = jwt.decode(token,  os.environ.get('SECRET_KEY'), algorithms=os.environ.get('ALGORITHM'))

        # Get the email from the payload
        email: str = payload.get("email")

        # Get the token scopes and data        
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(id = payload.get("id"), email=email)
        return token_data
    except Exception as e:
        # Raise an exception if the token is invalid
        print(e)
        return None
    