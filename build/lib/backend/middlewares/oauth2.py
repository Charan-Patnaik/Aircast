from fastapi import Depends, status, HTTPException
from utils.JWT_token import verify_token
from fastapi.security import (
    OAuth2PasswordBearer
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    """
    A function that returns the current user based on the authentication token provided by the user.

    Parameters:
    -----------
    token : str
        The authentication token provided by the user. Obtained through FastAPI's built-in dependency injection system.

    Returns:
    --------
    dict:
        A dictionary containing the user's information if the authentication token is valid.

    Raises:
    -------
    HTTPException:
        If the token is invalid, expired or does not contain the required information.
    """
        
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    return verify_token(token = token, credentials_exception= credentials_exception)