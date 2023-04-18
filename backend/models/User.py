from sqlalchemy import Integer, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from config.db import Base
from sqlalchemy.orm import relationship
import datetime

class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    createdAt = Column(DateTime, default= datetime.datetime.utcnow)


    # def to_json_for_all_user(self):
    #     return {
    #         "id": str(self.id),
    #         "username": str(self.username)
    #     }