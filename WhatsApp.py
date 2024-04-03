#!/usr/bin/python3

import SharedMethods
from Person import *
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



webdriverPath = "/home/mr124/Documents/Projects/SMIF/geckodriver"
profilePath =  "/home/mr124/Documents/Projects/SMIF/WhatsAppProfile"

logger = SharedMethods.logSetup.log("whatsApp","log.txt")

class XPath():
    def __init__(self):
        # Xpath Part
        self.newChatXpath = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div'
        self.searchXpath = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
        self.smallImageXpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[1]/div/img'
        self.aboutXpath = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[2]/span/span'
        self.BigImageXpath='/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[1]/div/img' 
        self.bussinessProfileXpath = '/html/body/div[1]/div/div/div[2]/div[5]/span/div/span/div/div/section/div[2]/div/div/div[1]'
                        
        self.contactDivXpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/header'
        self.imageDivXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]'
        self.imageIfCoverXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div/div/img'
        self.imageIfNoCoverXpath = '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[1]/div/img'
        self.myImageXpath = '/html/body/div[1]/div/div/div[2]/div[3]/header/div[1]/div/img'
        self.whatsAppUrl = "https://web.whatsapp.com"


class WhatsApp(Person,XPath):
    def __init__(self, phoneNumber=None, name=None):
        self.logger = logger
        self.webdriverPath = webdriverPath
        self.profilePath = profilePath
        self.Xpath = XPath()
        self.Person = Person(name=name,phoneNumber=phoneNumber)

    def saveCookie(self, cookieFileName ,cookies):
        if cookies:
            with open(cookieFileName,"w") as cookieFile:
                json.dump(cookies, cookieFile, indent=4)
            self.logger.info("done writeing what's app cookie")
            return True
        else:
            self.logger.error("erro in saving the cookie")

    def LoadCookeFile(self, cookieFileName):
        if SharedMethods.BaseClass.checkIfFileExist(cookieFileName):
            with open(cookieFileName, 'r') as cookiesFile:
                cookies = json.load(cookiesFile)
                self.logger.info(f"done loading cookefile {cookieFileName}")
                return cookies
        else:
            self.logger.error("can't load cooke file")
            return False

        
    def setupWhatsAppProfile(self):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath)
            driver.get(self.Xpath.whatsAppUrl)
            self.logger.info("Link Your Device")
            SaveCookie = input("Done Linking Save the cookie?: Y/n ")
            if SaveCookie.lower() == "y" or SaveCookie.lower == 'yes':
                driver.quit()
        except:
            self.logger.error('Error in setuping the whats profile')
        
    def LoadCookies(self):
        # not ready yet
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath)
        WhatsAppCookies = self.LoadCookeFile("WhatsAppCookies.json")
        if WhatsAppCookies:
            for cookie in WhatsAppCookies:
                driver.add_cookie(cookie)
            else:
                self.logger.info("done adding the cookies")
        return driver
            
    def creatWhatssAppDriver(self, HeadLess=None):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
            driver.get(self.Xpath.whatsAppUrl)
            self.logger.info("now opened whatsApp")
            self.driver = driver
            return True
        except:
            self.logger.error("Couldn't create Driver")
            return False
        
    def creatWebDriver(self, HeadLess=None):
        try:
            driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath, HeadLess=HeadLess)
            self.logger.info("now opened Web driver")
            self.driver = driver
            return True
        except:
            self.logger.error("Couldn't create Driver")
            return False

    
    def checkIfElementIsLoaded(self, elementClass):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,elementClass )))
            if element:
                self.logger.info("element is loaded in the page")
                sleep(3)
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")
        except Exception as e:
            self.logger.error(f'error {e}')

    def checkIfElementIsLoadedByXpath(self, elementXpath):
        try:
            element = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, elementXpath)))
            if element:
                self.logger.info("element is loaded in the page")
                sleep(3)
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")
        except Exception as e:
            self.logger.error(f'error {e}')





    def findElementByXpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    def findElementByClass(self, ClassName):
        try:
            element = self.driver.find_element(By.CLASS_NAME, ClassName)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    def findElementByCssSelector(self, cssSelector):
        try:
            element = self.driver.find_element_by_css_selector(cssSelector)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error(f"couldn't find this element {cssSelector}")

    def findElementByText(self, ElementText):
        # Find element by partial text content using XPath
        try:
            element = self.driver.find_element(By.XPATH, f"//*[text()='{ElementText}']")
            if element:
                return element
            else:
                return False
        except:
            self.logger.info(f"Text {ElementText} not found in the site")
            return False
    
    def sendKeys(self, word=None):
        actions = ActionChains(self.driver)
        actions.send_keys(word)
        actions.perform()




    def openContactViaUrl(self):
        try:
            print("hello")
            print(f'{self.Xpath.whatsAppUrl}/send?phone={self.Person.phoneNumber}')
            self.driver.get(f'{self.Xpath.whatsAppUrl}/send?phone={self.Person.phoneNumber}')
            WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, self.Xpath.smallImageXpath)))
            return True
        except:
            self.logger.error("can't find contact")
            return False
    
    def searchContact(self):
        try:
            newChatElement = self.findElementByXpath(self.Xpath.newChatXpath)
            newChatElement.click()
            searchElement = self.findElementByXpath(self.Xpath.searchXpath)
            searchElement.click()
            self.sendKeys(word=self.Person.phoneNumber)
            self.logger.info("done searching for contact ")
            sleep(3)
            return True
        except:
            self.logger.error("can't find contact")
            return False

    def openContact(self):
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageElement.click()
            self.logger.info("Done opening the contact chat")
            return True
        except:
            self.logger.error("error in opening the contact chat")


    def openContactInfo(self):
        try:
            contactDiv = self.findElementByXpath(self.Xpath.contactDivXpath)
            contactDiv.click()
            self.logger.info("done opeing the about")
            return True
        except:
            self.logger.error("can't open the contact Info")
    
    def getUrlFromimg(self, element):
        try:
            if element.tag_name == 'img':
                return element.get_attribute('src')
        except:
            self.logger.error("can't find url from the element")
            return False
        
    def checkIfBussinessProfile(self):
        try:
            element = self.findElementByXpath(self.Xpath.bussinessProfileXpath)
            if element.text == 'This is a business account.':
                return True
            else:
                return False
        except:
            self.logger.error("Error in trying to know if what's app bussiness profile")

    def checkIfBussinessProfileUsingSearch(self):
        try:
            element = self.findElementByText('This is a business account.')
            if element.text == 'This is a business account.':
                return True
            else:
                return False
        except:
            self.logger.info("Not a bussniss Profile")
            return False
        

    def getSmallImageUrl(self):
        # set the value of the small image url MUSTH RUN AFTER OPEN CONTACT
        try:
            smallImageElement = self.findElementByXpath(self.Xpath.smallImageXpath)
            smallImageUrl = self.getUrlFromimg(element=smallImageElement)
            self.smallImageUrl = smallImageUrl
            self.logger.info("Done finding small image url")
            return True
        except:
            self.logger.error("can't find the small image")
            return False
    
    def getAbout(self):
        try:
            aboutElemnet = self.findElementByXpath(self.Xpath.aboutXpath)
            if aboutElemnet:
                self.about = aboutElemnet.text
                self.logger.info("done finding about")
                return True
            else:
                self.logger.error("can't find about element")
        except:
            self.logger.error("can't get about ")
        
    def findImageLink(self):
        try:
            imageElement = self.findElementByXpath(self.Xpath.BigImageXpath)
            imgLink = imageElement.get_attribute("src")
            if imgLink:
                self.imageUrl = imgLink
                self.logger.info("done finding the image url")
                return True
            else:
                self.logger.error("can't find img url")
        except:
            self.logger.error("can't find the big image url")
            return False

    def getAlluserInfo(self):
        if self.Person.name and self.Person.phoneNumber:
            contactDiv = self.checkIfElementIsLoadedByXpath(self.Xpath.contactDivXpath)
            if contactDiv:
                self.getSmallImageUrl()
                self.openContactInfo()
                self.getAbout()
                self.findImageLink()
            else:
                self.logger.error('cant find contact div element')
        else:
            self.logger.error("can't find user name or phoneNumber")

    def downloadUesrImage(self):
        try:
            if self.imageUrl and self.Person.name :
                BigImage = SharedMethods.Image(ImageURL=self.imageUrl, ImageName=f'big{self.Person.name}')
                BigImage.DownloadImage()
        except Exception as e:
            self.logger.error(f'Error {e}')

    def checkIfUserChangedPic(self):
        pass

    def createUserFoldar(self):
        pass # username foldar then whats twiiter etc - whatss > images: about:
            
    def sendMessage(self):
        pass

    def GetUserProfilePicLink(self):
        pass

    def DownloadUserProfilePic(self):
        pass

    def CheckIfUserChagedProfilePic(self):
        pass





if __name__ == "__main__":
    print("hello")