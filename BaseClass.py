import logSetup
import os
import subprocess
import requests
import hashlib
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver



logger = logSetup.log("BaseClass","log.txt")

class BaseClass:

    @staticmethod
    def ReadFile(Path):
        if BaseClass.checkIfFileExist(Path):
            try:
                with open(Path, 'r') as file:
                    Lines = [line.strip() for line in file.readlines() if line.strip()]
                    return Lines
            except:
                logger.error("Error in reading file {}".format(Path))
        else:
            logger.error("File does not exist")

    @staticmethod
    def makeDir(Path):
        if os.path.isdir(Path):
            return True
        else:
            os.makedirs(Path, exist_ok=True)
            return True

    @staticmethod
    def checkIfFileExist(Path):
        if Path:
            return os.path.isfile(Path)
        else:
            return False
    
    @staticmethod
    def checkIfDir(dirPath):
        return os.path.isdir(dirPath)

    @staticmethod
    def ExcuteCommand(command):
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    @staticmethod
    def checkCommandResult(result):
        try:
            if result.returncode == 0:
                return True
            else:
                return False
        except:
            logger.error("command results doesn't have returecode")

    @staticmethod
    def writeToFile(FileName, Data):
        with open(FileName, "a") as file:
            if isinstance(Data, list):
                for i in Data:
                    file.write(i+'\n')
            else:
                file.write(Data+'\n')
    @staticmethod
    def WriteImage(FileName, Data):
        with open(FileName, "wb") as file:
            file.write(Data)

    @staticmethod
    def sendRequest(url):
        return requests.get(url)

    @staticmethod
    def chekcTool(tool):
        command = f"which {tool}"
        result = BaseClass.ExcuteCommand(command)
        if BaseClass.checkCommandResult(result):
            return True
        else:
            logger.error(f"This {tool} is not installed")
            return False

    @staticmethod
    def checkResponseResult(response):
        try:
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            logger.error("response doesn't have status_code")

    @staticmethod
    def DownloadImage(FileName, URL):
        logger.info(f"starting downloading {FileName}")
        response = BaseClass.sendRequest(URL)
        if BaseClass.checkResponseResult(response) and FileName:
            ImageData = response.content
            BaseClass.WriteImage(FileName, ImageData)
            logger.info(f"Done saving the image {FileName}")
        else:
            logger.error(f"can't download the image {URL} ")


    @staticmethod
    def CreatWebDriver(DriverPath, profilePath, HeadLess=None):
        if BaseClass.checkIfFileExist(DriverPath) and BaseClass.checkIfDir(profilePath) :
            options = Options()
            if HeadLess:
                options.add_argument("-headless") 
            options.add_argument('--profile')
            options.add_argument(profilePath)
            return WebDriver(service=Service(DriverPath), options=options)
        else:
            logger.error("Can't find Driver Path or profile directory")