#!/usr/bin/python3
''' FileStorage '''
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.post import Post


class FileStorage:
    ''' serializes instances to a JSON file 
    and deserializes JSON file to instances '''
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        ''' returns the dictionary __objects '''
        if cls is not None:
            class_objects = {}
            class_name = cls.__name__
            for k, v in FileStorage.__objects.items():
                if class_name in k:
                    class_objects[k] = v
            return class_objects
        return FileStorage.__objects
    
    def new(self, obj):
        ''' sets in __objects the obj with key <obj class name>.id '''
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        '''  serializes __objects to the JSON file (path: __file_path) '''
        objsDictRep = {}
        for key in FileStorage.__objects.keys():
            objsDictRep[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(objsDictRep, f, indent=4)

    def reload(self):
        ''' deserializes the JSON file to __objects 
        (only if the JSON file (__file_path) exists'''
        try:
            with open(FileStorage.__file_path) as f:
                dict_objct = json.load(f)
                for v in dict_objct.values():
                    class_name = v["__class__"]
                    del v["__class__"]
                    self.new(eval(class_name)(**v))
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        # Deletes an instence 
        if obj is None:
            return
        print("remvoed object id ", obj.id)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects.pop(key)
        self.save()

    def close(self):
        """ calls reload() method for deserializing the JSON file to objects """
        self.reload()

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