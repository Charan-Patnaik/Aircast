from pydantic import BaseModel, validator

class Plan(BaseModel):
    id:int
    planName:str
    requestLimit:int
    timeFrame:int

    class Config:
        orm_mode = True