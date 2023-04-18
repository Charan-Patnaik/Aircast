from sqlalchemy.orm import Session
from models.User import UserModel
from schemas.User import LoginResponse, User
from utils import hashing, JWT_token
from fastapi import status
from fastapi.responses import JSONResponse
from schemas.Responses import response
from sqlalchemy import or_


def create(request: User, db: Session):
    try:
        user = db.query(UserModel).filter(or_(UserModel.email == request.email, UserModel.username == request.username)).first()

        if user:
            return response.conflict(f"User with the email '{request.email}' or username '{request.username}' already exists!")


        new_user = UserModel(username=request.username, email=request.email, password= hashing.Hash().get_hashed_password(request.password))
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
    
    return LoginResponse(username= str(user.username), email= str(user.email), access_token= access_token, token_type= 'bearer')
