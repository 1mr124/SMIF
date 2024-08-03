#!/usr/bin/python3

import SharedMethods
from Person import *
from models import *

webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("Twitter","log.txt")


class Twitter(Person):
	def __init__(self, name=None, dateOfBirth=None, phoneNumber=None, nickName=None, username=None):
		super().__init__(name, dateOfBirth, phoneNumber, nickName, username)
		self.logger = logger

	def loadApiTokens(self):
		'''
			Args: None
			Retursn: None
			just it load the api tokesn from encrypted file
		'''
		pass
	
	def checkIfProtectedAcc(self):
		'''

		'''



if __name__ == '__main__':
	print('hello') 
	#x = SharedMethods.BaseClass.CreatWebDriver(DriverPath=webdriverPath,profilePath=profilePath)
	logger.info("Hello First Test")

