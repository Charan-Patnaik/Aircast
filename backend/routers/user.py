from fastapi import APIRouter, status, Depends
from schemas.User import User, LoginResponse
from sqlalchemy.orm import Session
from config import db
from repository.user import create, find_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = db.get_db


@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
def sign_up_user(request: User, db: Session = Depends(get_db)):
    result = create(request = request, db = db)
    return result



@router.post('/login', status_code=status.HTTP_200_OK, response_model= LoginResponse)
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = find_user(request.username, request.password, db = db)    
    return result