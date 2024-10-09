
from models import Persondb

class Person:
    def __init__(self, name=None, dateOfBirth=None, phoneNumber=None, nickName=None, username=None):
        self.name = name
        self.dateOfBirth = dateOfBirth
        self.phoneNumber = phoneNumber
        self.nickName = nickName
        self.username = username
        self.persondb = Persondb(name=name, username=username)
    
    def calculateAge(self):
        pass

    
