from sqlalchemy import Column,String, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from base import Base

class Notes(Base):
    __tablename__ = 'notes'
    __table_args__ = {'schema': 'notesapplication'}

    note_id = Column('note_id',String(36), primary_key=True,nullable=False)
    note_title = Column('note_title',String(200), nullable=False)
    note_content = Column('note_content',String(255), nullable=True)
    last_update = Column('last_update',DateTime, nullable=False,server_default=func.now(), onupdate=func.now())
    create_on = Column('create_on',DateTime, nullable=False,server_default=func.now(), onupdate=func.now())
    user_id = Column(String(36), ForeignKey('notesapplication.user.user_id'))
    # Relationship
    user = relationship("User", back_populates="notes")

    def __init__(self, note_title, note_content,user_id =None):
        self.note_id = str(uuid.uuid4())
        self.note_title = note_title
        self.note_content = note_content
        self.user_id = user_id

