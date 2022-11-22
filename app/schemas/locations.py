
from pydantic import BaseModel, validator, Field, PositiveInt
from typing import Optional


class LocationCreateSchema(BaseModel):
    placename: str = Field(min_length=1, max_length=32)
    latitude: int 
    longitude: int 

    
    
    class Config:
        orm_mode = True


class LocationSchema(BaseModel):
    id: int = Field(gt=0)
    placename: str = Field(min_length=1, max_length=32)
    latitude: int 
    longitude: int 
   

    class Config:
        orm_mode = True


class LocationAlterSchema(BaseModel):
    placename: str = Field(min_length=1, max_length=32)
    latitude: int
    longitude: int 


    class Config:
        orm_mode = True
