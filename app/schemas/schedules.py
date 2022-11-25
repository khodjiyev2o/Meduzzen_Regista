
from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date, time


class ScheduleCreateSchema(BaseModel):
    worker_id: int = Field(gt=0)
    date: date
    start_time: time
    end_time: time


    
    class Config:
        orm_mode = True


class ScheduleSchema(BaseModel):
    id: int = Field(gt=0)
    worker_id: int = Field(gt=0)
    date: date
    start_time: time
    end_time: time
   

    class Config:
        orm_mode = True


class ScheduleAlterSchema(BaseModel):
    date: Union[date, None] 
    start_time: Union[time, None] 
    end_time: Union[time, None] 


    class Config:
        orm_mode = True