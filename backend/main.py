from fastapi import FastAPI
import uvicorn
from routers import user
from config.db import Base, engine, SessionLocal

app =  FastAPI()
db = SessionLocal()


# create tables if not exist
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized the db")

@app.on_event("startup")
async def startup():

    # register user router
    app.include_router(user.router)

    init_db()
    

# define a default route
@app.get('/')
def index():
    return 'Success! APIs are working!'


if __name__ == '__main__':
    # start the server
    uvicorn.run(app, host='127.0.0.1', port=8000)
