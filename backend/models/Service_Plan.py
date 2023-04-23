from sqlalchemy import Integer, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import Base
from sqlalchemy.orm import relationship

class ServicePlanModel(Base):
    __tablename__ = 'ServicePlans'

    id = Column(Integer, primary_key=True, autoincrement=False)
    planName = Column(String(255), unique=True)
    requestLimit = Column(Integer, default= 10)
    timeFrame = Column(Integer, default= 60) # Specified time frame as 60 minutes (i.e. 1 hr)

    user = relationship("UserModel", back_populates="plan")
