from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

# Association Table for many-to-many relationship between Person and ProfilePic
person_profilepic_association = Table(
    'person_profilepic_association',
    Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id')),
    Column('profilepic_id', Integer, ForeignKey('profilepic.id'))
)

# Association Table for many-to-many relationship between Twitter and Media
twitter_media_association = Table(
    'twitter_media_association',
    Base.metadata,
    Column('twitter_id', Integer, ForeignKey('twitter.id')),
    Column('media_id', Integer, ForeignKey('media.id'))
)

# Update the Person class
class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    birthday = Column(DateTime)
    country = Column(String)
    address = Column(String)
    creation_time = Column(DateTime, default=func.now())

    # One-to-Many relationship with WhatsApp
    whatsapp = relationship('WhatsApp', back_populates='person')

    # One-to-Many relationship with Twitter
    twitter = relationship('Twitter', back_populates='person')

    # Many-to-Many relationship with ProfilePic
    profilepics = relationship('ProfilePic', secondary=person_profilepic_association, back_populates='persons')

# Update the WhatsApp class
class WhatsApp(Base):
    __tablename__ = 'whatsapp'

    id = Column(Integer, primary_key=True)
    current_profilepic = Column(String)
    current_about_status = Column(String)
    phone_number = Column(String)
    creation_time = Column(DateTime, default=func.now())

    # Many-to-One relationship with Person
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='whatsapp')

    # Many-to-Many relationship with ProfilePic
    profilepics = relationship('ProfilePic', secondary=person_profilepic_association, back_populates='whatsapp', primaryjoin="WhatsApp.id==person_profilepic_association.c.whatsapp_id", secondaryjoin="ProfilePic.id==person_profilepic_association.c.profilepic_id")

# The rest of your code remains unchanged

class Twitter(Base):
    __tablename__ = 'twitter'

    id = Column(Integer, primary_key=True)
    current_profilepic = Column(String)
    current_bio = Column(String)
    username = Column(String)
    creation_time = Column(DateTime, default=func.now())

    # Many-to-One relationship with Person
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship('Person', back_populates='twitter')

    # Many-to-Many relationship with Media
    media = relationship('Media', secondary=twitter_media_association, back_populates='twitter')

class ProfilePic(Base):
    __tablename__ = 'profilepic'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    creation_time = Column(DateTime, default=func.now())
    hash_value = Column(String)

    # Many-to-Many relationship with Person
    persons = relationship('Person', secondary=person_profilepic_association, back_populates='profilepics')

    # Many-to-Many relationship with WhatsApp
    whatsapp = relationship('WhatsApp', secondary=person_profilepic_association, back_populates='profilepics')

    # Many-to-Many relationship with Twitter
    twitter = relationship('Twitter', secondary=twitter_media_association, back_populates='media')

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    creation_time = Column(DateTime, default=func.now())
    important = Column(Boolean)
    author = Column(Boolean)

    # Many-to-Many relationship with Twitter
    twitter = relationship('Twitter', secondary=twitter_media_association, back_populates='media')
