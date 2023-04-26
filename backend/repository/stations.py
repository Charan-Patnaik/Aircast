from sqlalchemy.orm import Session
from models.Stations import StationsModel
from models.StationsData import StationsDataModel
from models.StationsDataDaily import StationsDataDailyModel
from sqlalchemy.sql import func
import ast
import json
from models.Stations import StationsModel
from models.Zipcode import ZipcodeModel

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
    

def get_zipcode_using_lat_long(zipcode, db: Session):

    zip: ZipcodeModel = db.query(ZipcodeModel).filter(ZipcodeModel.zipcode==zipcode).first()

    return zip.latitude, zip.longitude


def get_all_nearest_sitenames(zipcode, db: Session):
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

    for key, value in result.items():
        final_result.append({
            "station": key,
            "pollutant": value
        })

    return {
        "success": True,
        "stations": final_result
        }

