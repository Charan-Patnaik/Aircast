from sqlalchemy.orm import Session
from models.Request_Logs import UserRequestsModel
from models.Stations import StationsModel
from models.Zipcode import ZipcodeModel
from utils.JWT_token import verify_token_v2
from typing import List
from sqlalchemy.orm import Session
from config import db
from fastapi import Depends, Request
from schemas.User import TokenData
from utils.JWT_token import verify_token_v2
from models.User import UserModel
from models.Service_Plan import ServicePlanModel
from models.Request_Logs import UserRequestsModel
# from utils.redis import islimiter
from config import db
from datetime import datetime, timedelta, date
from sqlalchemy import and_, or_, Date, cast, distinct, tuple_
from sqlalchemy.sql import func
import pandas as pd
import ast
import json

def create(request_endpoint: str, request_status: int,  db: Session, token:str):
    try:
        tokenData = verify_token_v2(token.split(" ")[1])
        if tokenData is None:
            return None
        
        new_request = UserRequestsModel(user_id= tokenData.id, endpoint = request_endpoint, statusCode = request_status)
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    
    except Exception as e:
        print(e)
        return None
    

def get_user_api_request_data_by_hour_for_specific_date(date_requested: Date, user_id:int, db: Session):
    # record = [z.to_json() for z in db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) >= date_requested, UserRequestsModel.user_id == user_id)).all()]
    # total_api_hits = db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) == date_requested, UserRequestsModel.user_id == user_id)).all()

    result = db.query(func.extract('hour', UserRequestsModel.created_date).label('h'), func.sum(1), UserRequestsModel.statusCode).filter(cast(UserRequestsModel.created_date, Date) == date_requested, UserRequestsModel.user_id == user_id).group_by('h').group_by(UserRequestsModel.statusCode).all()

    # [(22, Decimal('3'), 503), (22, Decimal('2'), 200), (23, Decimal('1'), 201), (16, Decimal('1'), 501), (11, Decimal('1'), 201), (11, Decimal('1'), 200)]
    d = dict()
    l = list()

    for j in range(0,24):
        if [ i for i, v in enumerate(result) if v[0] == j]:
            # print("** ", j," **** ", sum([v[1] for v in result if v[0] == j and (v[2] == 200 or v[2] == 201) ]))
            l.append(
                {
                    "time": j,
                    "success": int(sum([v[1] for v in result if v[0] == j and (v[2] == 200 or v[2] == 201) ])),
                    "failuer": int(sum([v[1] for v in result if v[0] == j and (v[2] != 200 and v[2] != 201) ]))  
                }
            )
        else:
            l.append(
                {
                    "time": j,
                    "success": 0,
                    "failuer": 0 
                }
            )

    # print(result)

    print(l)

    return l

def get_all_users_for_admin(db: Session):
    records =[z.to_json_for_all_user() for z in db.query(UserModel).all()]

    return records
    

def get_user_specific_api_rate_limit(request:Request, db: Session = Depends(db.get_db)):

    try:
        if request.headers.get('Authorization') is not None:
            tokenData = verify_token_v2(request.headers['Authorization'].split(" ")[1])
            print(tokenData)
            if tokenData is None:
                return None
            
            print(tokenData)
        
        user: UserModel = db.query(UserModel).filter(UserModel.id == tokenData.id).join(ServicePlanModel).first()
        return islimiter(user.id, user.plan.requestLimit)
    
    except Exception as e:
        print(e)


def get_user_api_request_in_hr(user_id:int, db: Session):
    one_hour_interval_before = datetime.utcnow() - timedelta(hours=1)

    total_api_hits = db.query(UserRequestsModel).filter(and_(UserRequestsModel.created_date >= one_hour_interval_before, UserRequestsModel.user_id == user_id)).count()
    total_succesfull_api_hits = db.query(UserRequestsModel).filter(
        and_(
            UserRequestsModel.created_date >= one_hour_interval_before, 
            UserRequestsModel.user_id == user_id, 
            or_(
                UserRequestsModel.statusCode == 200, 
                UserRequestsModel.statusCode == 201
                )
            )).count()

    return total_api_hits, total_succesfull_api_hits


def get_user_api_request_in_day(user_id:int, db: Session):
    previous_day = date.today() - timedelta(days= 1)

    total_api_hits = db.query(UserRequestsModel).filter(and_(cast(UserRequestsModel.created_date, Date) == previous_day, UserRequestsModel.user_id == user_id)).count()
    total_succesfull_api_hits = db.query(UserRequestsModel).filter(
        and_(
            cast(UserRequestsModel.created_date, Date) == previous_day,
            UserRequestsModel.user_id == user_id, 
            or_(
                UserRequestsModel.statusCode == 200, 
                UserRequestsModel.statusCode == 201
                )
            )).count()

    return total_api_hits, total_succesfull_api_hits


# def get_all_apis_list_with_count(db: Session, user_id = None):

