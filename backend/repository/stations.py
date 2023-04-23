from sqlalchemy.orm import Session
from models.Stations import StationsModel

def create(aquid:str, sitename:str, latitude, longitude, county, parameter, db: Session):
    try:        
        new_request = StationsModel(
            aquid = aquid,
            sitename = sitename,
            latitude = latitude,
            longitude = longitude,
            countyName = county,
            parameter_list = parameter
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except Exception as e:
        print(e)
        return None