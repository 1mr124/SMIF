import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from services import logSetup


class WebDriverHandler:
    """
    A handler class for creating and managing Selenium WebDriver instances.
    """
    def __init__(self, driver_path: str, profile_path: str, logger=None):
        """
        Initializes the WebDriverHandler with paths and a logger.
        
        Args:
            driver_path (str): Path to the WebDriver executable.
            profile_path (str): Path to the Firefox profile directory.
            logger (optional): Custom logger instance. Defaults to a standard logger.
        """
        self.driver_path = driver_path
        self.profile_path = profile_path
        self.logger = logger or logSetup.setup_logger("WebDriverHandler", "webdriverLog.txt")

    def create_webdriver(self, headless: bool = False):
        """
        Creates and initializes a Selenium WebDriver instance.
        """
        try:
            # Validate paths
            if not os.path.isfile(self.driver_path):
                self.logger.error(f"Driver path does not exist: {self.driver_path}")
                raise FileNotFoundError(f"Driver path does not exist: {self.driver_path}")

            if not os.path.isdir(self.profile_path):
                self.logger.error(f"Profile path does not exist: {self.profile_path}")
                raise FileNotFoundError(f"Profile path does not exist: {self.profile_path}")

            # Configure Firefox options
            options = Options()
            if headless:
                options.add_argument("-headless")
            options.add_argument("--profile")
            options.add_argument(self.profile_path)
            
            # Hide automation flag
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("media.peerconnection.enabled", False)  # Example: disable WebRTC (if not needed)

            # Optionally, override the user agent with a typical one
            options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/117.0")
            
            driver = webdriver.Firefox(service=Service(self.driver_path), options=options)
            self.logger.info("WebDriver successfully created.")
            return driver
        except Exception as e:
            self.logger.error(f"Error creating WebDriver: {e}")
            raise RuntimeError(f"Failed to create WebDriver: {e}")

    def check_if_element_is_loaded(self, driver: webdriver.Firefox, element_class: str) -> bool:
        """
        Checks if a specific element is loaded on the page.
        
        Args:
            driver (webdriver.Firefox): The WebDriver instance.
            element_class (str): The class name of the element to check.
        
        Returns:
            bool: True if the element is loaded, False otherwise.
        """
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, element_class))
            )
            if element:
                self.logger.info(f"Element with class '{element_class}' is loaded.")
                return True
        except TimeoutException:
            self.logger.error(f"Timeout while waiting for element: {element_class}")
        except Exception as e:
            self.logger.error(f"Error checking element: {e}")
        return False

    def click_element_human_like(self, driver: webdriver.Firefox, xpath: str, timeout: int = 15) -> bool:
        """
        Waits for an element by XPath, scrolls it into view, and clicks it using ActionChains.
        
        Args:
            driver (webdriver.Firefox): The Selenium driver.
            xpath (str): XPath to locate the element.
            timeout (int): Maximum time to wait for the element.
        
        Returns:
            bool: True if the element was clicked successfully, False otherwise.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # Scroll element into view using JavaScript
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(random.uniform(0.5, 1.5))  # Small random delay
            
            # Use ActionChains to move to the element and click it
            actions = ActionChains(driver)
            actions.move_to_element(element).pause(random.uniform(0.3, 0.7)).click().perform()
            return True
        except Exception as e:
            self.logger.error(f"Error in click_element_human_like: {e}")
            return False

    def wait_for_element_by_xpath(self, driver: webdriver.Firefox, xpath: str, timeout: int = 10):
        """
        Waits until an element specified by XPath is present on the page.
        
        Args:
            driver (webdriver.Firefox): The Selenium WebDriver instance.
            xpath (str): The XPath of the element to wait for.
            timeout (int): Maximum wait time in seconds.
        
        Returns:
            WebElement: The located WebElement if found within the timeout, otherwise None.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.logger.info(f"Element found by XPath: {xpath}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout while waiting for element by XPath: {xpath}")
        except Exception as e:
            self.logger.error(f"Error while waiting for element by XPath: {e}")
        return None

    def wait_and_click_by_xpath(self, driver: webdriver.Firefox, xpath: str, timeout: int = 10) -> bool:
        """
        Waits until an element specified by XPath is clickable, then clicks it.
        
        Args:
            driver (webdriver.Firefox): The Selenium WebDriver instance.
            xpath (str): The XPath of the element to click.
            timeout (int): Maximum wait time in seconds.
        
        Returns:
            bool: True if the element was clicked successfully, False otherwise.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            self.logger.info(f"Clicked element by XPath: {xpath}")
            return True
        except TimeoutException:
            self.logger.error(f"Timeout while waiting to click element by XPath: {xpath}")
        except Exception as e:
            self.logger.error(f"Error while clicking element by XPath: {e}")
        return False