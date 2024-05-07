#!/usr/bin/python3
# Post class
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Post(BaseModel, Base):
    ''' Post class '''
    __tablename__ = 'posts'

    title = Column(String(35), nullable=False)
    content = Column(String(140), nullable=False)
    user_id = Column(String(17), ForeignKey('users.id'), nullable=False)
    
    # Define the relationship between User and Post
    user = relationship("User", back_populates="posts")
