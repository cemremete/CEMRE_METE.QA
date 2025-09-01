
"""
Data Manager for Insider Test Automation Project
Handles test data validation, bug reproduction, and expected vs actual result comparison.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class DataManager:
    """Manager for handling test data validation and bug reproduction."""
    
    def __init__(self, driver):
        """
        Initialize DataManager with WebDriver instance.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.test_results = {}
        self.performance_metrics = {}
        self.bug_reproductions = {}
    
    def is_element_present(self, locator, timeout=10):
        """
        Check if element is present in DOM.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds
            
        Returns:
            Boolean indicating if element is present
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=10):
        """
        Check if element is visible on page.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds
            
        Returns:
            Boolean indicating if element is visible
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def click_element(self, locator, timeout=10):
        """
        Click element after waiting for it to be clickable.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def get_element_text(self, locator, timeout=10):
        """
        Get text from element.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds
            
        Returns:
            Element text content
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    def execute_javascript(self, script):
        """
        Execute JavaScript in browser.
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            JavaScript execution result
        """
        return self.driver.execute_script(script)
    
    def validate_bug_001_url_dependency(self, base_url, test_url):
        """
        Validate BUG001: Production Blocker - URL parameter dependency.
        
        Args:
            base_url: Base URL without parameters
            test_url: Test URL with parameters
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bug_id": "BUG001",
            "description": "URL parameter dependency",
            "reproduced": False,
            "details": {}
        }
        
        try:
            # Test base URL without parameters
            self.driver.get(base_url)
            time.sleep(3)
            
            # Try to find test panel or popup trigger
            test_panel_found = self.is_element_present((By.XPATH, "//button[contains(text(), 'SHOW INSTANTLY')]"))
            results["details"]["base_url_functional"] = test_panel_found
            
            # Test URL with parameters
            self.driver.get(test_url)
            time.sleep(3)
            
            test_panel_with_params = self.is_element_present((By.XPATH, "//button[contains(text(), 'SHOW INSTANTLY')]"))
            results["details"]["test_url_functional"] = test_panel_with_params
            
            # Bug is reproduced if base URL doesn't work but test URL does
            if not test_panel_found and test_panel_with_params:
                results["reproduced"] = True
                results["details"]["conclusion"] = "System only works with specific URL parameters"
            elif test_panel_found and test_panel_with_params:
                results["reproduced"] = False
                results["details"]["conclusion"] = "System works with both URLs - Bug may be fixed"
            else:
                results["details"]["conclusion"] = "System not functional with either URL"
            
        except Exception as e:
            results["details"]["error"] = str(e)
        
        self.bug_reproductions["BUG001"] = results
        return results
    
    def validate_bug_002_add_to_cart(self, popup_page):
        """
        Validate BUG002: Add to Cart button not working.
        
        Args:
            popup_page: PopupPage instance
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bug_id": "BUG002",
            "description": "Add to Cart button not working",
            "reproduced": False,
            "details": {}
        }
        
        try:
            # Get initial cart count
            initial_cart_count = self._get_cart_count()
            results["details"]["initial_cart_count"] = initial_cart_count
            
            # Trigger popup
            if popup_page.click_show_instantly_button():
                time.sleep(2)
                
                # Look for Add to Cart button in popup
                add_to_cart_locators = [
                    (By.XPATH, "//button[contains(text(), 'Add to Cart')]"),
                    (By.XPATH, "//button[contains(text(), 'ADD TO CART')]"),
                    (By.CSS_SELECTOR, ".add-to-cart, .btn-add-cart"),
                    (By.XPATH, "//button[contains(@class, 'add-to-cart')]")
                ]
                
                add_to_cart_found = False
                for locator in add_to_cart_locators:
                    if self.is_element_visible(locator, timeout=2):
                        add_to_cart_found = True
                        results["details"]["add_to_cart_button_found"] = True
                        
                        # Try to click Add to Cart
                        try:
                            self.click_element(locator, timeout=5)
                            time.sleep(2)
                            
                            # Check if cart count increased
                            final_cart_count = self._get_cart_count()
                            results["details"]["final_cart_count"] = final_cart_count
                            
                            if final_cart_count > initial_cart_count:
                                results["reproduced"] = False
                                results["details"]["conclusion"] = "Add to Cart working - Bug may be fixed"
                            else:
                                results["reproduced"] = True
                                results["details"]["conclusion"] = "Add to Cart button not functional"
                            
                        except TimeoutException:
                            results["reproduced"] = True
                            results["details"]["conclusion"] = "Add to Cart button not clickable"
                        
                        break
                
                if not add_to_cart_found:
                    results["details"]["add_to_cart_button_found"] = False
                    results["details"]["conclusion"] = "Add to Cart button not found in popup"
            else:
                results["details"]["conclusion"] = "Could not trigger popup to test Add to Cart"
                
        except Exception as e:
            results["details"]["error"] = str(e)
        
        self.bug_reproductions["BUG002"] = results
        return results
    
    def validate_bug_006_performance(self, popup_page, expected_limit=2.0):
        """
        Validate BUG006: Performance Critical - 4.49s delay.
        
        Args:
            popup_page: PopupPage instance
            expected_limit: Expected load time limit in seconds
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bug_id": "BUG006",
            "description": "Performance Critical - Load delay",
            "reproduced": False,
            "details": {}
        }
        
        try:
            # Measure popup load time
            start_time = time.time()
            
            if popup_page.click_show_instantly_button():
                # Wait for popup to appear and measure time
                popup_appeared = popup_page.wait_for_popup_to_appear(timeout=10)
                
                end_time = time.time()
                load_time = end_time - start_time
                
                results["details"]["load_time"] = round(load_time, 2)
                results["details"]["expected_limit"] = expected_limit
                results["details"]["popup_appeared"] = popup_appeared
                
                if load_time > expected_limit:
                    results["reproduced"] = True
                    results["details"]["conclusion"] = f"Performance issue confirmed: {load_time}s > {expected_limit}s"
                else:
                    results["reproduced"] = False
                    results["details"]["conclusion"] = f"Performance acceptable: {load_time}s <= {expected_limit}s"
                
                # Store performance metrics
                self.performance_metrics["popup_load_time"] = load_time
                
            else:
                results["details"]["conclusion"] = "Could not trigger popup to measure performance"
                
        except Exception as e:
            results["details"]["error"] = str(e)
        
        self.bug_reproductions["BUG006"] = results
        return results
    
    def validate_bug_007_content_mapping(self, popup_page, product_page, expected_product="Mug"):
        """
        Validate BUG007: Content Critical - 90% incorrect product mapping.
        
        Args:
            popup_page: PopupPage instance
            product_page: ProductPage instance
            expected_product: Expected product name
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bug_id": "BUG007",
            "description": "Content Critical - Incorrect product mapping",
            "reproduced": False,
            "details": {}
        }
        
        try:
            # Get page title/product name
            page_title = product_page.get_page_title_text()
            results["details"]["page_title"] = page_title
            
            # Trigger popup
            if popup_page.click_show_instantly_button():
                time.sleep(2)
                
                # Get popup content
                popup_content = popup_page.get_popup_content_text()
                popup_title = popup_page.get_popup_title()
                
                results["details"]["popup_content"] = popup_content
                results["details"]["popup_title"] = popup_title
                results["details"]["expected_product"] = expected_product
                
                # Check if expected product is in page title
                page_has_expected_product = expected_product.lower() in page_title.lower()
                results["details"]["page_has_expected_product"] = page_has_expected_product
                
                # Check if popup shows the same product
                popup_has_expected_product = (
                    expected_product.lower() in popup_content.lower() or
                    expected_product.lower() in popup_title.lower()
                )
                results["details"]["popup_has_expected_product"] = popup_has_expected_product
                
                # Determine if content mapping is correct
                if page_has_expected_product and popup_has_expected_product:
                    results["reproduced"] = False
                    results["details"]["conclusion"] = "Product mapping correct - Bug may be fixed"
                elif page_has_expected_product and not popup_has_expected_product:
                    results["reproduced"] = True
                    results["details"]["conclusion"] = "Product mapping incorrect - Popup shows wrong product"
                else:
                    results["details"]["conclusion"] = "Cannot determine product mapping accuracy"
                    
            else:
                results["details"]["conclusion"] = "Could not trigger popup to test content mapping"
                
        except Exception as e:
            results["details"]["error"] = str(e)
        
        self.bug_reproductions["BUG007"] = results
        return results
    
    def validate_bug_008_close_functionality(self, popup_page):
        """
        Validate BUG008: UX Critical - Pop-up close buttons not working.
        
        Args:
            popup_page: PopupPage instance
            
        Returns:
            Dictionary with validation results
        """
        results = {
            "bug_id": "BUG008",
            "description": "UX Critical - Pop-up close buttons not working",
            "reproduced": False,
            "details": {}
        }
        
        try:
            # Test X button close
            if popup_page.click_show_instantly_button():
                time.sleep(1)
                
                # Verify popup is open
                popup_visible_before = popup_page.is_popup_visible()
                results["details"]["popup_visible_before_close"] = popup_visible_before
                
                if popup_visible_before:
                    # Try to close with X button
                    close_success = popup_page.click_close_button()
                    results["details"]["close_button_clicked"] = close_success
                    
                    if close_success:
                        time.sleep(1)
                        popup_visible_after = popup_page.is_popup_visible()
                        results["details"]["popup_visible_after_close"] = popup_visible_after
                        
                        if popup_visible_after:
                            results["reproduced"] = True
                            results["details"]["x_button_conclusion"] = "X button not working - popup still visible"
                        else:
                            results["details"]["x_button_conclusion"] = "X button working - popup closed"
                    else:
                        results["reproduced"] = True
                        results["details"]["x_button_conclusion"] = "X button not clickable"
                
                # Test outside click close (if popup still open)
                if popup_page.is_popup_visible():
                    outside_click_success = popup_page.click_outside_popup()
                    results["details"]["outside_click_attempted"] = outside_click_success
                    
                    if outside_click_success:
                        time.sleep(1)
                        popup_visible_after_outside = popup_page.is_popup_visible()
                        results["details"]["popup_visible_after_outside_click"] = popup_visible_after_outside
                        
                        if popup_visible_after_outside:
                            results["reproduced"] = True
                            results["details"]["outside_click_conclusion"] = "Outside click not working"
                        else:
                            results["details"]["outside_click_conclusion"] = "Outside click working"
                
                # Overall conclusion
                if results["reproduced"]:
                    results["details"]["conclusion"] = "Close functionality not working properly"
                else:
                    results["details"]["conclusion"] = "Close functionality working - Bug may be fixed"
                    
            else:
                results["details"]["conclusion"] = "Could not trigger popup to test close functionality"
                
        except Exception as e:
            results["details"]["error"] = str(e)
        
        self.bug_reproductions["BUG008"] = results
        return results
    
    def _get_cart_count(self):
        """
        Get current cart item count.
        
        Returns:
            Integer cart count, 0 if not found
        """
        cart_locators = [
            (By.CSS_SELECTOR, ".cart-count"),
            (By.CSS_SELECTOR, ".cart-badge"),
            (By.XPATH, "//span[contains(@class, 'cart')]//text()"),
            (By.CSS_SELECTOR, "[data-testid='cart-count']")
        ]
        
        for locator in cart_locators:
            try:
                if self.is_element_visible(locator, timeout=2):
                    count_text = self.get_element_text(locator, timeout=2)
                    # Extract number from text
                    import re
                    numbers = re.findall(r'\d+', count_text)
                    return int(numbers[0]) if numbers else 0
            except:
                continue
        
        return 0
    
    def generate_bug_reproduction_report(self):
        """
        Generate a comprehensive bug reproduction report.
        
        Returns:
            Dictionary with all bug reproduction results
        """
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_bugs_tested": len(self.bug_reproductions),
            "bugs_reproduced": sum(1 for bug in self.bug_reproductions.values() if bug["reproduced"]),
            "bugs_fixed": sum(1 for bug in self.bug_reproductions.values() if not bug["reproduced"]),
            "performance_metrics": self.performance_metrics,
            "detailed_results": self.bug_reproductions
        }
        
        return report
    
    def validate_cross_browser_compatibility(self, browser_name):
        """
        Validate cross-browser compatibility issues.
        
        Args:
            browser_name: Name of the browser being tested
            
        Returns:
            Dictionary with browser compatibility results
        """
        results = {
            "browser": browser_name,
            "compatible": True,
            "issues": []
        }
        
        try:
            # Test basic page load
            current_url = self.driver.current_url
            if not current_url:
                results["compatible"] = False
                results["issues"].append("Page failed to load")
            
            # Test JavaScript functionality
            js_test = self.execute_javascript("return typeof document !== 'undefined';")
            if not js_test:
                results["compatible"] = False
                results["issues"].append("JavaScript not working")
            
            # Test popup trigger availability
            show_button_present = self.is_element_present((By.XPATH, "//button[contains(text(), 'SHOW INSTANTLY')]"))
            if not show_button_present:
                results["compatible"] = False
                results["issues"].append("Popup trigger not available")
            
            # Browser-specific known issues
            if browser_name.lower() in ["firefox", "safari"]:
                results["known_issues"] = ["BUG005: Complete browser failure reported in manual testing"]
            
        except Exception as e:
            results["compatible"] = False
            results["issues"].append(f"Browser compatibility test failed: {str(e)}")
        
        return results