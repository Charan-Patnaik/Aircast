from sqlalchemy import Integer, Column, ForeignKey, Enum, ARRAY, Float
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Numeric
from config.db import Base
import datetime

class ZipDataDailyCacheModel(Base):
    __tablename__ = 'ZipDataDailyCache'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    zipcode = Column(String(255), unique=False)
    ozone = Column(Float(20), nullable= True, default=None)
    so2 = Column(Float(20), nullable= True, default=None)
    no2 = Column(Float(20), nullable= True, default=None)
    co = Column(Float(20), nullable= True, default=None)
    pm2_5 = Column(Float(20), nullable= True, default=None)
    pm10 = Column(Float(20), nullable= True, default=None)



    # def to_json_for_all_user(self):
    #     return {
    #         "id": str(self.id),
    #         "username": str(self.username)
    #     }