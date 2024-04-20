from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey, DateTime, MetaData )
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime



def createSession():
    try:
        engine = create_engine('sqlite:///E.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except:
        return False

Base = declarative_base()

class Persondb(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phoneNumber = Column(String(15), nullable=False, unique=True, index=True )
    birthday = Column(String(10))
    country = Column(String(50))
    address = Column(String(100))
    creationTime    = Column(DateTime , default = datetime.now())

    # Define one-to-many relationship with WhatsApp table
    whatsappEntries = relationship('whatsAppdb', back_populates='person')
    TwitterEntries = relationship('Twitterdb', back_populates='person')


    # functions stuff
    def addPerson(self, session):
        """
        Add the current instance to the database.

        """
        try:
            existingUser = session.query(Persondb).filter_by(phoneNumber=self.phoneNumber).first()
            if existingUser:
                print("user Found")
                return False
            else:
                session.add(self)
                return True
        except:
            return False
        
    def searchForPerson(self, session):
        """
        Search for a person by their phone number.

        Args:
            session

        Returns:
            Persondb or None: The person object if found, or None if not found.
        """
        try:
            # Query the database for a person with the given phone number
            person = session.query(Persondb).filter_by(phoneNumber=self.phoneNumber).first()
            return person
        except:
            return False

class whatsAppdb(Base):
    __tablename__ = 'whatsApp'
    id = Column(Integer, primary_key=True)
    currentProfilePic = Column(String(100))
    currentAboutStatus = Column(String(140))
    currentbussinessCover = Column(String(100))
    currentbussinessName = Column(String(50))

    lastOnline = Column(DateTime, nullable=True)


    phoneNumber = Column(String(17), nullable=False)

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Persondb', back_populates='whatsappEntries')
    # One-to-Many relationship with ProfilePic
    profilePics = relationship('ProfilePic', back_populates='whatsapp', cascade='all, delete-orphan')



class Twitterdb(Base):
    __tablename__ = 'Twitter'
    id = Column(Integer, primary_key=True)
    currentProfilePic = Column(String(100))
    currentBio = Column(String(200))
    userName = Column(String(15), nullable=False)
    profilePics = relationship('ProfilePic', back_populates='twitter', cascade='all, delete-orphan')

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship('Persondb', back_populates='TwitterEntries')





class ProfilePic(Base):
    __tablename__ = 'ProfilePic'
    id = Column(Integer, primary_key=True)
    path = Column(String(100))
    #entity_type = Column(String(50))  # Type of the associated entity (e.g., WhatsApp, Twitter, Facebook)
    #entity_id = Column(Integer)        # ID of the associated entity
    createdAt = Column(DateTime, default=datetime.now)
    hash = Column(String(32))
    
    whatsappId = Column(Integer, ForeignKey('whatsApp.id'))
    whatsapp = relationship('whatsAppdb', back_populates='profilePics')
    
    TwitterId = Column(Integer, ForeignKey('Twitter.id'))
    twitter = relationship('Twitterdb', back_populates='profilePics')
    
