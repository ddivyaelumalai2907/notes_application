from sqlalchemy import Column,String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from base import Base

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'notesapplication'}
    
    user_id = Column('user_id',String(36), primary_key=True,nullable=False)
    user_name = Column('user_name',String(255), nullable=False)
    user_email = Column('user_email',String(45), nullable=False)
    password = Column('password',String(45), nullable=False)
    last_update = Column('last_update',DateTime, nullable=False,server_default=func.now(), onupdate=func.now())
    create_on = Column('create_on',DateTime, nullable=False,server_default=func.now(), onupdate=func.now())
    # Relationship
    notes = relationship("Notes", back_populates="user", cascade="all, delete")

    def __init__(self, user_name, user_email,password):
        self.user_id = str(uuid.uuid4())
        self.user_name = user_name
        self.user_email = user_email
        self.password = password
