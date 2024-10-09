#!/usr/bin/python3

from BaseClass import * 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import json
import getpass 


logger = logSetup.log("SharedMethods","log.txt")

class Image():
    def __init__(self, imageUrl=None, imageHash=None, imageName=None, listOfUrls=None):
        self.logger = logger
        self.Path = imageName
        self.URL = imageUrl
        self.Hash = imageHash
        self.FileName = imageName
        self.UrlList = listOfUrls

    def DownloadImage(self):
        self.logger.info(f"starting downloading {self.URL}")
        response = BaseClass.sendRequest(self.URL)
        if BaseClass.checkResponseResult(response) and self.FileName:
            ImageData = response.content
            BaseClass.WriteImage(self.FileName, ImageData)
            self.logger.info(f"Done saving the image {self.FileName}")
            return True
        else:
            self.logger.error(f"can't download the image {self.URL} ")
            return False

    def DownloadListOfImages(self):
        if self.UrlList:
            tempImageName = 0
            for i in self.UrlList:
                self.URL = i
                self.FileName = str(tempImageName)
                self.DownloadImage()
                tempImageName += 1
            else:
                self.logger.info("Done Downloading all the Images")
                return True

    def isTheSameImage(self, Image1, Image2):
        if not (Image1.Hash and Image2.Hash):
            self.logger.info("one image has no Hash starting to generate hash for both")
            imag1Hash = Image1.GenerateImageHash()
            image2hash = Image2.GenerateImageHash()
        
        if Image1.Hash == Image2.Hash:
            return True
        else:
            return False
            
   

    def GenerateImageHash(self):
        if BaseClass.checkIfFileExist(self.Path) :
            md5Hash = hashlib.md5()
            with open(self.Path, "rb") as imageFile:
                for chunk in iter(lambda: imageFile.read(4096), b""):
                    md5Hash.update(chunk)
            self.Hash = md5Hash.hexdigest()
            self.logger.info("Done generating the hash value")
            return self.Hash
        else:
            self.logger.info("can't find the image path")

class File:
    def __init__(self):
        pass

    def DownloadFile(self):
        pass
    
    def CompareFile(self):
        pass
    def GenerateFileHash(self):
        pass


class Encrypt:
    def __init__(self, password, filePath) -> None:
        getpass.getpass = lambda prompt='': password
        self.filePath = filePath
        self.password = password

    def generateKey(self, password):
        salt = b'HopeIsLife'  # Salt for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # You can adjust the number of iterations as needed
            salt=salt,
            length=32,  # Key length (32 bytes for Fernet)
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key


    # Function to decrypt data with the provided key
    def decryptData(self, data, key):
        try:
            cipher_suite = Fernet(key)
            return cipher_suite.decrypt(data).decode()
        except Exception as error:
            print("Invalid key")
            return None

    def readEData(self, filename):
        try:
            with open(filename,"rb") as file:
                loadedData = file.read()
            return loadedData
        except Exception as error:
            print("Error while loading file")
            return None
    
    def loadData(self):
        passKey = self.generateKey(self.password)
        loadedData =  self.readEData(self.filePath)
        if loadedData:
            data = self.decryptData(loadedData,passKey)
            if data:
                self.data = json.loads(data)
                return self.data
        return None

if __name__ == "__main__":
    print("hello")
 