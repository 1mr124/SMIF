#!/usr/bin/python3

from BaseClass import * 

logger = logSetup.log("SharedMethods","log.txt")

class Image():
    def __init__(self, imagePath=None, imageUrl=None, imageHash=None, imageName=None, listOfUrls=None):
        self.logger = logger
        self.Path = imagePath
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
            self.Path = self.FileName
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

    def isTheSameImage(Image1, Image2):
        if not (Image1.Hash and Image2.Hash):
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


if __name__ == "__main__":
    print("hello")
 