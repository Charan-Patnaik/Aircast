from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():

    def get_hashed_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, hashed_password, password):
        return pwd_context.verify(password, hashed_password)