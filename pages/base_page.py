"""
Base Page Class for Insider Test Automation Project
This class contains common methods and properties that all page classes inherit from.
It is designed to be robust, reusable, and maintainable with enhanced error handling,
performance optimizations, and best practices.
"""
import logging
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import List, Tuple, Optional, Callable, Any, Union

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.screenshot_helper import ScreenshotHelper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_automation.log'),
        logging.StreamHandler()
    ]
)

# Constants
DEFAULT_TIMEOUT = 15
MAX_RETRIES = 3
RETRY_DELAY = 1.0
SCREENSHOT_DIR = "screenshots"
LOGS_DIR = "logs"

# Ensure directories exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Custom Exceptions
class PageException(Exception):
    """Base exception for page-related errors."""
    pass

class ElementNotFoundException(PageException):
    """Raised when an element is not found."""
    pass

class ElementInteractionException(PageException):
    """Raised when element interaction fails."""
    pass

@dataclass
class ElementLocator:
    """Data class for element locators with metadata."""
    by: str
    value: str
    description: str = ""

    def to_tuple(self) -> Tuple[str, str]:
        """Convert to tuple format for Selenium."""
        return (self.by, self.value)

def retry_on_failure(max_attempts: int = MAX_RETRIES, delay: float = RETRY_DELAY,
                    exceptions: tuple = (TimeoutException, StaleElementReferenceException)):
    """
    Decorator to retry operations on failure.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
                    break
            raise last_exception
        return wrapper
    return decorator


class BasePage:
    """
    Base page class that provides common, reusable web interactions with enhanced
    error handling, retry mechanisms, and performance optimizations.
    """

    def __init__(self, driver: WebDriver, default_timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the base page with WebDriver instance and configuration.

        Args:
            driver: WebDriver instance for browser interaction.
            default_timeout: The default maximum time in seconds to wait for elements.
        """
        if not driver:
            raise ValueError("WebDriver instance is required")

        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(self.driver, default_timeout)
        self.actions = ActionChains(self.driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        # Unified screenshot helper
        self.screenshot_helper = ScreenshotHelper(self.driver, base_dir=SCREENSHOT_DIR)

        # Performance tracking
        self._operation_start_time: Optional[float] = None
        self._performance_metrics: dict = {}

    @contextmanager
    def performance_context(self, operation_name: str):
        """
        Context manager for tracking operation performance.

        Args:
            operation_name: Name of the operation being tracked
        """
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            duration = end_time - start_time
            self._performance_metrics[operation_name] = duration
            self.logger.debug(f"Operation '{operation_name}' completed in {duration:.2f}s")

    def get_performance_metrics(self) -> dict:
        """Get collected performance metrics."""
        return self._performance_metrics.copy()

    @retry_on_failure()
    def find_element(self, locator: Union[Tuple[str, str], ElementLocator],
                    timeout: Optional[int] = None) -> WebElement:
        """
        Finds a single visible element with explicit wait and retry mechanism.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            The found WebElement.

        Raises:
            ElementNotFoundException: If the element is not found within the timeout.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        actual_timeout = timeout or self.default_timeout
        wait_instance = WebDriverWait(self.driver, actual_timeout)

        with self.performance_context(f"find_element_{description}"):
            self.logger.info(f"Locating element: {description}")
            try:
                element = wait_instance.until(EC.visibility_of_element_located(locator_tuple))
                self.logger.debug(f"Element located successfully: {description}")
                return element
            except TimeoutException as e:
                error_msg = f"Element not found within {actual_timeout}s: {description}"
                self.logger.error(error_msg)
                self._take_error_screenshot(f"element_not_found_{description}")
                raise ElementNotFoundException(error_msg) from e

    @retry_on_failure()
    def find_elements(self, locator: Union[Tuple[str, str], ElementLocator],
                     timeout: Optional[int] = None) -> List[WebElement]:
        """
        Finds multiple elements with explicit wait and retry mechanism.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            A list of WebElements. Returns an empty list if no elements are found.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        actual_timeout = timeout or self.default_timeout
        wait_instance = WebDriverWait(self.driver, actual_timeout)

        with self.performance_context(f"find_elements_{description}"):
            self.logger.info(f"Locating elements: {description}")
            try:
                # Wait for at least one element to be present, then return all
                wait_instance.until(EC.presence_of_element_located(locator_tuple))
                elements = self.driver.find_elements(*locator_tuple)
                self.logger.debug(f"Located {len(elements)} elements: {description}")
                return elements
            except TimeoutException:
                self.logger.warning(f"No elements found within {actual_timeout}s: {description}")
                return []

    @retry_on_failure()
    def click_element(self, locator: Union[Tuple[str, str], ElementLocator],
                     timeout: Optional[int] = None) -> bool:
        """
        Waits for an element to be clickable and then clicks on it with retry mechanism.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            True if click was successful, False otherwise.

        Raises:
            ElementInteractionException: If the element cannot be clicked.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        actual_timeout = timeout or self.default_timeout
        wait_instance = WebDriverWait(self.driver, actual_timeout)

        with self.performance_context(f"click_element_{description}"):
            self.logger.info(f"Clicking element: {description}")
            try:
                element = wait_instance.until(EC.element_to_be_clickable(locator_tuple))
                element.click()
                self.logger.debug(f"Element clicked successfully: {description}")
                return True
            except TimeoutException as e:
                error_msg = f"Element not clickable within {actual_timeout}s: {description}"
                self.logger.error(error_msg)
                self._take_error_screenshot(f"click_failed_{description}")
                raise ElementInteractionException(error_msg) from e
            except WebDriverException as e:
                error_msg = f"WebDriver error while clicking element: {description}"
                self.logger.error(error_msg)
                raise ElementInteractionException(error_msg) from e

    @retry_on_failure()
    def send_keys_to_element(self, locator: Union[Tuple[str, str], ElementLocator],
                           text: str, clear_first: bool = True,
                           timeout: Optional[int] = None) -> bool:
        """
        Finds an element, optionally clears its content, and sends keys to it.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            text: The text to be sent to the element.
            clear_first: Whether to clear the element before sending keys.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            True if keys were sent successfully, False otherwise.

        Raises:
            ElementInteractionException: If sending keys fails.
        """
        if not text and text != "":
            raise ValueError("Text cannot be None")

        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"send_keys_{description}"):
            self.logger.info(f"Sending text to element: {description}")
            try:
                element = self.find_element(locator_tuple, timeout)
                if clear_first:
                    element.clear()
                element.send_keys(text)
                self.logger.debug(f"Text sent successfully to: {description}")
                return True
            except (TimeoutException, WebDriverException) as e:
                error_msg = f"Failed to send keys to element: {description}"
                self.logger.error(error_msg)
                self._take_error_screenshot(f"send_keys_failed_{description}")
                raise ElementInteractionException(error_msg) from e

    def is_element_visible(self, locator: Union[Tuple[str, str], ElementLocator],
                          timeout: Optional[int] = None) -> bool:
        """
        Checks if an element is visible on the page within the specified timeout.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            True if the element is visible, False otherwise.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        actual_timeout = timeout or self.default_timeout
        wait_instance = WebDriverWait(self.driver, actual_timeout)

        with self.performance_context(f"check_visibility_{description}"):
            self.logger.debug(f"Checking visibility of element: {description}")
            try:
                wait_instance.until(EC.visibility_of_element_located(locator_tuple))
                return True
            except TimeoutException:
                self.logger.debug(f"Element not visible within {actual_timeout}s: {description}")
                return False

    def wait_for_element_to_disappear(self, locator: Union[Tuple[str, str], ElementLocator],
                                     timeout: Optional[int] = None) -> bool:
        """
        Waits for an element to become invisible or disappear from the DOM.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            True if the element disappeared, False if it's still present after the timeout.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        actual_timeout = timeout or self.default_timeout
        wait_instance = WebDriverWait(self.driver, actual_timeout)

        with self.performance_context(f"wait_disappear_{description}"):
            self.logger.info(f"Waiting for element to disappear: {description}")
            try:
                result = wait_instance.until(EC.invisibility_of_element_located(locator_tuple))
                self.logger.debug(f"Element disappeared successfully: {description}")
                return result
            except TimeoutException:
                self.logger.warning(f"Element did not disappear within {actual_timeout}s: {description}")
                return False

    def scroll_to_element(self, locator: Union[Tuple[str, str], ElementLocator],
                         align_to_top: bool = True) -> bool:
        """
        Scrolls to an element to bring it into the viewport.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            align_to_top: Whether to align element to top of viewport.

        Returns:
            True if scroll was successful, False otherwise.

        Raises:
            ElementInteractionException: If scrolling fails.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"scroll_to_{description}"):
            self.logger.info(f"Scrolling to element: {description}")
            try:
                element = self.find_element(locator_tuple)
                self.driver.execute_script(f"arguments[0].scrollIntoView({str(align_to_top).lower()});", element)
                self.logger.debug(f"Scrolled to element successfully: {description}")
                return True
            except (TimeoutException, WebDriverException) as e:
                error_msg = f"Failed to scroll to element: {description}"
                self.logger.error(error_msg)
                raise ElementInteractionException(error_msg) from e

    def get_current_url(self) -> str:
        """
        Returns the current URL of the page.
        
        Returns:
            Current page URL as string.
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Returns the current page title.
        
        Returns:
            Current page title as string.
        """
        return self.driver.title

    def execute_javascript(self, script: str, *args):
        """
        Executes JavaScript code in the current window/frame.
        
        Args:
            script: The JavaScript to execute.
            *args: Any arguments to the script.
        
        Returns:
            The value returned by the script.
        """
        self.logger.info(f"Executing JavaScript: {script[:100]}...")
        return self.driver.execute_script(script, *args)

    def take_screenshot(self, filename: Optional[str] = None,
                       subfolder: str = "general") -> str:
        """
        Takes a screenshot of the current page with organized folder structure.

        Args:
            filename: Optional custom filename. If not provided, generates timestamp-based name.
            subfolder: Subfolder within screenshots directory for organization.

        Returns:
            The full path to the saved screenshot file.

        Raises:
            PageException: If screenshot capture fails.
        """
        # Map BasePage subfolder to ScreenshotHelper status
        status_map = {
            "errors": "error",
            "failed": "failed",
            "passed": "passed",
            "evidence": "evidence",
            "general": "evidence"
        }
        status = status_map.get(subfolder, "evidence")

        # Derive description from filename (helper will generate its own file name)
        description = None
        if filename:
            base_name = os.path.splitext(str(filename))[0]
            description = base_name

        with self.performance_context("take_screenshot"):
            try:
                path = self.screenshot_helper.take_screenshot(
                    test_name=self.__class__.__name__,
                    status=status,
                    description=description or ""
                )
                if not path:
                    raise PageException("ScreenshotHelper returned no path")
                self.logger.info(f"Screenshot saved: {path}")
                return path
            except Exception as e:
                error_msg = f"Failed to take screenshot: {e}"
                self.logger.error(error_msg)
                raise PageException(error_msg) from e

    def _take_error_screenshot(self, context: str) -> Optional[str]:
        """
        Takes a screenshot for error documentation purposes.

        Args:
            context: Context description for the error screenshot.

        Returns:
            Path to the screenshot file, or None if failed.
        """
        try:
            path = self.screenshot_helper.take_error_screenshot(
                test_name=self.__class__.__name__,
                error_context=str(context)
            )
            return path
        except Exception as e:
            self.logger.warning(f"Failed to take error screenshot: {e}")
            return None

    def wait_for_page_load(self, timeout: int = 30):
        """
        Waits for the page to be completely loaded.
        
        Args:
            timeout: Maximum time to wait for page load.
        """
        self.logger.info("Waiting for page to load completely")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.warning("Page load timeout reached")

    @retry_on_failure()
    def hover_over_element(self, locator: Union[Tuple[str, str], ElementLocator],
                          timeout: Optional[int] = None) -> bool:
        """
        Moves the mouse to hover over an element with retry mechanism.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            True if hover was successful, False otherwise.

        Raises:
            ElementInteractionException: If hovering fails.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"hover_over_{description}"):
            self.logger.info(f"Hovering over element: {description}")
            try:
                element = self.find_element(locator_tuple, timeout)
                self.actions.move_to_element(element).perform()
                self.logger.debug(f"Hovered over element successfully: {description}")
                return True
            except (TimeoutException, WebDriverException) as e:
                error_msg = f"Failed to hover over element: {description}"
                self.logger.error(error_msg)
                raise ElementInteractionException(error_msg) from e

    def get_element_text(self, locator: Union[Tuple[str, str], ElementLocator],
                        timeout: Optional[int] = None) -> str:
        """
        Gets the text content of an element.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            The text content of the element.

        Raises:
            ElementInteractionException: If getting text fails.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"get_text_{description}"):
            self.logger.info(f"Getting text from element: {description}")
            try:
                element = self.find_element(locator_tuple, timeout)
                text = element.text or ""
                self.logger.debug(f"Retrieved text from element: {description} (length: {len(text)})")
                return text
            except (TimeoutException, WebDriverException) as e:
                error_msg = f"Failed to get text from element: {description}"
                self.logger.error(error_msg)
                raise ElementInteractionException(error_msg) from e

    def get_element_attribute(self, locator: Union[Tuple[str, str], ElementLocator],
                             attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Gets a specific attribute value from an element.

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.
            attribute: The attribute name to retrieve.
            timeout: Custom timeout in seconds. Uses default if None.

        Returns:
            The attribute value as string, or None if attribute doesn't exist.

        Raises:
            ElementInteractionException: If getting attribute fails.
        """
        if not attribute:
            raise ValueError("Attribute name cannot be empty")

        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"get_attribute_{attribute}_{description}"):
            self.logger.info(f"Getting attribute '{attribute}' from element: {description}")
            try:
                element = self.find_element(locator_tuple, timeout)
                value = element.get_attribute(attribute)
                self.logger.debug(f"Retrieved attribute '{attribute}' from element: {description}")
                return value
            except (TimeoutException, WebDriverException) as e:
                error_msg = f"Failed to get attribute '{attribute}' from element: {description}"
                self.logger.error(error_msg)
                raise ElementInteractionException(error_msg) from e

    def is_element_present(self, locator: Union[Tuple[str, str], ElementLocator]) -> bool:
        """
        Checks if an element is present in the DOM (without waiting for visibility).

        Args:
            locator: Tuple containing the locator strategy (By) and the locator string,
                    or ElementLocator object.

        Returns:
            True if the element is present in DOM, False otherwise.
        """
        if isinstance(locator, ElementLocator):
            locator_tuple = locator.to_tuple()
            description = locator.description or str(locator_tuple)
        else:
            locator_tuple = locator
            description = str(locator_tuple)

        with self.performance_context(f"check_presence_{description}"):
            try:
                self.driver.find_element(*locator_tuple)
                self.logger.debug(f"Element present in DOM: {description}")
                return True
            except NoSuchElementException:
                self.logger.debug(f"Element not present in DOM: {description}")
                return False