def get_all_apis_list_with_count_last_week(db: Session, user_id = None):
    previous_week_end = date.today() - timedelta(days=7) #bigger date
    previous_week_start = previous_week_end - timedelta(days=7) #smaller date
    if user_id is None:


        total_api_hits = db.query(UserRequestsModel).filter(and_(UserRequestsModel.created_date <= previous_week_end, UserRequestsModel.created_date >= previous_week_start )).count()
        # .filter(and_(cast(UserRequestsModel.created_date, Date) >= previous_week_end)).count()
        total_succesfull_api_hits = db.query(UserRequestsModel).filter(
            and_(
                cast(UserRequestsModel.created_date, Date) <= previous_week_end,
                UserRequestsModel.created_date >= previous_week_start,
                or_(
                    UserRequestsModel.statusCode == 200, 
                    UserRequestsModel.statusCode == 201
                    )
                )).count()
    else:

        total_api_hits = db.query(UserRequestsModel).filter(and_(UserRequestsModel.created_date <= previous_week_end, UserRequestsModel.created_date >= previous_week_start, UserRequestsModel.user_id == user_id)).count()
        # .filter(and_(cast(UserRequestsModel.created_date, Date) >= previous_week_end)).count()
        total_succesfull_api_hits = db.query(UserRequestsModel).filter(
            and_(
                cast(UserRequestsModel.created_date, Date) <= previous_week_end,
                UserRequestsModel.created_date >= previous_week_start,
                or_(
                    UserRequestsModel.statusCode == 200, 
                    UserRequestsModel.statusCode == 201
                    )
                ), UserRequestsModel.user_id == user_id).count()
    
    average_api_hits = total_api_hits // 7 #integer returned

    return total_api_hits, total_succesfull_api_hits, average_api_hits


def get_zipcode_using_lat_long(zipcode, db: Session):

    print("^^^^^^^^^^")
    print(zipcode, ZipcodeModel.zipcode)
    print("^^^^^^^^^^")

    zip: ZipcodeModel = db.query(ZipcodeModel).filter(ZipcodeModel.zipcode==zipcode).first()

    print("***************")
    print(zip.latitude, zip.longitude)
    print("***************")
    return zip.latitude, zip.longitude


def get_all_nearest_sitenames(zipcode, db: Session):
    l = []
    print("^^^^^^^^^^")
    print(zipcode)
    print("^^^^^^^^^^")
    lat, lng = get_zipcode_using_lat_long(zipcode, db)
    radius = 50

    l = db.query(StationsModel).filter(func.acos(func.cos(func.radians(lat)) * func.cos(func.radians(StationsModel.latitude)) *
        func.cos(func.radians(StationsModel.longitude) - func.radians(lng)) +
        func.sin(func.radians(lat)) *
        func.sin(func.radians(StationsModel.latitude))) * 6371 <= radius
        ).order_by(
            func.acos(
                func.cos(func.radians(lat)) *
                func.cos(func.radians(StationsModel.latitude)) *
                func.cos(func.radians(StationsModel.longitude) - func.radians(lng)) +
                func.sin(func.radians(lat)) *
                func.sin(func.radians(StationsModel.latitude))
            ) * 6371
        ).all()
    
    result = []

    for i in l:

        aqsid = ''

        records = i.to_json_for_retrieving_stations_data()
        print(records)
        records = ast.literal_eval(records['parameter_list'])

        result.append(records)

    print("*****************")
    print(result)
    print("*****************")

    # [['NO2', 'CO', 'PM2.5', 'PM10', 'SO2', 'OZONE'], ['NO2', 'PM2.5', 'SO2'], ['NO2', 'CO', 'PM2.5'], ['PM2.5'], ['PM2.5'], ['NO2', 'OZONE', 'PM2.5'], ['NO2', 'OZONE', 'PM2.5'], ['OZONE', 'PM2.5'], ['NO2', 'OZONE', 'PM2.5'], ['OZONE'], ['OZONE']]

    for rec in result:

        elements = []
        flag_NO2 = False
        flag_CO = False
        flag_PM2_5 = False
        flag_SO2 = False
        flag_PM10 = False
        flag_OZONE = False

        if len(rec) == 6:
            elements.append(rec)
            break
        else:
            for j in records:
                if j == 'NO2':
                    elements.append(j)
                    flag_NO2 = True

                if j == 'CO':
                    elements.append(j)
                    flag_CO = True

                if j == 'PM2.5':
                    elements.append(j)
                    flag_PM2_5 = True

                if j == 'SO2':
                    elements.append(j)
                    flag_SO2 = True

                if j == 'PM10':
                    elements.append(j)
                    flag_PM10 = True

                if j == 'OZONE':
                    elements.append(j)
                    flag_OZONE = True

                if (flag_NO2 == True) and (flag_CO == True) and (flag_PM2_5 == True) and (flag_SO2 == True) and (flag_PM10 == True) and (flag_OZONE == True):
                    break

    # [[ "NO2", "CO", "PM2.5", "PM10", "SO2", "OZONE"]]

    d = {}
    d['value'] = elements[0]

    return d

