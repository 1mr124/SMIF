#!/usr/bin/python3

import SharedMethods
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



webdriverPath = "/home/mr124/Documents/geckodriver"
profilePath =  "/home/mr124/Project/SocialMediaInvestigationFramework/WhatsAppProfile"

logger = SharedMethods.logSetup.log("whatsApp","log.txt")


class WhatsApp():
    def __init__(self,):
        self.logger = logger
        self.webdriverPath = webdriverPath
        self.profilePath = profilePath
        self.whatsAppUrl = "https://web.whatsapp.com"

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
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath)
        driver.get(self.whatsAppUrl)
        self.logger.info("Link Your Device")
        SaveCookie = input("Done Linking Save the cookie?: Y/n ")
        if SaveCookie.lower() == "y" or SaveCookie.lower == 'yes':
            cookies = driver.get_cookies()
            while not cookies:
                input("retry Getting cookies: ?")
                cookies = driver.get_cookies()
            driver.quit()
    
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

    def creatWhatssAppDriver(self):
        driver = SharedMethods.BaseClass.CreatWebDriver(self.webdriverPath, self.profilePath)
        driver.get(self.whatsAppUrl)
        self.logger.info("now opened whatsApp")
        self.driver = driver
        return True
        
    def checkIfWhatsAppLoaded(self):
        try:
            element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_3WByx")))
            if element:
                self.logger.info("whatsApp page loaded")
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")


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
            element = driver.find_element(By.CLASS_NAME, ClassName)
            if element:
                return element
            else:
                return False
        except:
            self.logger.error("can't find element")

    
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
    