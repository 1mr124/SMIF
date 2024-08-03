#!/usr/bin/python3

import SharedMethods
from Person import *
from models import *

webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("Twitter","log.txt")


class Twitter(Person):
	def __init__(self, name=None, dateOfBirth=None, phoneNumber=None, nickName=None, username=None, apiFilePath=None, apiPass=None):
		super().__init__(name, dateOfBirth, phoneNumber, nickName, username)
		self.logger = logger
		self.apiPass = apiPass
		self.apiFilePath = apiFilePath

	def loadApiTokens(self):
		'''
			Args: None
			Retursn: None
			just it load the api tokesn from encrypted file
		'''
		if self.apiFilePath and self.apiPass:
			encryptedData = SharedMethods.Encrypt(password=self.apiPass,filePath=self.apiFilePath)
			try:
				encryptedData.loadData()
				self.apiToken = encryptedData.data
			except Exception as e:
				self.logger.error("Error in loading the api tokens")
		else:
			self.logger.error("No ApiFilePath or Pass")
			return None
		
	
	def checkIfProtectedAcc(self):
		'''

		'''
		print(self.apiToken)



if __name__ == '__main__':
	print('hello') 
	#x = SharedMethods.BaseClass.CreatWebDriver(DriverPath=webdriverPath,profilePath=profilePath)
	logger.info("Hello First Test")

