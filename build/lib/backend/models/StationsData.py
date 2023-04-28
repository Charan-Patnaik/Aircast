from sqlalchemy import Integer, Column, ForeignKey, Enum, ARRAY, Float
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Numeric
from config.db import Base
import datetime

class StationsDataModel(Base):
    __tablename__ = 'StationsData'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    aquid = Column(String(255), unique=False)
    collection_timestamp = Column(DateTime, default= datetime.datetime.now)
    ozone = Column(String(10), nullable= True, default=None)
    so2 = Column(String(10), nullable= True, default=None)
    no2 = Column(String(10), nullable= True, default=None)
    co = Column(String(10), nullable= True, default=None)
    pm2_5 = Column(String(10), nullable= True, default=None)
    pm10 = Column(String(10), nullable= True, default=None)



    # def to_json_for_all_user(self):
    #     return {
    #         "id": str(self.id),
    #         "username": str(self.username)
    #     }

    # def to_json_for_retrieving_stations_data(self):
    #     return {
    #         'id' : str(self.id),
    #         'aquid' : str(self.aquid),
    #         'collection_timestamp' : str(self.collection_timestamp),
    #         'ozone' : str(self.ozone),
    #         'so2' : str(self.so2),
    #         'no2' : str(self.no2),
    #         'co' : str(self.co),
    #         'pm2_5' : str(self.pm2_5),
    #         'pm10' : str(self.pm10)
    #     }