from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from app.db import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    placename = Column(String, unique=True, index=True)
    latitude = Column(Integer)
    longitude = Column(Integer)
    worker = relationship('Worker', back_populates='location', cascade='all, delete')