from sqlalchemy.orm import Session
from models.Zipcode import ZipcodeModel

def create(zipcode, latitude, longitude, db: Session):
    try:        
        new_request = ZipcodeModel(
            zipcode = zipcode,
            latitude = latitude,
            longitude = longitude,
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except Exception as e:
        print(e)
        return None