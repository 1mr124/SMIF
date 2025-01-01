import os
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
import logSetup

logger = logSetup.log("WebDriverHandler", "log.txt")

class WebDriverHandler:
    """
    A handler class for creating and managing Selenium WebDriver instances.
    """

    @staticmethod
    def create_webdriver(
        driver_path: str, 
        profile_path: str, 
        headless: bool = False, 
        additional_options: list[str] = None
    ) -> WebDriver:
        """
        Creates and initializes a Selenium WebDriver instance.

        Args:
            driver_path (str): Path to the WebDriver executable.
            profile_path (str): Path to the Firefox profile directory.
            headless (bool): Whether to run the browser in headless mode.
            additional_options (list[str]): Additional options for the WebDriver.

        Returns:
            WebDriver: The initialized WebDriver instance.

        Raises:
            FileNotFoundError: If the driver or profile path is invalid.
            RuntimeError: If the WebDriver initialization fails.
        """
        # Validate the driver path
        if not os.path.isfile(driver_path):
            logger.error(f"Driver path does not exist: {driver_path}")
            raise FileNotFoundError(f"Driver path does not exist: {driver_path}")
        
        # Validate the profile path
        if not os.path.isdir(profile_path):
            logger.error(f"Profile path does not exist: {profile_path}")
            raise FileNotFoundError(f"Profile path does not exist: {profile_path}")

        # Configure WebDriver options
        options = Options()
        if headless:
            options.add_argument("-headless")
        
        options.add_argument("--profile")
        options.add_argument(profile_path)

        # Add any additional options
        if additional_options:
            for option in additional_options:
                options.add_argument(option)
        
        # Initialize the WebDriver
        try:
            driver = WebDriver(service=Service(driver_path), options=options)
            logger.info("WebDriver successfully created.")
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise RuntimeError(f"WebDriver initialization failed: {str(e)}")
