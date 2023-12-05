from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime



Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)
    phoneNumber = Column(String(15))
    birthday = Column(String(10))
    country = Column(String(50))
    address = Column(String(100))
    creationTime    = Column(DateTime , default = datetime.now())

    # Define one-to-many relationship with WhatsApp table
    whastappEntries = relationship('WhatsApp', back_populates='person')
    TwitterEntries = relationship('Twitter', back_populates='person')
class WhatsApp(Base):
    __tablename__ = 'whatsApp'
    id = Column(Integer, primary_key=True)
    ProfilePic = Column(String(100))
    aboutStatus = Column(String(200))
    phoneNumber = Column(String(15), nullable=False)

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='whastappEntries')


class Twitter(Base):
    __tablename__ = 'Twitter'
    id = Column(Integer, primary_key=True)
    ProfilePic = Column(String(100))
    aboutStatus = Column(String(200))
    userName = Column(String(15), nullable=False)

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='TwitterEntries')