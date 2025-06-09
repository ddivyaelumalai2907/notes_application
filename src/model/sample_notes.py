from sqlalchemy import Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from base import Base

class Sample_notes(Base):
    __tablename__ = 'sample_notes'
    __table_args__ = {'schema': 'notesapplication'}
    
    id = Column('id',Integer, primary_key=True,nullable=False)
    title = Column('title',String(200), nullable=False)
    content = Column('content',String(255), nullable=False)