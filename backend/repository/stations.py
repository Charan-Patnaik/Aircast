from sqlalchemy.orm import Session
from models.Stations import StationsModel
from models.StationsData import StationsDataModel
import pandas as pd

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