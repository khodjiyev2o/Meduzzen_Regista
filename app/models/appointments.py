
from sqlalchemy import Column, String, Integer, Date, Boolean, Time, ForeignKey
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from app.db import Base


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='appointment')

    worker_id = Column(Integer, ForeignKey('workers.id'), index=True)
    worker = relationship('Worker', back_populates='appointment')

    procedure_id = Column(Integer, ForeignKey('procedures.id'), index=True)
    procedure = relationship('Procedure', back_populates='appointment')



#    id: int = Field(gt=0)
#     user_id: int = Field(gt=0)
#     worker_id: int = Field(gt=0)
#     date: date
#     start_time: time
#     end_time: time
#     procedure_id: int
   