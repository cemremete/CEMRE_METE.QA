"""
Cross-Browser Compatibility Tests for Insider Test Automation Project
Tests based on manual findings: Chrome partial failure, Firefox/Safari complete failure.
"""

import pytest
import time
from pages.popup_page import PopupPage
from pages.product_page import ProductPage
from utils.data_manager import DataManager
from utils.test_data import BugData


class TestCrossBrowserCompatibility:
    """Test class for cross-browser compatibility validation."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, test_url, browser_name):
        """Setup for each test method."""
        self.driver = driver
        self.test_url = test_url
        self.browser_name = browser_name
        self.popup_page = PopupPage(driver)
        self.product_page = ProductPage(driver)
        self.test_data_manager = DataManager(driver)
        
        # Navigate to test URL
        self.driver.get(test_url)
        self.product_page.wait_for_page_load()
    
    @pytest.mark.critical
    @pytest.mark.cross_browser
    @pytest.mark.browser_chrome
    def test_tc017_chrome_browser_compatibility(self):
        """
        TC017: Chrome Browser Test
        Manual Result: FAIL - Multiple issues (BUG001, BUG002)
        Expected: All features work in Chrome
        """
        if self.browser_name.lower() != "chrome":
            pytest.skip("This test is specific to Chrome browser")
        
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC017_chrome_initial", "evidence")
        
        # Validate browser compatibility
        compatibility_results = self.test_data_manager.validate_cross_browser_compatibility("chrome")
        
        # Test basic functionality
        test_results = {
            "page_load": True,
            "popup_trigger": False,
            "popup_display": False,
            "popup_close": False,
            "add_to_cart": False
        }
        
        # Test popup trigger
        try:
            trigger_success = self.popup_page.click_show_instantly_button()
            test_results["popup_trigger"] = trigger_success
            
            if trigger_success:
                # Test popup display
                popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
                test_results["popup_display"] = popup_appeared
                
                self.test_data_manager.take_screenshot("TC017_chrome_popup_displayed", "evidence")
                
                if popup_appeared:
                    # Test popup close
                    close_success = self.popup_page.click_close_button()
                    if close_success:
                        time.sleep(1)
                        popup_closed = not self.popup_page.is_popup_visible()
                        test_results["popup_close"] = popup_closed
                    
                    # Test Add to Cart (if popup still open)
                    if self.popup_page.is_popup_visible():
                        bug_002_results = self.test_data_manager.validate_bug_002_add_to_cart(self.popup_page)
                        test_results["add_to_cart"] = not bug_002_results["reproduced"]
        
        except Exception as e:
            print(f"Chrome compatibility test error: {e}")
        
        # Calculate success rate
        successful_tests = sum(test_results.values())
        total_tests = len(test_results)
        success_rate = (successful_tests / total_tests) * 100
        
        # Take final screenshot
        self.test_data_manager.take_screenshot("TC017_chrome_final", "evidence")
        
        # Based on manual findings, Chrome should have partial functionality
        if success_rate >= 50:  # Partial success expected
            self.test_data_manager.take_screenshot("TC017_chrome_partial_success", "passed")
            print(f"Chrome compatibility: {success_rate:.1f}% success rate (partial functionality confirmed)")
        else:
            self.test_data_manager.take_screenshot("TC017_chrome_major_failure", "failed")
            pytest.fail(f"Chrome compatibility worse than expected: {success_rate:.1f}% success rate")
    
    @pytest.mark.critical
    @pytest.mark.cross_browser
    @pytest.mark.browser_firefox
    def test_tc018_firefox_browser_compatibility(self):
        """
        TC018: Firefox Browser Test
        Manual Result: FAIL - BUG005 (Complete failure)
        Expected: All features work in Firefox (but known to fail)
        """
        if self.browser_name.lower() != "firefox":
            pytest.skip("This test is specific to Firefox browser")
        
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC018_firefox_initial", "evidence")
        
        # Validate browser compatibility
        compatibility_results = self.test_data_manager.validate_cross_browser_compatibility("firefox")
        
        # Based on manual findings (BUG005), Firefox should completely fail
        expected_to_fail = BugData.is_test_expected_to_fail("TC018")
        
        if expected_to_fail:
            # Test basic page functionality
            try:
                # Check if page loads properly
                current_url = self.driver.current_url
                page_loaded = bool(current_url and self.test_url in current_url)
                
                # Check if popup trigger is available
                trigger_available = self.popup_page.is_element_present(
                    self.popup_page.SHOW_INSTANTLY_BUTTON
                )
                
                # Take screenshot of Firefox state
                self.test_data_manager.take_screenshot("TC018_firefox_state", "evidence")
                
                if not page_loaded or not trigger_available:
                    # Expected failure confirmed
                    self.test_data_manager.take_screenshot("TC018_firefox_expected_failure", "failed")
                    pytest.xfail("BUG005: Firefox complete failure confirmed as expected from manual testing")
                else:
                    # Unexpected success - bug may be fixed
                    self.test_data_manager.take_screenshot("TC018_firefox_unexpected_success", "passed")
                    print("Firefox compatibility better than expected - BUG005 may be fixed")
                    
            except Exception as e:
                # Exception expected due to BUG005
                self.test_data_manager.take_screenshot("TC018_firefox_exception", "failed")
                pytest.xfail(f"BUG005: Firefox failure confirmed with exception: {e}")
        else:
            # Test normal functionality
            self._test_browser_functionality("firefox")
    
    @pytest.mark.critical
    @pytest.mark.cross_browser
    @pytest.mark.browser_safari
    def test_tc019_safari_browser_compatibility(self):
        """
        TC019: Safari Browser Test
        Manual Result: FAIL - BUG005 (Complete failure)
        Expected: All features work in Safari (but known to fail)
        """
        if self.browser_name.lower() != "safari":
            pytest.skip("This test is specific to Safari browser")
        
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC019_safari_initial", "evidence")
        
        # Validate browser compatibility
        compatibility_results = self.test_data_manager.validate_cross_browser_compatibility("safari")
        
        # Based on manual findings (BUG005), Safari should completely fail
        expected_to_fail = BugData.is_test_expected_to_fail("TC019")
        
        if expected_to_fail:
            # Test basic page functionality
            try:
                # Check if page loads properly
                current_url = self.driver.current_url
                page_loaded = bool(current_url and self.test_url in current_url)
                
                # Check if popup trigger is available
                trigger_available = self.popup_page.is_element_present(
                    self.popup_page.SHOW_INSTANTLY_BUTTON
                )
                
                # Take screenshot of Safari state
                self.test_data_manager.take_screenshot("TC019_safari_state", "evidence")
                
                if not page_loaded or not trigger_available:
                    # Expected failure confirmed
                    self.test_data_manager.take_screenshot("TC019_safari_expected_failure", "failed")
                    pytest.xfail("BUG005: Safari complete failure confirmed as expected from manual testing")
                else:
                    # Unexpected success - bug may be fixed
                    self.test_data_manager.take_screenshot("TC019_safari_unexpected_success", "passed")
                    print("Safari compatibility better than expected - BUG005 may be fixed")
                    
            except Exception as e:
                # Exception expected due to BUG005
                self.test_data_manager.take_screenshot("TC019_safari_exception", "failed")
                pytest.xfail(f"BUG005: Safari failure confirmed with exception: {e}")
        else:
            # Test normal functionality
            self._test_browser_functionality("safari")
    
    @pytest.mark.medium
    @pytest.mark.cross_browser
    def test_browser_specific_features(self):
        """
        Test browser-specific features and capabilities.
        """
        browser_info = {
            "browser_name": self.browser_name,
            "user_agent": self.driver.execute_script("return navigator.userAgent;"),
            "window_size": self.driver.get_window_size(),
            "capabilities": self.driver.capabilities
        }
        
        # Take screenshot with browser info
        self.test_data_manager.take_screenshot(f"browser_info_{self.browser_name}", "evidence")
        
        # Test JavaScript execution
        js_test = self.driver.execute_script("return 'JavaScript working';")
        assert js_test == "JavaScript working", f"JavaScript not working in {self.browser_name}"
        
        # Test CSS support
        css_test = self.driver.execute_script("""
            var div = document.createElement('div');
            div.style.display = 'flex';
            return div.style.display === 'flex';
        """)
        assert css_test, f"CSS flexbox not supported in {self.browser_name}"
        
        # Test local storage
        storage_test = self.driver.execute_script("""
            try {
                localStorage.setItem('test', 'value');
                var result = localStorage.getItem('test') === 'value';
                localStorage.removeItem('test');
                return result;
            } catch(e) {
                return false;
            }
        """)
        assert storage_test, f"Local storage not working in {self.browser_name}"
        
        print(f"Browser {self.browser_name} passed basic feature tests")
    
    def _test_browser_functionality(self, browser_name):
        """
        Helper method to test basic browser functionality.
        
        Args:
            browser_name: Name of the browser being tested
        """
        functionality_results = {
            "page_load": False,
            "popup_trigger": False,
            "popup_display": False,
            "popup_close": False
        }
        
        try:
            # Test page load
            current_url = self.driver.current_url
            functionality_results["page_load"] = bool(current_url)
            
            # Test popup trigger
            trigger_success = self.popup_page.click_show_instantly_button()
            functionality_results["popup_trigger"] = trigger_success
            
            if trigger_success:
                # Test popup display
                popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
                functionality_results["popup_display"] = popup_appeared
                
                if popup_appeared:
                    # Test popup close
                    close_success = self.popup_page.click_close_button()
                    if close_success:
                        time.sleep(1)
                        popup_closed = not self.popup_page.is_popup_visible()
                        functionality_results["popup_close"] = popup_closed
            
            # Calculate success rate
            successful_tests = sum(functionality_results.values())
            total_tests = len(functionality_results)
            success_rate = (successful_tests / total_tests) * 100
            
            # Take final screenshot
            self.test_data_manager.take_screenshot(f"{browser_name}_functionality_test", "evidence")
            
            if success_rate >= 75:
                self.test_data_manager.take_screenshot(f"{browser_name}_success", "passed")
                assert True, f"{browser_name} functionality test passed: {success_rate:.1f}%"
            else:
                self.test_data_manager.take_screenshot(f"{browser_name}_failure", "failed")
                pytest.fail(f"{browser_name} functionality test failed: {success_rate:.1f}% success rate")
                
        except Exception as e:
            self.test_data_manager.take_screenshot(f"{browser_name}_error", "failed")
            pytest.fail(f"{browser_name} functionality test error: {e}")
    
    @pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
    def test_cross_browser_popup_consistency(self, browser):
        """
        Test popup behavior consistency across browsers.
        
        Args:
            browser: Browser name to test
        """
        if self.browser_name.lower() != browser.lower():
            pytest.skip(f"Test requires {browser} browser, current: {self.browser_name}")
        
        # Known issues for specific browsers
        if browser.lower() in ["firefox", "safari"]:
            pytest.xfail(f"BUG005: {browser} known to have complete failure")
        
        # Test popup consistency
        consistency_results = []
        
        for attempt in range(3):  # Test 3 times for consistency
            try:
                # Trigger popup
                trigger_success = self.popup_page.click_show_instantly_button()
                
                if trigger_success:
                    popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=5)
                    consistency_results.append(popup_appeared)
                    
                    # Close popup for next attempt
                    if popup_appeared:
                        self.popup_page.click_close_button()
                        time.sleep(1)
                else:
                    consistency_results.append(False)
                
                time.sleep(1)  # Brief pause between attempts
                
            except Exception:
                consistency_results.append(False)
        
        # Calculate consistency
        successful_attempts = sum(consistency_results)
        consistency_rate = (successful_attempts / len(consistency_results)) * 100
        
        # Take screenshot of consistency test
        self.test_data_manager.take_screenshot(f"{browser}_consistency_test", "evidence")
        
        if consistency_rate >= 66:  # At least 2 out of 3 attempts
            self.test_data_manager.take_screenshot(f"{browser}_consistent", "passed")
            assert True, f"{browser} popup behavior consistent: {consistency_rate:.1f}%"
        else:
            self.test_data_manager.take_screenshot(f"{browser}_inconsistent", "failed")
            pytest.fail(f"{browser} popup behavior inconsistent: {consistency_rate:.1f}% success rate")
    
    def teardown_method(self):
        """Cleanup after each test method."""
        try:
            # Log browser-specific results
            if hasattr(self, 'test_data_manager'):
                print(f"\n🌐 Cross-browser test completed for: {self.browser_name}")
        except Exception as e:
            print(f"Error in cross-browser teardown: {e}")