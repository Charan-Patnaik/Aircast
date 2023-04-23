from fastapi import FastAPI
import uvicorn
from routers import user, service_plans
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



# create tables if not exist
def init_db():
    Base.metadata.create_all(bind=engine)
    servicePlans.create(1, 'Free', 10, db= db)
    servicePlans.create(2, 'Gold', 15, db= db)
    servicePlans.create(3, 'Platinum', 20, db= db)
    UserRepository.create(User(username='damg7245', email=EmailStr('rishab1300@gmail.com'), password='spring2023', planId=2, userType= Role.User), db= db)
    UserRepository.create(User(username='admin', email=EmailStr('mail@heyitsrj.com'), password='spring2023', planId=1, userType = Role.Admin), db= db)

    df = pd.read_csv('station_with_params.csv')
    print(df.shape)

    for index, row in df.iterrows():
        print(row)

        stations.create(
            aquid=row['AQSID'],
            sitename=row['SiteName'],
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            county=row['CountyName'],
            parameter=row['parameter name'],
            db= db
        )

    df = pd.read_csv('zip_with_lat.csv', dtype={'ZIP': str})
    # print(df)
    for index, row in df.iterrows():
        # print(row)

        zipcode.create(
            zipcode=str(row['ZIP']),
            latitude=row['LAT'],
            longitude=row['LNG'],
            db= db
        )

    print("Initialized the db")

@app.on_event("startup")
async def startup():

    # register user router
    app.include_router(user.router)
    app.include_router(service_plans.router)


    init_db()
    

# define a default route
@app.get('/')
def index():
    return 'Success! APIs are working!'


if __name__ == '__main__':
    # start the server
    uvicorn.run(app, host='127.0.0.1', port=8000)
