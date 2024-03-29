''' A user class that inhurts from BaseModel '''
from models.base_model import BaseModel

class User(BaseModel):
    ''' User class '''
    username = ''
    email = ''
    followers = 0
    following = 0
    vip = False
    mic = 0
    cam = 0
    chat = 1
    image = ''