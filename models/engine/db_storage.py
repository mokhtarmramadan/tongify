#!/usr/bin/python3
''' Mysql engine '''
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.post import Post
from models.user_urls import User_urls
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"User": User, "Post": Post, "User_urls": User_urls}

class DBStorage():
    __engine = None
    __session = None

    def __init__(self):
        DBStorage.__engine = create_engine('mysql+mysqldb://tongify_dev:123@localhost/tongify_db',
                                   pool_pre_ping=True)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss])
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)


    def user_id_by_email(self, user_email):
        ''' Checks if the user already logged in before '''
        user = self.__session.query(User).filter_by(email=user_email).first()
        return user


    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def count(self, cls=None):
        " Counts the number of cls"
        return len(models.storage.all(cls))
    
    def get(self, cls, id):
        " gets an object based on the id and cls name "
        objects = models.storage.all(cls)
        for v in objects.values():
            if v.id == id:
                return v
        return None
    
    def check_session(self, cls, session_id):
        " gets an object based on the id and cls name "
        objects = models.storage.all(cls)
        for v in objects.values():
            if v.id == id:
                return v
        return None