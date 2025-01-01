import requests
import os
import logSetup

logger = logSetup.log("ImageHandler", "log.txt")

class ImageHandler:
    """
    A class to handle image-related operations such as downloading and writing.
    """

    @staticmethod
    def write_image(file_name: str, data: bytes) -> None:
        """
        Writes binary image data to a file.

        Args:
            file_name (str): The name of the file to write.
            data (bytes): The binary data of the image.

        Raises:
            IOError: If there is an issue writing the file.
        """
        try:
            with open(file_name, "wb") as file:
                file.write(data)
            logger.info(f"Image successfully saved: {file_name}")
        except IOError as e:
            logger.error(f"Failed to write image {file_name}: {str(e)}")
            raise

    @staticmethod
    def download_image(file_name: str, url: str) -> None:
        """
        Downloads an image from a URL and saves it to a file.

        Args:
            file_name (str): The name of the file to save the image to.
            url (str): The URL of the image.

        Raises:
            RuntimeError: If the image cannot be downloaded or saved.
        """
        try:
            logger.info(f"Starting to download {file_name} from {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200 and file_name:
                image_data = response.content
                ImageHandler.write_image(file_name, image_data)
                logger.info(f"Successfully downloaded and saved image: {file_name}")
            else:
                logger.error(f"Failed to download image. URL: {url}, Status Code: {response.status_code}")
                raise RuntimeError(f"Failed to download image from {url}")
        except requests.RequestException as e:
            logger.error(f"Error during image download: {str(e)}")
            raise RuntimeError(f"Image download failed for URL: {url}") from e
