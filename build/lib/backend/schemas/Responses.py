from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import status

class Responses():
    
    # Define a class to handle HTTP response objects
    success: bool
    message: str

    def __init__(self) -> None:
        # Constructor to set default values for success and message
        self.success = False
        self.message = ""


    def conflict(self, message: str) -> JSONResponse:
        # Method to return a JSONResponse object with HTTP status code 409 Conflict

        return JSONResponse(
                status_code= status.HTTP_409_CONFLICT,
                content= {
                    "success": self.success,
                    "message": message
                }
        )
    

    def bad_request(self, message: str) -> JSONResponse:
        # Method to return a JSONResponse object with HTTP status code 400 Bad Request

        return JSONResponse(
                status_code= status.HTTP_400_BAD_REQUEST,
                content= {
                    "success": self.success,
                    "message": message
                }
        )
    
    def internal_server(self, message: str) -> JSONResponse:
        # Method to return a JSONResponse object with HTTP status code 500 Internal Server Error

        return JSONResponse(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                content= {
                    "success": self.success,
                    "message": message
                }
        )
    
    def not_found(self, message: str) -> JSONResponse:
        # Method to return a JSONResponse object with HTTP status code 404 Not Found

        return JSONResponse(
                status_code= status.HTTP_404_NOT_FOUND,
                content= {
                    "success": self.success,
                    "message": message
                }
        )
    

response = Responses()