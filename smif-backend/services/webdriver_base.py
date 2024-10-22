# Logging import
import logSetup

# BaseClass import
from base_class import BaseClass

# Web driver imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class WebDriverBase:
    def __init__(self, webdriverPath, profilePath, logger=None):
        self.webdriverPath = webdriverPath
        self.profilePath = profilePath
        self.logger = logger or logSetup.log("WebDriverBase", "webdriverLog.txt")
        
    
    def createWebdriver(self, headless=None):
        try:
            if BaseClass.checkIfFileExist(self.webdriverPath) and BaseClass.checkIfDir(self.profilePath) :
                options = Options()
                if headless:
                    options.add_argument("-headless") 
                options.add_argument('--profile')
                options.add_argument(self.profilePath)
                return WebDriver(service=Service(self.webdriverPath), options=options)
            else:
                logger.error("Can't find Driver Path or profile directory")
        except Exception as e:
            self.logger.error(f"Error creating Webdriver: {e}")
            return False
    
    def checkIfElementIsLoaded(self, driver ,element_class):
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,element_class )))
            if element:
                self.logger.info("element is loaded in the page")
                return True
        except TimeoutException as e:
            self.logger.error("Time out on loading whatsApp")
        except Exception as e:
            self.logger.error(f"Error loading element: {e}")
        return False