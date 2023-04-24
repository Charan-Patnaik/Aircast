from sqlalchemy.orm import Session
from models.Zipcode import ZipcodeModel
import pandas as pd

def create(zipcodes, db: Session):
    try:
        rows = []
        for index, row in zipcodes.iterrows():
        # print(row)
            rows.append(ZipcodeModel(
                zipcode=str(row['ZIP']),
                latitude=row['LAT'],
                longitude=row['LNG'],
            ))

        db.bulk_save_objects(rows)
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(e)
        return None