    
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from app.db import Base


class Procedure(Base):
    __tablename__ = 'procedures'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    duration =  Column(Integer)
    specialization =Column(String)
    description =Column(String)
    worker = relationship('Worker', back_populates='procedure', cascade='all, delete')
    
    
    
    
    
    
    
    
    # id: int = Field(gt=0)
    # name: str = Field(min_length=1, max_length=32)
    # specialization: str 
    # description: Optional[str] = Field(min_length=1, max_length=4096)
   