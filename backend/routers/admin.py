from fastapi import APIRouter, status, HTTPException, Response, Depends
from config import db
from sqlalchemy.orm import Session
from repository.requests_logs import get_user_api_request_data_by_hour_for_specific_date, get_all_users_for_admin, get_all_nearest_sitenames
#, get_all_apis_list_with_count, get_all_apis_list_with_count_last_week, get_user_api_request_in_day_admin, get_each_api_request_admin_all, get_admin_success_failure_comparison
# from repository.user import find_user_api_key
from fastapi.responses import JSONResponse
from datetime import datetime
from schemas.User import TokenData
from middlewares.oauth2 import get_current_user
from repository.stations import StationsModel

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

get_db = db.get_db

@router.get('/all-users')
def get_all_users(db: Session = Depends(db.get_db)):

    users = get_all_users_for_admin(db = db)

    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "users": users,
                }
            )

@router.get('/api-hits-count/user/{user_id}')
def get_user_api_hits_for_particular_days_for_user(user_id, date_request: str, get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

    requested_date = datetime.strptime(date_request, "%m/%d/%Y").date()

    if get_current_user.userType == 1:
        total_api_hits = get_user_api_request_data_by_hour_for_specific_date(requested_date, user_id, db= db)
    else:
        total_api_hits = get_user_api_request_data_by_hour_for_specific_date(requested_date, get_current_user.id, db= db)
    return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'success': True, 
                    "api_req": total_api_hits,
                }
            )


@router.get('/api-sitenames-nearest')
def get_user_sitenames_nearest(zipcode: str, db: Session = Depends(db.get_db)):
    # sql extract data
    station_list = get_all_nearest_sitenames(zipcode, db=db)
    
    return station_list




# @router.get('/all-apis-hits-with-count')
# def get_all_apis_list(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

#     if get_current_user.userType == 1:
#         return get_all_apis_list_with_count(db = db)
#     else:
#         return get_all_apis_list_with_count(db = db, user_id= get_current_user.id)


# @router.get('/api-hits-previous-days')
# def get_user_api_hits_count_for_previus_days(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):
#     if get_current_user.userType == 1:
#         total_api_hits, total_successful_api = get_user_api_request_in_day_admin(db = db)
#     else:
#         total_api_hits, total_successful_api = get_user_api_request_in_day_admin(db = db, user_id= get_current_user.id)

#     failed_api_hits = total_api_hits - total_successful_api

#     return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content={
#                     'success': True, 
#                     "total_api_hits_in_previous_day": total_api_hits,
#                     "total_successful_api_hits_in_previous_day": total_successful_api,
#                     "total_failed_api_hits_in_previous_day": failed_api_hits
#                 }
#             )

# @router.get('/all-apis-hits-with-count-last-week')
# def get_all_apis_list(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):
#     if get_current_user.userType == 1:
#         total_api_hits, total_successful_api, average_api_hits = get_all_apis_list_with_count_last_week(db = db)
#     else:
#         total_api_hits, total_successful_api, average_api_hits = get_all_apis_list_with_count_last_week(db = db, user_id= get_current_user.id)

#     failed_api_hits = total_api_hits - total_successful_api

#     return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content={
#                     'success': True, 
#                     "total_api_hits_in_previous_week": total_api_hits,
#                     "total_successful_api_hits_in_previous_week": total_successful_api,
#                     "total_failed_api_hits_in_previous_week": failed_api_hits,
#                     'average_total_hits_in_previous_week': average_api_hits
#                 }
#             )

# @router.get('/all-apis-hits-with-count-compare-success-failure')
# def get_all_apis_list_success_failure(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

#     if get_current_user.userType == 1:
#         total_api_hits, total_succesfull_api_hits = get_admin_success_failure_comparison(db, user_id=None)
#     else:
#         total_api_hits, total_succesfull_api_hits = get_admin_success_failure_comparison(db, user_id= get_current_user.id)
    
#     return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content={
#                     'success': True, 
#                     "total_api_hits": total_api_hits,
#                     "success_count": total_succesfull_api_hits, 
#                     "failure_count": total_api_hits - total_succesfull_api_hits,
#                 }
#             )


# @router.get('/get_each_api_request_admin_all')
# def get_each_api_request_admin_all_time(get_current_user: TokenData = Depends(get_current_user), db: Session = Depends(db.get_db)):

#     if get_current_user.userType == 1:
#         total_api_hits = get_each_api_request_admin_all(db = db, user_id= None)
#     else:
#         total_api_hits = get_each_api_request_admin_all(db = db, user_id= get_current_user.id)

#     return JSONResponse(
#                 status_code=status.HTTP_200_OK,
#                 content={
#                     'success': True, 
#                     "total_api_hits_all_time": total_api_hits
#                 }
#             )