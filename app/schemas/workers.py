from typing import Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class WorkerCreateSchema(BaseModel):
    user_id: int = Field(gt=0)
    specialization: str = Field(min_length=1, max_length=32)
    location_id: int = Field(gt=0)
    procedure_id: list[int] = Field(gt=0)
    description: Optional[str] = Field(min_length=1, max_length=4096)
    


class WorkerAlterSchema(BaseModel):
    description: Optional[str] = Field(min_length=1, max_length=4096)
    procedure_id: list[int] = Field(gt=0)
    location_id: int = Field(gt=0)


class WorkerSchema(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    location_id: int = Field(gt=0)
    procedure_id: list[int] = Field(gt=0)
    specialization: str = Field(min_length=1, max_length=32)
    description: Optional[str] = Field(min_length=1, max_length=4096)



# class AppointmentSchema(BaseModel):
#     company: str = Field(min_length=1, max_length=32)
#     user: str = Field(min_length=1, max_length=32)
#     admin: Optional[bool]


# class RequestSchema(BaseModel):
#     id: int = Field(gt=0)
#     user: str = Field(min_length=1, max_length=32)
#     company: str = Field(min_length=1, max_length=32)
#     side: Literal['User requests appointment to worker']




