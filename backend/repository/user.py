from sqlalchemy.orm import Session
from models.User import UserModel
from schemas.User import LoginResponse, User, Role
from utils import hashing, JWT_token
from fastapi import status
from fastapi.responses import JSONResponse
from schemas.Responses import response
from sqlalchemy import or_
import uuid


def create(request: User, db: Session):
    """
    Create a new user in the database if the email or username provided does not already exist.

    Args:
    - request (User): User object containing the username, email, and password for the new user.
    - db (Session): Database session object.

    Returns:
    - JSONResponse: A JSON response containing a success message and status code 201 if the user is created successfully, otherwise a JSON response with a conflict message and status code 409.
    """
    
    try:
        user = db.query(UserModel).filter(or_(UserModel.email == request.email, UserModel.username == request.username)).first()

        if user:
            return response.conflict(f"User with the email '{request.email}' or username '{request.username}' already exists!")


        new_user = UserModel(username=request.username, email=request.email, password= hashing.Hash().get_hashed_password(request.password), planId = request.planId, apiKey = str(uuid.uuid4()), userType = 2)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return JSONResponse(
            status_code = status.HTTP_201_CREATED,
            content= {
                "success": True,
                "message": f"User with username '{request.username}' registered successfully!"
            }
        )
        
    except Exception as e:
        print(e)
        return response.bad_request(f"Internal server exception {str(e.with_traceback)}")
    

def find_user(username: str, password: str, db: Session):
    """
    Find a user with the given username and verify the provided password matches the hashed password in the database.

    Args:
    - username (str): Username of the user to search for.
    - password (str): Password provided by the user to verify.
    - db (Session): Database session object.

    Returns:
    - LoginResponse: A LoginResponse object containing the username, email, access token, and token type if the user is found and the password is correct. Otherwise, returns a JSON response with an error message and status code 404 if the user is not found, or a JSON response with an error message and status code 401 if the password is incorrect.
    """
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        return response.not_found(f"User with the username '{username}' not found")

    
    if not hashing.Hash().verify_password(user.password, password=password):
        return JSONResponse(
                status_code= status.HTTP_401_UNAUTHORIZED,
                content= {
                "success": True,
                "message": f"Invalid username or password!"
            }
        )
    
    access_token = JWT_token.create_access_token(data={"id": user.id, "email": user.email})
    
    return LoginResponse(username= str(user.username), email= str(user.email), access_token= access_token, token_type= 'bearer', user_type = 1 if user.userType == Role.Admin else 2)
