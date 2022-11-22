from typing import Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class WorkerCreateSchema(BaseModel):
    user_id: int = Field(gt=0)
    specialization: str = Field(min_length=1, max_length=32)
    description: Optional[str] = Field(min_length=1, max_length=4096)
    


class WorkerAlterSchema(BaseModel):
    specialization: Optional[str] = Field(min_length=1, max_length=32)
    description: Optional[str] = Field(min_length=1, max_length=4096)
  


class WorkerSchema(BaseModel):
    id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=32)
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




