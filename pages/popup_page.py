"""
Popup Page Class for Insider Test Automation Project
Handles popup/modal interactions with enhanced error handling, validation, and locator strategies.
"""

# Fix import path for direct script execution
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import logging
from typing import List, Optional, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from pages.base_page import BasePage, ElementLocator, ElementNotFoundException, ElementInteractionException

class PopupPage(BasePage):
    """
    Page object for handling popup/modal interactions with enhanced error handling,
    validation, and locator strategies.
    """

    # Enhanced locators with multiple strategies and descriptions
    POPUP_CONTAINER = ElementLocator(
        By.CSS_SELECTOR, ".popup, .modal, [role='dialog'], [aria-modal='true']",
        "Main popup/modal container"
    )
    EMAIL_INPUT = ElementLocator(
        By.CSS_SELECTOR, ".popup input[type='email'], .modal input[type='email'], [data-testid='email-input']",
        "Email input field in popup"
    )
    SUBMIT_BUTTON = ElementLocator(
        By.CSS_SELECTOR, ".popup button[type='submit'], .modal button[type='submit'], [data-testid='submit-btn']",
        "Submit button in popup"
    )
    CLOSE_BUTTON = ElementLocator(
        By.CSS_SELECTOR, ".popup .close, .modal .close, .popup button[aria-label='Close'], .modal button[aria-label='Close'], [data-testid='close-btn']",
        "Close button in popup"
    )

    # Additional locators for comprehensive popup handling
    SHOW_INSTANTLY_BUTTON = ElementLocator(
    By.CSS_SELECTOR, ".btn-show-instantly", "Show instantly trigger button"
)
    POPUP_TITLE = ElementLocator(
        By.CSS_SELECTOR, ".popup h1, .popup h2, .popup h3, .modal h1, .modal h2, .modal h3, [role='dialog'] h1",
        "Popup title/header"
    )
    POPUP_CONTENT = ElementLocator(
        By.CSS_SELECTOR, ".popup .content, .modal .content, [role='dialog'] .content",
        "Popup main content area"
    )
    OVERLAY_BACKDROP = ElementLocator(
        By.CSS_SELECTOR, ".popup-overlay, .modal-backdrop, .overlay",
        "Popup backdrop/overlay"
    )

    def __init__(self, driver: WebDriver):
        """
        Initialize the PopupPage with a WebDriver instance.

        Args:
            driver: WebDriver instance for browser interaction.
        """
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

        # Popup state tracking
        self._popup_state: Dict[str, Any] = {
            'is_visible': False,
            'last_action': None,
            'performance_metrics': {},
            'error_count': 0
        }

    def _update_popup_state(self, action: str, success: bool, **kwargs):
        """
        Update the internal popup state tracking.

        Args:
            action: The action that was performed.
            success: Whether the action was successful.
            **kwargs: Additional state information.
        """
        self._popup_state.update({
            'last_action': action,
            'last_success': success,
            'timestamp': __import__('time').time(),
            **kwargs
        })

        if not success:
            self._popup_state['error_count'] += 1

    def get_popup_state(self) -> Dict[str, Any]:
        """Get the current popup state information."""
        return self._popup_state.copy()

    def is_popup_visible(self, timeout: Optional[int] = None) -> bool:
        """
        Check if the popup container is visible on the page with enhanced validation.

        Args:
            timeout: Custom timeout for visibility check.

        Returns:
            bool: True if the popup is visible, False otherwise.
        """
        with self.performance_context("check_popup_visibility"):
            self.logger.info("Checking if popup is visible")
            try:
                is_visible = self.is_element_visible(self.POPUP_CONTAINER, timeout)
                self._update_popup_state('check_visibility', True, is_visible=is_visible)
                return is_visible
            except Exception as e:
                self.logger.error(f"Error checking popup visibility: {e}")
                self._update_popup_state('check_visibility', False, error=str(e))
                return False

    def wait_for_popup_to_appear(self, timeout: int = 10) -> bool:
        """
        Wait for the popup to appear within the specified timeout with enhanced error handling.

        Args:
            timeout: Maximum time in seconds to wait for the popup.

        Returns:
            bool: True if popup appeared, False otherwise.
        """
        with self.performance_context("wait_for_popup"):
            self.logger.info(f"Waiting for popup to appear within {timeout} seconds")
            try:
                # Use the base class method for consistency
                popup_visible = self.is_element_visible(self.POPUP_CONTAINER, timeout)
                if popup_visible:
                    self._update_popup_state('wait_appear', True)
                    self.logger.info("Popup appeared successfully")
                    return True
                else:
                    self._update_popup_state('wait_appear', False, reason="timeout")
                    self.logger.warning("Popup did not appear within the timeout")
                    return False
            except Exception as e:
                self.logger.error(f"Error waiting for popup to appear: {e}")
                self._update_popup_state('wait_appear', False, error=str(e))
                return False

    def enter_email(self, email: str, timeout: Optional[int] = None) -> bool:
        """
        Enter the provided email into the email input field after validation.

        Args:
            email: The email address to enter.
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if email was entered successfully, False otherwise.

        Raises:
            ValueError: If the email format is invalid.
            ElementInteractionException: If entering email fails.
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")

        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email format: {email}")

        with self.performance_context("enter_email"):
            self.logger.info(f"Entering email: {email}")
            try:
                success = self.send_keys_to_element(self.EMAIL_INPUT, email, timeout=timeout)
                self._update_popup_state('enter_email', success, email=email)
                return success
            except ElementInteractionException as e:
                self.logger.error(f"Failed to enter email: {e}")
                self._update_popup_state('enter_email', False, error=str(e))
                raise

    def click_submit_button(self, timeout: Optional[int] = None) -> bool:
        """
        Click the submit button in the popup with enhanced error handling.

        Args:
            timeout: Custom timeout for the click operation.

        Returns:
            bool: True if button was clicked successfully, False otherwise.

        Raises:
            ElementInteractionException: If clicking the button fails.
        """
        with self.performance_context("click_submit"):
            self.logger.info("Clicking submit button")
            try:
                success = self.click_element(self.SUBMIT_BUTTON, timeout=timeout)
                self._update_popup_state('click_submit', success)
                return success
            except ElementInteractionException as e:
                self.logger.error(f"Failed to click submit button: {e}")
                self._update_popup_state('click_submit', False, error=str(e))
                raise

    def dismiss_popup(self, timeout: Optional[int] = None) -> bool:
        """
        Dismiss the popup by clicking the close button if available.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if popup was dismissed, False otherwise.
        """
        with self.performance_context("dismiss_popup"):
            self.logger.info("Attempting to dismiss popup")
            try:
                if self.is_element_present(self.CLOSE_BUTTON):
                    success = self.click_element(self.CLOSE_BUTTON, timeout=timeout)
                    self._update_popup_state('dismiss', success)
                    return success
                else:
                    self.logger.warning("Close button not found")
                    self._update_popup_state('dismiss', False, reason="no_close_button")
                    return False
            except ElementInteractionException as e:
                self.logger.error(f"Failed to dismiss popup: {e}")
                self._update_popup_state('dismiss', False, error=str(e))
                return False

    # Additional methods for comprehensive popup handling

    def click_show_instantly_button(self, timeout: Optional[int] = None) -> bool:
        """
        Click the 'SHOW INSTANTLY' button to trigger the popup.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if button was clicked successfully, False otherwise.
        """
        with self.performance_context("click_show_instantly"):
            self.logger.info("Clicking 'SHOW INSTANTLY' button")
            try:
                success = self.click_element(self.SHOW_INSTANTLY_BUTTON, timeout=timeout)
                self._update_popup_state('trigger_popup', success)
                return success
            except ElementInteractionException as e:
                self.logger.error(f"Failed to click 'SHOW INSTANTLY' button: {e}")
                self._update_popup_state('trigger_popup', False, error=str(e))
                return False

    def get_popup_content_text(self, timeout: Optional[int] = None) -> str:
        """
        Get the text content of the popup.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            str: The popup content text, or empty string if not found.
        """
        with self.performance_context("get_popup_content"):
            self.logger.info("Getting popup content text")
            try:
                content = self.get_element_text(self.POPUP_CONTENT, timeout=timeout)
                self.logger.debug(f"Popup content retrieved (length: {len(content)})")
                return content
            except ElementInteractionException as e:
                self.logger.error(f"Failed to get popup content: {e}")
                return ""

    def get_popup_title(self, timeout: Optional[int] = None) -> str:
        """
        Get the title of the popup.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            str: The popup title text, or empty string if not found.
        """
        with self.performance_context("get_popup_title"):
            self.logger.info("Getting popup title")
            try:
                title = self.get_element_text(self.POPUP_TITLE, timeout=timeout)
                self.logger.debug(f"Popup title: {title}")
                return title
            except ElementInteractionException as e:
                self.logger.error(f"Failed to get popup title: {e}")
                return ""

    def trigger_popup_and_verify(self, timeout: Optional[int] = None) -> bool:
        """
        Trigger the popup by clicking 'SHOW INSTANTLY' and verify it appears.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if popup was triggered and is visible, False otherwise.
        """
        with self.performance_context("trigger_and_verify"):
            self.logger.info("Triggering popup and verifying appearance")
            try:
                # Click the trigger button
                if not self.click_show_instantly_button(timeout=timeout):
                    self.logger.error("Failed to click trigger button")
                    return False

                # Wait a moment for popup to appear
                import time
                time.sleep(0.5)

                # Verify popup is visible
                if self.is_popup_visible(timeout=timeout):
                    self._update_popup_state('trigger_verify', True)
                    self.logger.info("Popup triggered and verified successfully")
                    return True
                else:
                    self._update_popup_state('trigger_verify', False, reason="popup_not_visible")
                    self.logger.error("Popup was triggered but not visible")
                    return False

            except Exception as e:
                self.logger.error(f"Error triggering and verifying popup: {e}")
                self._update_popup_state('trigger_verify', False, error=str(e))
                return False

    def click_close_button(self, timeout: Optional[int] = None) -> bool:
        """
        Click the close button in the popup.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if close button was clicked successfully, False otherwise.
        """
        with self.performance_context("click_close_button"):
            self.logger.info("Clicking close button")
            try:
                success = self.click_element(self.CLOSE_BUTTON, timeout=timeout)
                self._update_popup_state('click_close', success)
                return success
            except ElementInteractionException as e:
                self.logger.error(f"Failed to click close button: {e}")
                self._update_popup_state('click_close', False, error=str(e))
                return False

    def close_popup_and_verify(self, timeout: Optional[int] = None) -> bool:
        """
        Close the popup and verify it disappears.

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if popup was closed and is no longer visible, False otherwise.
        """
        with self.performance_context("close_and_verify"):
            self.logger.info("Closing popup and verifying disappearance")
            try:
                # Click close button
                if not self.click_close_button(timeout=timeout):
                    self.logger.error("Failed to click close button")
                    return False

                # Wait a moment for popup to disappear
                import time
                time.sleep(0.5)

                # Verify popup is no longer visible
                if not self.is_popup_visible(timeout=timeout):
                    self._update_popup_state('close_verify', True)
                    self.logger.info("Popup closed and verified successfully")
                    return True
                else:
                    self._update_popup_state('close_verify', False, reason="popup_still_visible")
                    self.logger.error("Popup close button clicked but popup still visible")
                    return False

            except Exception as e:
                self.logger.error(f"Error closing and verifying popup: {e}")
                self._update_popup_state('close_verify', False, error=str(e))
                return False

    def click_outside_popup(self, timeout: Optional[int] = None) -> bool:
        """
        Click outside the popup area to close it (if supported).

        Args:
            timeout: Custom timeout for the operation.

        Returns:
            bool: True if outside click was performed successfully, False otherwise.
        """
        with self.performance_context("click_outside"):
            self.logger.info("Attempting to click outside popup")
            try:
                # Try to click on the overlay/backdrop
                if self.is_element_present(self.OVERLAY_BACKDROP):
                    success = self.click_element(self.OVERLAY_BACKDROP, timeout=timeout)
                    self._update_popup_state('click_outside', success)
                    return success
                else:
                    # Fallback: click at a specific coordinate outside popup
                    viewport_size = self.driver.get_window_size()
                    # Click at bottom-right corner (assuming popup is centered)
                    self.driver.execute_script(f"document.elementFromPoint({viewport_size['width'] - 10}, {viewport_size['height'] - 10}).click();")
                    self._update_popup_state('click_outside', True, method="coordinates")
                    self.logger.info("Clicked outside popup using coordinates")
                    return True

            except Exception as e:
                self.logger.error(f"Failed to click outside popup: {e}")
                self._update_popup_state('click_outside', False, error=str(e))
                return False

    def submit_email_form(self, email: str, wait_for_popup: bool = True,
                         timeout: Optional[int] = None) -> bool:
        """
        Submit the email form by entering email and clicking submit, with comprehensive validation.

        Args:
            email: The email address to submit.
            wait_for_popup: Whether to wait for popup to appear before submitting.
            timeout: Custom timeout for operations.

        Returns:
            bool: True if form was submitted successfully, False otherwise.
        """
        with self.performance_context("submit_email_form"):
            self.logger.info(f"Submitting email form for: {email}")
            try:
                # Validate email first
                if not self._is_valid_email(email):
                    self.logger.error(f"Invalid email format: {email}")
                    self._update_popup_state('submit_form', False, reason="invalid_email")
                    return False

                # Wait for popup if requested
                if wait_for_popup and not self.wait_for_popup_to_appear(timeout):
                    self.logger.error("Popup did not appear; cannot submit email form")
                    self._update_popup_state('submit_form', False, reason="popup_not_appeared")
                    return False

                # Verify popup is visible
                if not self.is_popup_visible(timeout):
                    self.logger.error("Popup is not visible; cannot submit email form")
                    self._update_popup_state('submit_form', False, reason="popup_not_visible")
                    return False

                # Enter email
                if not self.enter_email(email, timeout):
                    self.logger.error("Failed to enter email")
                    self._update_popup_state('submit_form', False, reason="email_entry_failed")
                    return False

                # Click submit
                if not self.click_submit_button(timeout):
                    self.logger.error("Failed to click submit button")
                    self._update_popup_state('submit_form', False, reason="submit_click_failed")
                    return False

                self._update_popup_state('submit_form', True, email=email)
                self.logger.info("Email form submitted successfully")
                return True

            except Exception as e:
                self.logger.error(f"Error submitting email form: {e}")
                self._update_popup_state('submit_form', False, error=str(e))
                return False

    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format using comprehensive regex pattern.

        Args:
            email: The email string to validate.

        Returns:
            bool: True if email is valid, False otherwise.
        """
        if not email or not isinstance(email, str):
            return False

        # More comprehensive email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))

    def validate_popup_content(self, expected_elements: List[str] = None) -> Dict[str, Any]:
        """
        Validate that the popup contains expected content elements.

        Args:
            expected_elements: List of expected content elements to check for.

        Returns:
            Dict containing validation results.
        """
        validation_results = {
            'popup_visible': False,
            'has_title': False,
            'has_content': False,
            'expected_elements_found': [],
            'validation_passed': False
        }

        try:
            validation_results['popup_visible'] = self.is_popup_visible()

            if validation_results['popup_visible']:
                title = self.get_popup_title()
                content = self.get_popup_content_text()

                validation_results['has_title'] = bool(title.strip())
                validation_results['has_content'] = bool(content.strip())

                if expected_elements:
                    for element in expected_elements:
                        if element.lower() in title.lower() or element.lower() in content.lower():
                            validation_results['expected_elements_found'].append(element)

                validation_results['validation_passed'] = (
                    validation_results['has_title'] and
                    validation_results['has_content'] and
                    (not expected_elements or len(validation_results['expected_elements_found']) > 0)
                )

        except Exception as e:
            self.logger.error(f"Error validating popup content: {e}")
            validation_results['error'] = str(e)

        return validation_results