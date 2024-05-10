#!/usr/bin/python3
''' user_urls class that inhurts from BaseModel '''
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User_urls(BaseModel ,Base):
    ''' Post class '''
    __tablename__ = 'user_urls'

    website_name = Column(String(25), nullable=False)
    url = Column(String(100), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    # Define the relationship between User and Post
    user = relationship("User", back_populates="user_urls")