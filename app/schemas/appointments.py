
from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import date, time


class AppointmentCreateSchema(BaseModel):
    user_id: int = Field(gt=0)
    worker_id: int = Field(gt=0)
    date: date
    start_time: time
    end_time: time
    procedure_id: int
    
    class Config:
        orm_mode = True


class AppointmentSchema(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    worker_id: int = Field(gt=0)
    date: date
    start_time: time
    end_time: time
    procedure_id: int
   

    class Config:
        orm_mode = True


class AppointmentAlterSchema(BaseModel):
    worker_id: Optional[int] = Field(gt=0)
    date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    procedure_id: Optional[int]


    class Config:
        orm_mode = True