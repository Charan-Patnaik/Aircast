from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from sqlalchemy.orm import Session
from repository.stations import get_all_nearest_sitenames
# from repository.user import find_user_api_key
from datetime import datetime
from schemas.User import TokenData
from middlewares.oauth2 import get_current_user
from repository.stations import StationsModel
from middlewares.requests_logs import TimedRoute

router = APIRouter(
    prefix='/aircast',
    tags=['Aircast'],
    route_class= TimedRoute
)

get_db = db.get_db

@router.get('/api-sitenames-nearest')
def get_user_sitenames_nearest(zipcode: str, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):
    # sql extract data
    station_list = get_all_nearest_sitenames(zipcode, db=db)
    return station_list