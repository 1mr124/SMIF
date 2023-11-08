#!/usr/bin/python3

import logSetup
import requests
from BaseClass import * 

logger = logSetup.log("SharedMethods","log.txt")

class Image():
    def __init__(self, ImagePath=None, ImageURL=None, ImageHash=None, ImageName=None, ListOfUrls=None):
        self.logger = logger
        self.Path = ImagePath
        self.URL = ImageURL
        self.Hash = ImageHash
        self.FileName = ImageName
        self.UrlList = ListOfUrls

    def DownloadImage(self):
        self.logger.info(f"starting downloading {self.URL}")
        response = BaseClass.sendRequest(self.URL)
        if BaseClass.checkResponseResult(response) and self.FileName:
            ImageData = response.content
            BaseClass.WriteImage(self.FileName, ImageData)
            self.logger.info(f"Done saving the image {self.FileName}")
        else:
            self.logger.error(f"can't download the image {self.URL} ")


    def DownloadListOfImages(self):
        if self.UrlList:
            tempImageName = 0
            for i in self.UrlList:
                self.URL = i
                self.FileName = str(tempImageName)
                self.DownloadImage()
                tempImageName += 1

    def CompareImages(self, Image1, Image2):
        pass

    def GenerateImageHash(self):
        pass

class File:
    def __init__(self, FilePath=None):
        self.logger = logger.log()
        self.Path = FilePath


    def DownloadFile(self):
        self.logger.info("fuck from the File")
    
    def CompareFile(self):
        print(self.Path)

    def GenerateFileHash(self):
        pass
