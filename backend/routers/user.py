from fastapi import APIRouter, status, Depends
from schemas.User import User, LoginResponse
from sqlalchemy.orm import Session
from config import db
from repository.user import create, find_user
from fastapi.security import OAuth2PasswordRequestForm
from schemas.Responses import response

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = db.get_db


@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
def sign_up_user(request: User, db: Session = Depends(get_db)):
    """
    Endpoint for creating a new user account.
    
    Args:
        request (User): A `User` object representing the new user account to create.
        db (Session): The SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the newly created user account.
    """
    if request.planId not in [1, 2, 3]:
        return response.bad_request(f"Please sepcify plan id")
    

    result = create(request = request, db = db)
    return result



@router.post('/login', status_code=status.HTTP_200_OK, response_model= LoginResponse)
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint for logging in to an existing user account.
    
    Args:
        request (OAuth2PasswordRequestForm): An `OAuth2PasswordRequestForm` object representing the user's login credentials.
        db (Session): The SQLAlchemy database session.

    Returns:
        LoginResponse: A `LoginResponse` object containing the JWT token for the authenticated user.
    """
    
    result = find_user(request.username, request.password, db = db)    
    return result