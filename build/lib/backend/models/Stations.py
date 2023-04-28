from sqlalchemy import Integer, Column, ForeignKey, Enum, ARRAY
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Numeric
from config.db import Base
import enum

class StationsModel(Base):
    __tablename__ = 'Stations'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    aquid = Column(String(255), unique=True)
    sitename = Column(String(255), unique=False, nullable=True)
    latitude = Column(Numeric(8, 6))
    longitude = Column(Numeric(9, 6))
    countyName = Column(String(255), unique=False, nullable= True)
    parameter_list = Column(String(255))


    # def to_json_for_all_user(self):
    #     return {
    #         "id": str(self.id),
    #         "username": str(self.username)
    #     }

    def to_json_for_retrieving_stations_data(self):
        return {
            'aquid': str(self.aquid),
            'sitename' : str(self.sitename),
            'latitude' : str(self.latitude),
            'longitude' : str(self.longitude),
            'countyName' : str(self.countyName),
            'parameter_list' : str(self.parameter_list)
        }