
from pydantic import BaseModel, Field
from typing import Optional


class ProcedureCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    worker_id: int = Field(gt=0)
    duration: int = Field(gt=0)
    description: Optional[str] = Field(min_length=1, max_length=4096)

    
    
    class Config:
        orm_mode = True


class ProcedureSchema(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=32)
    worker_id: int = Field(gt=0)
    duration: int = Field(gt=0)
    description: Optional[str] = Field(min_length=1, max_length=4096)
   

    class Config:
        orm_mode = True


class ProcedureAlterSchema(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    worker_id: int = Field(gt=0)
    duration: int = Field(gt=0)
    description: Optional[str] = Field(min_length=1, max_length=4096)


    class Config:
        orm_mode = True