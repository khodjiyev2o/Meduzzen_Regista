from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from app.db import Base


class Worker(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True, index=True)
    specialization = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='worker')

    location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    location = relationship('Location', back_populates='worker')

    
    procedure = relationship('Procedure', back_populates='worker', cascade='all, delete')

    schedule = relationship('Schedule', back_populates='worker', cascade='all, delete')

    appointment = relationship("Appointment", back_populates="worker", cascade='all, delete')
