from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from sqlalchemy.orm import Session
from repository.stations import get_all_nearest_sitenames, get_specified_site_data_link
# from repository.user import find_user_api_key
from datetime import datetime
from schemas.User import TokenData
from middlewares.oauth2 import get_current_user
from middlewares.requests_logs import TimedRoute
from repository.requests_logs import get_user_specific_api_rate_limit
from fastapi.responses import JSONResponse
import datetime

router = APIRouter(
    prefix='/aircast',
    tags=['Aircast'],
    route_class= TimedRoute
)

get_db = db.get_db

@router.get('/prediction-for-zipcode')
def get_user_sitenames_nearest(zipcode: str, get_current_user: TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit), db: Session = Depends(db.get_db)):
    # sql extract data
    if is_limit is True:
        station_list = get_all_nearest_sitenames(zipcode, db=db)
        return station_list
    
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )
    

@router.get('/get-data-by-site')
def get_data_for_site(station_name: str, start_date:str, end_date:str, get_current_user: TokenData = Depends(get_current_user), is_limit: bool = Depends(get_user_specific_api_rate_limit), db: Session = Depends(db.get_db)):
    if is_limit is True:
        # Convert start_date and end_date to datetime objects
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Check that start_datetime is earlier than end_datetime
        if start_datetime > end_datetime:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'success': False, 
                    "message": "Start date must be earlier than end date"
                }
            )


        station_list = get_specified_site_data_link(stations= station_name, start_date= start_date, end_date= end_date, db=db)
        return station_list
    
    else:
        return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    'success': False, 
                    "message": "API limit excceded!"
                }
            )