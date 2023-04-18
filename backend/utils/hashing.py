from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
This module is used for password hashing and verification.
"""

class Hash():

    def get_hashed_password(self, password: str) -> str:
        """
        Hashes the password using bcrypt algorithm.

        Parameters:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """

        return pwd_context.hash(password)
    
    def verify_password(self, hashed_password, password):
        """
        Verifies the given password with the hashed password.

        Parameters:
            hashed_password (str): The hashed password to compare.
            password (str): The password to verify.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        
        return pwd_context.verify(password, hashed_password)