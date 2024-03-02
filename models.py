from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey, DateTime, MetaData )
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime



Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phoneNumber = Column(String(15))
    birthday = Column(String(10))
    country = Column(String(50))
    address = Column(String(100))
    creationTime    = Column(DateTime , default = datetime.now())

    # Define one-to-many relationship with WhatsApp table
    whastappEntries = relationship('whatsApp', back_populates='person')
    TwitterEntries = relationship('Twitter', back_populates='person')

class whatsApp(Base):
    __tablename__ = 'whatsApp'
    id = Column(Integer, primary_key=True)
    CurrentProfilePic = Column(String(100))
    CurrentAboutStatus = Column(String(200))
    phoneNumber = Column(String(15), nullable=False)

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='whastappEntries')
    # One-to-Many relationship with ProfilePic
    profilePics = relationship('ProfilePic', back_populates='whatsapp', cascade='all, delete-orphan')



class Twitter(Base):
    __tablename__ = 'Twitter'
    id = Column(Integer, primary_key=True)
    CurrentProfilePic = Column(String(100))
    CurrentBio = Column(String(200))
    userName = Column(String(15), nullable=False)
    profilePics = relationship('ProfilePic', back_populates='twitter', cascade='all, delete-orphan')

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='TwitterEntries')





class ProfilePic(Base):
    __tablename__ = 'ProfilePic'
    id = Column(Integer, primary_key=True)
    path = Column(String(100))
    #entity_type = Column(String(50))  # Type of the associated entity (e.g., WhatsApp, Twitter, Facebook)
    #entity_id = Column(Integer)        # ID of the associated entity
    created_at = Column(String(20), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    hash = Column(String(32))
    
    whatsappId = Column(Integer, ForeignKey('whatsApp.id'))
    whatsapp = relationship('whatsApp', back_populates='profilePics')
    
    TwitterId = Column(Integer, ForeignKey('Twitter.id'))
    twitter = relationship('Twitter', back_populates='profilePics')
    
