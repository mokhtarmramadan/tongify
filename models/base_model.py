#!/usr/bin/python3
''' BaseModel class that defines
all common attributes/methods for other classes'''
import models
import uuid
from datetime import datetime


class BaseModel():
    ''' The super class that all the other classes will inhurt from '''
    def __init__(self, *args, **kwargs):
        ''' intializes class attributes either using a dictionary
        passed to it (kwargs) or by just taking an instance of
        the class '''
        if kwargs:
            for k, v in kwargs.items():
                if k == '__class__':
                    pass
                elif k == "created_at" or k == "updated_at":
                    setattr(self, k, datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        ''' Updates the public instance attribute updated_at
        to the current time '''
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        '''Returns a dictionary containing all the keys/values of __dict__'''
        dict_rep = self.__dict__.copy()
        dict_rep["__class__"] = self.__class__.__name__
        dict_rep["created_at"] = dict_rep["created_at"].isoformat()
        dict_rep["updated_at"] = dict_rep["updated_at"].isoformat()
        return dict_rep

    def __str__(self):
        ''' Returns a string representation of the class '''
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
