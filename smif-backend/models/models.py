from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey, DateTime, MetaData, Boolean)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime



def createSession():
    try:
        engine = create_engine('sqlite:///SMIF.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except:
        return False

Base = declarative_base()

class Persondb(Base):
    __tablename__ = 'person'
    userId = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    birthday = Column(String(10))
    country = Column(String(50))
    address = Column(String(100))
    creationTime    = Column(DateTime , default = datetime.now())

    # Define one-to-many relationship with WhatsApp table
    whatsappEntries = relationship('whatsAppdb', back_populates='person')
    TwitterEntries = relationship('Twitterdb', back_populates='person')
    phoneNumbers = relationship('PhoneNumbers', back_populates='person')
    spotifyEntries = relationship('Spotify', back_populates='person')



    # functions stuff
    def addPerson(self, session):
        """
        Add the current instance to the database.

        """
        try:
            existingUser = session.query(Persondb).filter_by(username=self.username).first()
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
            person = session.query(Persondb).filter_by(username=self.username).first()
            return person
        except:
            return False

class PhoneNumbers(Base):
    __tablename__ = 'phoneNumbers'
    phoneNumbersId = Column(Integer, primary_key=True)
    phoneNumber = Column(String(15), nullable=False, unique=True)
    personId = Column(Integer, ForeignKey('person.userId'))
    person = relationship('Persondb', back_populates='phoneNumbers')

class whatsAppdb(Base):
    __tablename__ = 'whatsApp'
    whatsappUserId = Column(Integer, primary_key=True)
    currentProfilePic = Column(String(100))
    currentAbout = Column(String(140))
    currentHash = Column(String(32), nullable=True, unique=True)
    
    currentbussinessCover = Column(String(100), nullable=True, default=None) 
    currentbussinessName = Column(String(50), nullable=True, default=None)

    lastOnline = Column(DateTime, nullable=True)


    phoneNumber = Column(String(17), nullable=False)

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.userId'))
    person = relationship('Persondb', back_populates='whatsappEntries')
    # One-to-Many relationship with ProfilePic
    profilePics = relationship('ProfilePic', back_populates='whatsapp', cascade='all, delete-orphan')

    aboutLog = relationship('aboutLog', back_populates='whatsAppUser')
    profilePicLog = relationship('profilePicsLog', back_populates='whatsAppUser')
    onlineLog = relationship('onlineLog', back_populates='whatsAppUser')
    bDataLog = relationship('bussnissDataLog', back_populates='whatsAppUser')



class onlineLog(Base):
    __tablename__ = 'onlineLog'
    logId = Column(Integer, primary_key=True)
    timeStamp = Column(DateTime, default=datetime.now)
    status = Column(Boolean, nullable=False)

    whatsappUserId = Column(Integer, ForeignKey('whatsApp.whatsappUserId'))
    whatsAppUser = relationship('whatsAppdb', back_populates='onlineLog')




class aboutLog(Base):
    __tablename__ = 'aboutLog'
    userId = Column(Integer, primary_key=True)
    dateChanged = Column(DateTime , default = datetime.now())
    about = Column(String(140))

    whatsappUserId = Column(Integer, ForeignKey('whatsApp.whatsappUserId'))
    whatsAppUser = relationship('whatsAppdb', back_populates='aboutLog')



class profilePicsLog(Base):
    __tablename__ = 'profilePicsLog'
    picId = Column(Integer, primary_key=True)
    dateChanged = Column(DateTime , default = datetime.now())
    picPath = Column(String(100))
    picHash = Column(String(32), nullable=False, unique=True)

    whatsappUserId = Column(Integer, ForeignKey('whatsApp.whatsappUserId'))
    whatsAppUser = relationship('whatsAppdb', back_populates='profilePicLog')


class bussnissDataLog(Base):
    __tablename__ = 'bussnissDataLog'
    bDataId = Column(Integer, primary_key=True)
    dateChanged = Column(DateTime , default = datetime.now())
    bName = Column(String(50))
    bCoverPath = Column(String(100))

    whatsappUserId = Column(Integer, ForeignKey('whatsApp.whatsappUserId'))
    whatsAppUser = relationship('whatsAppdb', back_populates='bDataLog')


class Spotify(Base):
    __tablename__ = 'spotify'
    Id = Column(Integer, primary_key=True)
    personId = Column(Integer, ForeignKey('person.userId'))
    playlistSongsNumber = Column(Integer)
    storedDate = Column(DateTime, default=datetime.now)


    person = relationship('Persondb', back_populates='spotifyEntries')



class Twitterdb(Base):
    __tablename__ = 'Twitter'
    userId = Column(Integer, primary_key=True)
    currentProfilePic = Column(String(100))
    currentBio = Column(String(200))
    userName = Column(String(15), nullable=False)
    profilePics = relationship('ProfilePic', back_populates='twitter', cascade='all, delete-orphan')

    # Define the foreign key relationship
    personId = Column(Integer, ForeignKey('person.userId'))
    person = relationship('Persondb', back_populates='TwitterEntries')





class ProfilePic(Base):
    __tablename__ = 'ProfilePic'
    userId = Column(Integer, primary_key=True)
    path = Column(String(100))
    #entity_type = Column(String(50))  # Type of the associated entity (e.g., WhatsApp, Twitter, Facebook)
    #entity_userId = Column(Integer)        # ID of the associated entity
    createdAt = Column(DateTime, default=datetime.now)
    hash = Column(String(32))
    
    whatsappId = Column(Integer, ForeignKey('whatsApp.whatsappUserId'))
    whatsapp = relationship('whatsAppdb', back_populates='profilePics')
    
    TwitterId = Column(Integer, ForeignKey('Twitter.userId'))
    twitter = relationship('Twitterdb', back_populates='profilePics')
    
