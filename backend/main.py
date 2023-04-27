from fastapi import FastAPI
from fastapi.testclient import TestClient
import uvicorn
from routers import user, service_plans, admin
from config.db import Base, engine, SessionLocal
import repository.user as UserRepository
import repository.service_plans as servicePlans
from schemas.User import User
from models.User import Role
from pydantic import BaseModel, Field, EmailStr, validator
from repository import stations, zipcode
import pandas as pd

app =  FastAPI()
db = SessionLocal()
client = TestClient(app)


# create tables if not exist
def init_db():
    Base.metadata.create_all(bind=engine)
    servicePlans.create(1, 'Free', 10, db= db)
    servicePlans.create(2, 'Gold', 15, db= db)
    servicePlans.create(3, 'Platinum', 20, db= db)
    UserRepository.create(User(username='damg7245', email=EmailStr('rishab1300@gmail.com'), password='spring2023', planId=2, userType= Role.User), db= db)
    UserRepository.create(User(username='admin', email=EmailStr('mail@heyitsrj.com'), password='spring2023', planId=1, userType = Role.Admin), db= db)


    df = pd.read_csv('zip_code_with_state_coordinates.csv', dtype={'ZIP': str})
    zipcode.create(df, db= db)


    df = pd.read_csv('station_with_params.csv')
    stations.create(df, db= db)

    print("Initialized the db")

@app.on_event("startup")
async def startup():

    # register user router
    app.include_router(user.router)
    app.include_router(service_plans.router)
    app.include_router(admin.router)


    init_db()
    

# define a default route
@app.get('/')
async def index():
    return 'Success! APIs are working!'

import pytest
import json

def test_all_users():
    response = client.get("/admin/all-users")

    print(response.status_code)

    assert response.status_code == 200
    json_string = '{"success": true,"users": [{ "id": "1", "username": "damg7245"}, { "id": "2", "username": "admin" }, {"id": "3", "username": "vsh123" }]}'
    json_object = json.loads(json_string)
    assert response.json() == json_object


if __name__ == '__main__':
    # start the server
    uvicorn.run(app, host='127.0.0.1', port=8000)


# def get_uvicorn_app():
#     return app

# def get_test_client_app():
#     return client

