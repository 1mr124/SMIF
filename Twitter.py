import SharedMethods
from Person import *
from models import *
import requests
from lxml import html
import json

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


	# No API section  - Rate LIMIT MY ASS
	def NoAPICheckIfProtectedAcc(self):
		if not self.username:
			self.logger.error("No username to check for")
			return
			
		textToSearchFor="This account's tweets are protected."
		xpath = '/html/body/div/div/div[3]/div/h2'
		url = f"https://xcancel.com/{self.username}"
		
		try:
			response= requests.get(url)
			tree = html.fromstring(response.content)
			elements = tree.xpath(xpath)
			print(response.status_code)
			print(elements[0].text)
			if elements and elements[0].text == textToSearchFor:
				return True
			else:
				return False

		except Exception as e:
			self.logger.error("Error while getting the infos")
			self.logger.error(e)

	
		

if __name__ == '__main__':
	print('hello') 
	#x = SharedMethods.BaseClass.CreatWebDriver(DriverPath=webdriverPath,profilePath=profilePath)
	logger.info("Hello First Test")
	user=input("Enter UserName: ")
	x = Twitter(username=user)
	x.logger.info(x.getUserProfile())