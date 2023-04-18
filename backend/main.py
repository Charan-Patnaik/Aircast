from fastapi import FastAPI
import uvicorn
from routers import user
from config.db import Base, engine, SessionLocal

app =  FastAPI()
db = SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized the db")

@app.on_event("startup")
async def startup():
    app.include_router(user.router)

    init_db()
    

@app.get('/')
def index():
    return 'Success! APIs are working!'


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
