from sqlalchemy.orm import Session
from models.Stations import StationsModel
from models.StationsData import StationsDataModel
from models.StationsDataDaily import StationsDataDailyModel
from sqlalchemy.sql import func
import ast
import json
from models.Stations import StationsModel
from models.Zipcode import ZipcodeModel
from models.ZipDataDailyCache import ZipDataDailyCacheModel
from fastapi.responses import JSONResponse
from fastapi import status

import requests
import os

from models.ZipDataDailyCache import ZipDataDailyCacheModel

from dotenv import load_dotenv

from sqlalchemy import and_

import csv

from aws_cloud.s3_upload import file_upload


load_dotenv()

BASE_URL_FOR_MAAS = os.environ.get('BASE_URL_PREDICITON')


def create(stations, db: Session):
    try:
        rows = []
        for index, row in stations.iterrows():
            
            rows.append(StationsModel(
                aquid=row['AQSID'],
                sitename=row['SiteName'],
                latitude=row['Latitude'],
                longitude=row['Longitude'],
                countyName=row['CountyName'],
                parameter_list=row['parameter name']
            ))
            
        db.bulk_save_objects(rows)
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(e)
        return None
    

def get_specified_site_data_link(stations:str, start_date, end_date, db: Session):

    data_zip = db.query(StationsDataModel).filter(
        StationsDataModel.aquid == stations,
        and_(StationsDataModel.collection_timestamp >= start_date, StationsDataModel.collection_timestamp <= end_date)
    ).all()

        # Convert data_zip to a list of dictionaries
    data_list = [record.__dict__ for record in data_zip]

    # Remove unnecessary keys from each dictionary
    for record in data_list:
        record.pop('_sa_instance_state', None)

    # Write data_list to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
        except Exception as e:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content= {
                    "success": False,
                    "message": f"Data for Station ID {stations} not found in the date range"
                }
            )

    
    url_file = file_upload('data.csv')

    return {
            "success": True,
            "file_url": url_file
        }




def get_zipcode_using_lat_long(zipcode, db: Session):

    zip: ZipcodeModel = db.query(ZipcodeModel).filter(ZipcodeModel.zipcode==zipcode).first()

    return zip.latitude, zip.longitude


def get_all_nearest_sitenames(zipcode, db: Session):
    data_zip = db.query(ZipDataDailyCacheModel).filter(ZipDataDailyCacheModel.zipcode == zipcode).all()

    if len(data_zip) > 0:
        print("data from db directly", data_zip)

        new_list = []
        for dat in data_zip:

            new_list.append({
                "SO2": dat.so2,
                "OZONE": dat.ozone,
                "CO": dat.co,
                "NO2": dat.no2,
                "PM2.5": dat.pm2_5,
                "PM10": dat.pm10
            })
        
        return {
            "success": True,
            "stations": new_list
        }


    l = []
    
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
    
    result_parameter_list = []
    result_aqsid_list = []

    for i in l:

        records = i.to_json_for_retrieving_stations_data()

        result_parameter = ast.literal_eval(records['parameter_list'])
        result_aqsid = ast.literal_eval(records['aquid'])

        result_parameter_list.append(result_parameter)
        result_aqsid_list.append(result_aqsid)

    print("********* list ********")
    print(result_aqsid_list)
    print(result_parameter_list)
    print("********* list ********")

    pollutants = []
    aqsid_output = []

    flag_NO2 = False
    flag_CO = False
    flag_PM2_5 = False
    flag_SO2 = False
    flag_PM10 = False
    flag_OZONE = False
        
    print("%%%%%%%%%%%% RESULT %%%%%%%%%%")

    for j in range(len(result_parameter_list)): 

        for k in result_parameter_list[j]:

            k = str(k)
            result_parameter_list[j] = str(result_parameter_list[j])
            dict = {}

            if k == 'NO2' and flag_NO2 == False :
                dict[result_aqsid_list[j]] = k
                flag_NO2 = True

            if k == 'CO' and flag_CO == False :
                dict[result_aqsid_list[j]] = k
                flag_CO = True

            if k == 'PM2.5' and flag_PM2_5 == False :
                dict[result_aqsid_list[j]] = k
                flag_PM2_5 = True

            if k == 'SO2' and flag_SO2 == False :
                dict[result_aqsid_list[j]] = k
                flag_SO2 = True

            if k == 'PM10' and flag_PM10 == False :
                dict[result_aqsid_list[j]] = k
                flag_PM10 = True

            if k == 'OZONE' and flag_OZONE == False :
                dict[result_aqsid_list[j]] = k
                flag_OZONE = True

            if dict != {}:
                aqsid_output.append(dict)

            if (flag_NO2 == True) and (flag_CO == True) and (flag_PM2_5 == True) and (flag_SO2 == True) and (flag_PM10 == True) and (flag_OZONE == True):
                break

        if (flag_NO2 == True) and (flag_CO == True) and (flag_PM2_5 == True) and (flag_SO2 == True) and (flag_PM10 == True) and (flag_OZONE == True):
            break

    # [[ "NO2", "CO", "PM2.5", "PM10", "SO2", "OZONE"]]

    print("$$$$$$$ final $$$$$$$")
    print(aqsid_output)
    print("$$$$$$$ final $$$$$$$")


    result = {}
    for d in aqsid_output:
        aqsid, pollutant = list(d.items())[0]
        if aqsid in result:
            result[aqsid].append(pollutant)
        else:
            result[aqsid] = [pollutant]

    final_result = []


    # new_list = []

    combined_list= []

    list_of_list = []
    for stations_name, station_parameters in result.items():
        new_list = []
        print("**** api_hit_stations: ", stations_name, " Params: ", station_parameters)

        response = requests.post( f"{BASE_URL_FOR_MAAS}/get-prediction-for-station-id/{stations_name}", headers={"accept": "application/json"})
        if(response.status_code == 200):
            predictions_list = response.json()['predictions']

            # print("*** Predictions: \n", predictions_list)
            # new_list = []
            # for i in station_parameters:
            for item in predictions_list:
                new_item = {}

                    # ozone = item['OZONE']
                    # so2 = item['SO2']
                    # no2 = item['NO2']
                    # pm25 = item['PM2.5']
                    # new_item = {i: item[f'{i}']}
                # new_item['timestamp'] = item[f'index']
                for i in station_parameters:
                    new_item[i] = item[f'{i}']
        
                new_list.append(new_item)
        
        print(new_list)
        list_of_list.append(new_list)

    # print(list_of_list)

    # combined_list = []
    # combined_dict = {}
    # for sub_list in list_of_list:
        
    #     combined_dict = {}

    #     for d in sub_list:
    #         combined_dict.update(d)
    #     combined_list.append(combined_dict)


    
    combined_list = []
    for dicts in zip(*list_of_list):
        combined_dict = {}
        for d in dicts:
            combined_dict.update(d)
        combined_list.append(combined_dict)
    
    # combined_list = [dict1.update(dict2) or dict1 for dict1, dict2 in zip(*list_of_list)]

    rows = []

    for i in combined_list:
        rows.append(ZipDataDailyCacheModel(
            zipcode=str(zipcode),
            so2=i['SO2'],
            ozone=i['OZONE'],
            co=i['CO'],
            no2 = i['NO2'],
            pm2_5 = i['PM2.5'],
            pm10 = i['PM10'],
        ))

    db.bulk_save_objects(rows)
    db.commit()
    db.close()

    return {
        "success": True,
        "stations": combined_list
        }




