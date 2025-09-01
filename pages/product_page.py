"""
Product Page Class for Insider Test Automation Project
This class represents the product page and provides methods to interact with it.
"""

# Fix import path for direct script execution
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from typing import Optional
from urllib.parse import urlparse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for the product page with common interactions."""

    # Locators
    MAIN_CONTENT = (By.TAG_NAME, "main")

    def __init__(self, driver: WebDriver, default_timeout: int = 15):
        """
        Initialize the ProductPage with WebDriver instance.

        Args:
            driver: WebDriver instance for browser interaction.
            default_timeout: Default timeout for waits in seconds.
        """
        super().__init__(driver, default_timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def navigate_to_product_page(self, url: str) -> bool:
        """
        Navigate to the product page URL and wait for it to load.

        Args:
            url: The URL of the product page to navigate to.

        Returns:
            True if navigation and page load were successful, False otherwise.

        Raises:
            ValueError: If the provided URL is invalid.
            WebDriverException: If navigation fails.
        """
        if not url or not isinstance(url, str):
            raise ValueError("Invalid URL provided")

        try:
            # Validate URL format
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")

            self.logger.info(f"Navigating to product page: {url}")
            self.driver.get(url)
            self.wait_for_page_load()
            return True
        except WebDriverException as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during navigation: {e}")
            return False

    def is_page_loaded(self) -> bool:
        """
        Check if the product page is fully loaded by verifying key elements.

        Returns:
            True if the page is loaded and main content is visible, False otherwise.
        """
        try:
            self.logger.info("Checking if product page is loaded")
            # Check if main content is visible
            return self.is_element_visible(self.MAIN_CONTENT)
        except Exception as e:
            self.logger.error(f"Error checking page load status: {e}")
            return False

    def get_main_content_text(self) -> Optional[str]:
        """
        Get the text content of the main section.

        Returns:
            The text content of the main element, or None if not found.
        """
        try:
            return self.get_element_text(self.MAIN_CONTENT)
        except Exception as e:
            self.logger.error(f"Failed to get main content text: {e}")
            return None