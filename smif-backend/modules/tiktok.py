from services import web_driver_handler

class TikTok:
    def __init__(self, driver_path: str, profile_path: str, base_url: str = "https://www.tiktok.com"):
        """
        Initialize the TikTok module with the given driver and profile paths.
        
        Args:
            driver_path (str): Path to the browser driver executable.
            profile_path (str): Path to the browser profile (if needed).
            base_url (str): Base URL for TikTok. Defaults to "https://www.tiktok.com".
        """
        self.base_url = base_url
        self.web_driver_handler = web_driver_handler.WebDriverHandler(driver_path=driver_path, profile_path=profile_path)
        self.driver = self.web_driver_handler.create_webdriver()


    def search_user_reposts_page(self, username: str) -> bool:
        """
        Navigate to the profile page of a given TikTok user and click the "Reposts" section.
        
        Args:
            username (str): The TikTok username for which to display the reposts.
        
        Returns:
            bool: True if the click action on the Reposts section was successful, False otherwise.
        """
        url = f"{self.base_url}/@{username}"
        self.driver.get(url)
        reposts_xpath = "//*[contains(text(), 'Reposts')]"
        clicked = self.web_driver_handler.click_element_human_like(self.driver, reposts_xpath, timeout=15)
        return clicked

    def close(self):
        """
        Close the web driver session.
        """
        self.driver.quit()
