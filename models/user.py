''' A user class that inhurts from BaseModel '''
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    ''' User class '''
    __tablename__ = 'users'

    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    vip = Column(Integer, default=0)
    mic = Column(Integer, default=0)
    cam = Column(Integer, default=0)
    chat = Column(Integer, default=1)
    image = Column(LargeBinary, nullable=True)
    
    # Define the relationship between User and Post
    posts = relationship("Post", back_populates="user")
