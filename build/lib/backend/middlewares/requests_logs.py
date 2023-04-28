# import time
from typing import Callable

from fastapi import Request, Response, Depends
from fastapi.routing import APIRoute
from repository import requests_logs as requestLog
# from models.index import UserRequestsModel
from config.db import SessionLocal

db = SessionLocal()

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # print(request.url.path)
            # before = time.time()

            response: Response = await original_route_handler(request)
            # duration = time.time() - before
            # response.headers["X-Response-Time"] = str(duration)
            # print(f"route duration: {duration}")
            # print(f"route response: {response}")
            # print(f"route response headers: {response.headers}")

            # print(response.status_code)

            if request.headers.get('Authorization') is not None:
                requestLog.create(request_endpoint=request.url.path, request_status= response.status_code, db= db, token = request.headers['Authorization'])

            return response

        return custom_route_handler