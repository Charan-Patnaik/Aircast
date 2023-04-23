from sqlalchemy import Integer, Column, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Numeric
from config.db import Base
import enum

class ZipcodeModel(Base):
    __tablename__ = 'Zipcode'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    zipcode = Column(String(255), unique=True)
    latitude = Column(Numeric(8, 6))
    longitude = Column(Numeric(9, 6))

    # def to_json_for_all_user(self):
    #     return {
    #         "id": str(self.id),
    #         "username": str(self.username)
    #     }