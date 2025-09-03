"""
WebDriver Manager for Insider Test Automation Project
Handles WebDriver initialization, configuration, and management with enterprise-grade features.
"""

import os
import time
import logging
from typing import Dict, Any, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:
    """
    Enterprise-grade WebDriver manager with comprehensive browser support,
    mobile emulation, and advanced configuration options.
    """
    
    def __init__(self):
        """Initialize the DriverManager with default configuration."""
        self.driver = None
        self.browser_name = None
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_driver(self, browser: str = "chrome", headless: bool = False, 
                   window_size: Tuple[int, int] = (1920, 1080), 
                   mobile_emulation: Optional[Dict[str, Any]] = None) -> webdriver.Remote:
        """
        Initialize and return WebDriver instance with comprehensive configuration.
        
        Args:
            browser: Browser name ('chrome', 'firefox', 'safari')
            headless: Run in headless mode for CI/CD environments
            window_size: Tuple of (width, height) for browser window
            mobile_emulation: Mobile device emulation settings for responsive testing
            
        Returns:
            Configured WebDriver instance
            
        Raises:
            ValueError: If unsupported browser is specified
            RuntimeError: If driver initialization fails
        """
        self.browser_name = browser.lower()
        
        try:
            if self.browser_name == "chrome":
                self.driver = self._get_chrome_driver(headless, window_size, mobile_emulation)
            elif self.browser_name == "firefox":
                self.driver = self._get_firefox_driver(headless, window_size)
            elif self.browser_name == "safari":
                self.driver = self._get_safari_driver(window_size)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Set implicit wait for element discovery
            self.driver.implicitly_wait(10)
            
            self.logger.info(f"Successfully initialized {self.browser_name} WebDriver")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {browser} WebDriver: {str(e)}")
            raise RuntimeError(f"WebDriver initialization failed: {str(e)}") from e
    
    def _get_chrome_driver(self, headless: bool, window_size: Tuple[int, int], 
                          mobile_emulation: Optional[Dict[str, Any]]) -> webdriver.Chrome:
        """
        Initialize Chrome WebDriver with enterprise-grade options and optimizations.
        
        Args:
            headless: Enable headless mode
            window_size: Browser window dimensions
            mobile_emulation: Mobile device emulation configuration
            
        Returns:
            Configured Chrome WebDriver instance
        """
        chrome_options = ChromeOptions()
        
        # Headless configuration
        if headless:
            chrome_options.add_argument("--headless=new")  # Use new headless mode
        
        # Core stability options
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
        
        # Memory and resource management
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=4096")
        chrome_options.add_argument("--disable-background-networking")
        
        # Security and privacy enhancements
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        
        # Mobile emulation configuration
        if mobile_emulation:
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            self.logger.info(f"Mobile emulation enabled: {mobile_emulation.get('deviceName', 'Custom')}")
        
        # Anti-detection measures for automation
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional enterprise options
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-save-password-bubble")
        
        # Initialize Chrome service with automatic driver management
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to remove webdriver property for stealth mode
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.logger.debug("Chrome WebDriver initialized with enterprise configuration")
        return driver
    
    def _get_firefox_driver(self, headless: bool, window_size: Tuple[int, int]) -> webdriver.Firefox:
        """
        Initialize Firefox WebDriver with optimized configuration.
        
        Args:
            headless: Enable headless mode
            window_size: Browser window dimensions
            
        Returns:
            Configured Firefox WebDriver instance
        """
        firefox_options = FirefoxOptions()
        
        # Headless configuration
        if headless:
            firefox_options.add_argument("--headless")
        
        # Window size configuration
        firefox_options.add_argument(f"--width={window_size[0]}")
        firefox_options.add_argument(f"--height={window_size[1]}")
        
        # Performance and stability preferences
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("media.volume_scale", "0.0")
        firefox_options.set_preference("browser.tabs.remote.autostart", False)
        firefox_options.set_preference("browser.sessionstore.resume_from_crash", False)
        
        # Security and privacy preferences
        firefox_options.set_preference("network.http.phishy-userpass-length", 255)
        firefox_options.set_preference("security.csp.enable", False)
        firefox_options.set_preference("security.mixed_content.block_active_content", False)
        
        # Anti-detection preferences
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference("useAutomationExtension", False)
        firefox_options.set_preference("general.useragent.override", 
                                     "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0")
        
        # Performance optimizations
        firefox_options.set_preference("browser.cache.disk.enable", False)
        firefox_options.set_preference("browser.cache.memory.enable", False)
        firefox_options.set_preference("browser.cache.offline.enable", False)
        firefox_options.set_preference("network.http.use-cache", False)
        
        # Initialize Firefox service
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.set_window_size(window_size[0], window_size[1])
        
        self.logger.debug("Firefox WebDriver initialized with optimized configuration")
        return driver
    
    def _get_safari_driver(self, window_size: Tuple[int, int]) -> webdriver.Safari:
        """
        Initialize Safari WebDriver with basic configuration.
        
        Args:
            window_size: Browser window dimensions
            
        Returns:
            Configured Safari WebDriver instance
            
        Note:
            Safari WebDriver has limited configuration options compared to Chrome/Firefox
        """
        driver = webdriver.Safari()
        driver.set_window_size(window_size[0], window_size[1])
        
        self.logger.debug("Safari WebDriver initialized")
        return driver
    
    def quit_driver(self) -> None:
        """
        Safely quit the WebDriver instance and clean up resources.
        """
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info(f"Successfully quit {self.browser_name} WebDriver")
            except Exception as e:
                self.logger.warning(f"Error while quitting WebDriver: {str(e)}")
            finally:
                self.driver = None
                self.browser_name = None
    
    def get_mobile_emulation_settings(self, device_name: str) -> Dict[str, Any]:
        """
        Get predefined mobile emulation settings for Chrome WebDriver.
        
        Args:
            device_name: Name of the device to emulate
            
        Returns:
            Dictionary with mobile emulation configuration
        """
        mobile_devices = {
            "iPhone SE": {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
            },
            "iPhone 12": {
                "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            },
            "iPhone 12 Pro Max": {
                "deviceMetrics": {"width": 428, "height": 926, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            },
            "iPad": {
                "deviceMetrics": {"width": 768, "height": 1024, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
            },
            "iPad Pro": {
                "deviceMetrics": {"width": 1024, "height": 1366, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
            },
            "Samsung Galaxy S21": {
                "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
            },
            "Samsung Galaxy Tab": {
                "deviceMetrics": {"width": 800, "height": 1280, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-T820) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
            },
            "Google Pixel 5": {
                "deviceMetrics": {"width": 393, "height": 851, "pixelRatio": 2.75},
                "userAgent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
            }
        }
        
        device_config = mobile_devices.get(device_name, mobile_devices["iPhone SE"])
        self.logger.info(f"Mobile emulation configuration retrieved for: {device_name}")
        return device_config
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot of the current page with automatic file management.
        
        Args:
            filename: Optional custom filename for the screenshot
            
        Returns:
            Path to the saved screenshot file
            
        Raises:
            RuntimeError: If no driver instance is available or screenshot fails
        """
        if not self.driver:
            raise RuntimeError("No WebDriver instance available for screenshot")
        
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{self.browser_name}_{timestamp}.png"
        
        # Ensure screenshots directory exists
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filepath = os.path.join(screenshot_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise RuntimeError(f"Screenshot capture failed: {str(e)}") from e
    
    def get_browser_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the current browser instance.
        
        Returns:
            Dictionary containing browser information and capabilities
        """
        if not self.driver:
            return {"error": "No WebDriver instance available"}
        
        try:
            capabilities = self.driver.capabilities
            return {
                "browser_name": self.browser_name,
                "browser_version": capabilities.get("browserVersion", "Unknown"),
                "driver_version": capabilities.get("chrome", {}).get("chromedriverVersion", "Unknown"),
                "platform": capabilities.get("platformName", "Unknown"),
                "window_size": self.driver.get_window_size(),
                "current_url": self.driver.current_url,
                "page_title": self.driver.title,
                "session_id": self.driver.session_id,
                "capabilities": capabilities
            }
        except Exception as e:
            self.logger.error(f"Failed to get browser info: {str(e)}")
            return {"error": f"Failed to retrieve browser info: {str(e)}"}
    
    def maximize_window(self) -> None:
        """Maximize the browser window to full screen."""
        if self.driver:
            try:
                self.driver.maximize_window()
                self.logger.debug("Browser window maximized")
            except Exception as e:
                self.logger.warning(f"Failed to maximize window: {str(e)}")
    
    def set_window_size(self, width: int, height: int) -> None:
        """
        Set the browser window to specific dimensions.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        if self.driver:
            try:
                self.driver.set_window_size(width, height)
                self.logger.debug(f"Window size set to {width}x{height}")
            except Exception as e:
                self.logger.warning(f"Failed to set window size: {str(e)}")
    
    def refresh_page(self) -> None:
        """Refresh the current page."""
        if self.driver:
            try:
                self.driver.refresh()
                self.logger.debug("Page refreshed")
            except Exception as e:
                self.logger.warning(f"Failed to refresh page: {str(e)}")
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL with validation.
        
        Args:
            url: URL to navigate to
            
        Raises:
            ValueError: If URL is invalid
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        
        if self.driver:
            try:
                self.driver.get(url)
                self.logger.info(f"Navigated to: {url}")
            except Exception as e:
                self.logger.error(f"Failed to navigate to {url}: {str(e)}")
                raise
    
    def get_current_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            Current page URL or empty string if driver not available
        """
        if self.driver:
            try:
                return self.driver.current_url
            except Exception as e:
                self.logger.warning(f"Failed to get current URL: {str(e)}")
        return ""
    
    def get_page_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            Current page title or empty string if driver not available
        """
        if self.driver:
            try:
                return self.driver.title
            except Exception as e:
                self.logger.warning(f"Failed to get page title: {str(e)}")
        return ""
    
    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript code in the browser context.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
            
        Returns:
            Result of JavaScript execution or None if driver not available
        """
        if self.driver:
            try:
                result = self.driver.execute_script(script, *args)
                self.logger.debug(f"JavaScript executed: {script[:50]}...")
                return result
            except Exception as e:
                self.logger.error(f"Failed to execute JavaScript: {str(e)}")
                raise
        return None
    
    def clear_browser_data(self) -> None:
        """Clear browser cache, cookies, and local storage."""
        if self.driver:
            try:
                # Clear cookies
                self.driver.delete_all_cookies()
                
                # Clear local storage and session storage
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
                
                self.logger.info("Browser data cleared successfully")
            except Exception as e:
                self.logger.warning(f"Failed to clear browser data: {str(e)}")
    
    def wait_for_page_load(self, timeout: int = 30) -> bool:
        """
        Wait for page to be completely loaded.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if page loaded successfully, False otherwise
        """
        if not self.driver:
            return False
        
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.debug("Page loaded successfully")
            return True
        except Exception as e:
            self.logger.warning(f"Page load timeout or error: {str(e)}")
            return False