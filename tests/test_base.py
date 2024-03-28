#!/usr/bin/python3
''' The unit test for the base model '''
import unittest
from models.base_model import BaseModel

Base = BaseModel()

class TestBaseModel(unittest.TestCase):
    ''' The test class that include all the methods 
    for testing BaseModel'''
    def test_save(self):
        ''' Testing the save method of BaseModel instance '''
        pass

    def test_to_dict(self):
        ''' Testing the to_dict method of BaseMode instance '''
        pass
    def test_str(self):
        ''' Testing the str method of BaseModel instance '''
        pass


if __name__ == '__main__':
    unittest.main()