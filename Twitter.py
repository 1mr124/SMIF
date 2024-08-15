import SharedMethods
from Person import *
from models import *
import requests
from lxml import html
import json
import tweepy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime 


webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("Twitter","log.txt")


class XPath():
	def __init__(self):
		# Xpath Part
		self.nameDiv = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]'
		self.userInfoDiv = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div'
		self.protectedUserInfoDiv = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[2]'
		self.publicUserNav = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/nav'
		self.XUrl = "https://x.com/"
	


class Twitter(Person, XPath):
	def __init__(self, name=None, dateOfBirth=None, phoneNumber=None, nickName=None, username=None, apiFilePath=None, apiPass=None):
		super().__init__(name, dateOfBirth, phoneNumber, nickName, username)
		self.logger = logger
		self.Xpath = XPath()
		self.webdriverPath = webdriverPath
		self.profilePath = profilePath
		self.apiPass = apiPass
		self.apiFilePath = apiFilePath

	# Useless Fuck Elon Tusk
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
				self.logger.info("Done decryption ")
			except Exception as e:
				self.logger.error("Error in loading the api tokens")
		else:
			self.logger.error("No ApiFilePath or Pass")
			return None
		
	# Selenium Part 
	def creatXdriver(self, HeadLess=None):
		try:
			driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
			self.logger.info("driver has been created")
			self.driver = driver
			return True
		except Exception as e:
			self.logger.error("Couldn't create Driver",e)
			return False
		
	def checkIfElementIsLoadedByXpath(self, elementXpath):
		try:
			element = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, elementXpath)))
			if element:
				self.logger.info("element is loaded in the page")
				time.sleep(3)
				return True
		except TimeoutException as e:
			self.logger.error("Time out on loading whatsApp")
		except Exception as e:
			self.logger.error(f'error {e}')

	
	def goToUserPage(self):
		try:
			self.driver.get(f"{self.Xpath.XUrl}{self.username}")
			isLoded = self.checkIfElementIsLoadedByXpath(elementXpath=self.Xpath.nameDiv)
			if isLoded:
				return True
			else:
				self.logger.error("Errorr in loading User Profile")
				return False
		except Exception as e:
			self.logger.error("Error while getting the accout page",e)

	def checkIfProtectedAcc(self):
		'''

		'''
		try:
			self.goToUserPage()
			element = self.driver.find_element(By.XPATH, self.Xpath.protectedUserInfoDiv)
			if 'protected' in element.text:
				return True  
		except:
			self.logger.info("Account Not Protected")	


	# Useless - No API section  - Rate LIMIT MY ASS
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
	logger.info("Hello First Test")
	x = Twitter(username="mr12rewind")
	x.creatXdriver(HeadLess=True)
	print(x.checkIfProtectedAcc())
	input()
	x.driver.quit()
	