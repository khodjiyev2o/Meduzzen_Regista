    
from sqlalchemy import Column, String, Integer, Date, Boolean, Time, ForeignKey
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from app.db import Base


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    worker = relationship('Worker', back_populates='schedule')
    worker_id = Column(Integer, ForeignKey('workers.id'), index=True)
    






   