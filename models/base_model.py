#!/usr/bin/python3
''' BaseModel class that defines
all common attributes/methods for other classes'''
import models
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()

class BaseModel():
    ''' The super class that all the other classes will inhurt from '''
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

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

    def save(self):
        ''' Updates the public instance attribute updated_at
        to the current time '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''Returns a dictionary containing all the keys/values of __dict__'''
        dict_rep = self.__dict__.copy()
        if "_sa_instance_state" in dict_rep:
            del dict_rep["_sa_instance_state"]
        if "password" in dict_rep:
            del dict_rep["password"]
        dict_rep["__class__"] = self.__class__.__name__
        dict_rep["created_at"] = dict_rep["created_at"].isoformat()
        dict_rep["updated_at"] = dict_rep["updated_at"].isoformat()
        return dict_rep

    def delete(self):
        ''' Deletes the current instance from the storage '''
        models.storage.delete(self)

    def __str__(self):
        ''' Returns a string representation of the class '''
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"