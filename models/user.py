''' A user class that inhurts from BaseModel '''
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    ''' User class '''
    __tablename__ = 'users'

    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    vip = Column(Integer, default=0)
    mic = Column(Integer, default=0)
    cam = Column(Integer, default=0)
    chat = Column(Integer, default=1)
    image = Column(Text, nullable=False)
    
    # Define the relationship between User and Post
    posts = relationship("Post", back_populates="user")
