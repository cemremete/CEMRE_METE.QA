"""
WebDriver Manager for Insider Test Automation Project
Handles WebDriver initialization, configuration, and management.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:
    """Manages WebDriver instances with different configurations."""
    
    def __init__(self):
        self.driver = None
        self.browser_name = None
        
    def get_driver(self, browser="chrome", headless=False, window_size=(1920, 1080), mobile_emulation=None):
        """
        Initialize and return WebDriver instance.
        
        Args:
            browser: Browser name ('chrome', 'firefox', 'safari')
            headless: Run in headless mode
            window_size: Tuple of (width, height)
            mobile_emulation: Mobile device emulation settings
            
        Returns:
            WebDriver instance
        """
        self.browser_name = browser.lower()
        
        if self.browser_name == "chrome":
            self.driver = self._get_chrome_driver(headless, window_size, mobile_emulation)
        elif self.browser_name == "firefox":
            self.driver = self._get_firefox_driver(headless, window_size)
        elif self.browser_name == "safari":
            self.driver = self._get_safari_driver(window_size)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
        
        return self.driver
    
    def _get_chrome_driver(self, headless, window_size, mobile_emulation):
        """Initialize Chrome WebDriver with options."""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        # Basic Chrome options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        
        # Performance optimizations
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        
        # Mobile emulation if specified
        if mobile_emulation:
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Additional options for stability
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def _get_firefox_driver(self, headless, window_size):
        """Initialize Firefox WebDriver with options."""
        firefox_options = FirefoxOptions()
        
        if headless:
            firefox_options.add_argument("--headless")
        
        # Firefox-specific options
        firefox_options.add_argument(f"--width={window_size[0]}")
        firefox_options.add_argument(f"--height={window_size[1]}")
        
        # Performance settings
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("media.volume_scale", "0.0")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.set_window_size(window_size[0], window_size[1])
        
        return driver
    
    def _get_safari_driver(self, window_size):
        """Initialize Safari WebDriver."""
        driver = webdriver.Safari()
        driver.set_window_size(window_size[0], window_size[1])
        return driver
    
    def quit_driver(self):
        """Quit the WebDriver instance."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_mobile_emulation_settings(self, device_name):
        """
        Get mobile emulation settings for Chrome.
        
        Args:
            device_name: Name of the device to emulate
            
        Returns:
            Dictionary with mobile emulation settings
        """
        mobile_devices = {
            "iPhone SE": {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15"
            },
            "iPhone 12": {
                "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
            },
            "iPad": {
                "deviceMetrics": {"width": 768, "height": 1024, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15"
            },
            "Samsung Galaxy S21": {
                "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36"
            }
        }
        
        return mobile_devices.get(device_name, mobile_devices["iPhone SE"])
    
    def take_screenshot(self, filename=None):
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Optional filename for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        if not self.driver:
            raise RuntimeError("No driver instance available")
        
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Ensure screenshots directory exists
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        
        return filepath
    
    def get_browser_info(self):
        """
        Get information about the current browser.
        
        Returns:
            Dictionary with browser information
        """
        if not self.driver:
            return {}
        
        return {
            "browser_name": self.browser_name,
            "browser_version": self.driver.capabilities.get("browserVersion", "Unknown"),
            "driver_version": self.driver.capabilities.get("chrome", {}).get("chromedriverVersion", "Unknown"),
            "platform": self.driver.capabilities.get("platformName", "Unknown"),
            "window_size": self.driver.get_window_size()
        }
    
    def maximize_window(self):
        """Maximize the browser window."""
        if self.driver:
            self.driver.maximize_window()
    
    def set_window_size(self, width, height):
        """
        Set the browser window size.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        if self.driver:
            self.driver.set_window_size(width, height)
    
    def refresh_page(self):
        """Refresh the current page."""
        if self.driver:
            self.driver.refresh()
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        if self.driver:
            self.driver.get(url)
    
    def get_current_url(self):
        """Get the current page URL."""
        if self.driver:
            return self.driver.current_url
        return ""
    
    def get_page_title(self):
        """Get the current page title."""
        if self.driver:
            return self.driver.title
        return ""
    
    def execute_script(self, script, *args):
        """
        Execute JavaScript code.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Result of JavaScript execution
        """
        if self.driver:
            return self.driver.execute_script(script, *args)
        return None