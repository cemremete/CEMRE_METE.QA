"""
Core Popup Functionality Tests for Insider Test Automation Project
Tests based on manual test findings and critical bug reproduction.
"""
"""
Test suite for popup functionality
"""
import pytest
import time

# IMPORT HATA ÇÖZÜMÜ - Bu kodları buraya yaz
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.popup_page import PopupPage
from pages.product_page import ProductPage
from utils.data_manager import DataManager  # Corrected import path
from utils.test_data import TestUrlData


class TestPopupFunctionality:
    """Test class for core popup functionality based on manual test findings."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, test_url):
        """Setup for each test method."""
        self.driver = driver
        self.test_url = test_url
        self.popup_page = PopupPage(driver)
        self.product_page = ProductPage(driver)
        self.test_data_manager = DataManager(driver)  # Corrected class name
        
        # Navigate to test URL
        self.driver.get(test_url)
        self.product_page.wait_for_page_load()
    
    @pytest.mark.critical
    @pytest.mark.smoke
    def test_tc001_popup_display_basic(self):
        """
        TC001: Pop-up Display Test
        Manual Result: FAIL - BUG001 (URL parameter dependency)
        Expected: Pop-up displays successfully with English content
        """
        # Validate BUG001: URL parameter dependency
        bug_001_results = self.test_data_manager.validate_bug_001_url_dependency(
            TestUrlData.BASE_URL, self.test_url
        )
        
        # Take evidence screenshot
        self.test_data_manager.take_screenshot("TC001_before_popup_trigger")
        
        # Attempt to trigger popup
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            # Wait for popup to appear
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of popup state
            self.test_data_manager.take_screenshot("TC001_popup_triggered")
            
            if popup_appeared:
                # Verify popup is visible
                assert self.popup_page.is_popup_visible(), "Pop-up should be visible after triggering"
                
                # Verify popup content
                popup_content = self.popup_page.get_popup_content_text()
                assert popup_content, "Pop-up should have content"
                
                # Take success screenshot
                self.test_data_manager.take_screenshot("TC001_popup_success")
                
            else:
                # Bug reproduction confirmed
                pytest.fail(f"BUG001 reproduced: Pop-up failed to appear. Bug details: {bug_001_results}")
        else:
            # Cannot find trigger button - critical issue
            self.test_data_manager.take_screenshot("TC001_no_trigger_button")
            pytest.fail("CRITICAL: Cannot find 'SHOW INSTANTLY' button - BUG001 confirmed")
    
    @pytest.mark.critical
    @pytest.mark.smoke
    def test_tc002_popup_close_x_button(self):
        """
        TC002: Pop-up Close via X Button
        Manual Result: FAIL - BUG008 (Close buttons not working)
        Expected: Pop-up closes successfully when X button is clicked
        """
        # First trigger the popup
        if not self.popup_page.trigger_popup_and_verify():
            pytest.skip("Cannot trigger popup - skipping close test due to BUG001")
        
        # Take screenshot before close attempt
        self.test_data_manager.take_screenshot("TC002_before_close")
        
        # Validate BUG008: Close functionality
        bug_008_results = self.test_data_manager.validate_bug_008_close_functionality(self.popup_page)
        
        # Verify popup is initially visible
        assert self.popup_page.is_popup_visible(), "Pop-up should be visible before close attempt"
        
        # Attempt to close popup with X button
        close_success = self.popup_page.click_close_button()
        
        if close_success:
            # Wait for close animation
            time.sleep(1)
            
            # Verify popup is closed
            popup_still_visible = self.popup_page.is_popup_visible(timeout=3)
            
            # Take screenshot after close attempt
            self.test_data_manager.take_screenshot("TC002_after_close")
            
            if popup_still_visible:
                # BUG008 reproduced
                self.test_data_manager.take_screenshot("TC002_close_failed")
                pytest.fail(f"BUG008 reproduced: X button not working. Bug details: {bug_008_results}")
            else:
                # Close worked - bug may be fixed
                self.test_data_manager.take_screenshot("TC002_close_success")
                assert True, "Pop-up closed successfully"
        else:
            # Cannot click close button
            self.test_data_manager.take_screenshot("TC002_close_button_not_found")
            pytest.fail("BUG008 confirmed: Close button not found or not clickable")
    
    @pytest.mark.critical
    @pytest.mark.smoke
    def test_tc003_popup_close_outside_click(self):
        """
        TC003: Pop-up Close via Outside Click
        Manual Result: FAIL - BUG008 (Close buttons not working)
        Expected: Pop-up closes when clicking outside popup area
        """
        # First trigger the popup
        if not self.popup_page.trigger_popup_and_verify():
            pytest.skip("Cannot trigger popup - skipping outside click test due to BUG001")
        
        # Take screenshot before outside click
        self.test_data_manager.take_screenshot("TC003_before_outside_click")
        
        # Verify popup is initially visible
        assert self.popup_page.is_popup_visible(), "Pop-up should be visible before outside click"
        
        # Attempt to close popup by clicking outside
        outside_click_success = self.popup_page.click_outside_popup()
        
        if outside_click_success:
            # Wait for close animation
            time.sleep(1)
            
            # Verify popup is closed
            popup_still_visible = self.popup_page.is_popup_visible(timeout=3)
            
            # Take screenshot after outside click
            self.test_data_manager.take_screenshot("TC003_after_outside_click")
            
            if popup_still_visible:
                # BUG008 reproduced - outside click not working
                self.test_data_manager.take_screenshot("TC003_outside_click_failed")
                pytest.fail("BUG008 reproduced: Outside click not working to close popup")
            else:
                # Outside click worked
                self.test_data_manager.take_screenshot("TC003_outside_click_success")
                assert True, "Pop-up closed successfully with outside click"
        else:
            # Outside click failed
            self.test_data_manager.take_screenshot("TC003_outside_click_error")
            pytest.fail("BUG008 confirmed: Outside click functionality not working")
    
    @pytest.mark.critical
    @pytest.mark.performance
    def test_tc004_popup_load_performance(self):
        """
        TC004: Pop-up Load Performance
        Manual Result: FAIL - BUG006 (4.49s delay > 2s standard)
        Expected: Pop-up loads within 2 seconds
        """
        # Take screenshot before performance test
        self.test_data_manager.take_screenshot("TC004_before_performance_test")
        
        # Validate BUG006: Performance issue
        bug_006_results = self.test_data_manager.validate_bug_006_performance(
            self.popup_page, expected_limit=2.0
        )
        
        # Extract performance data
        load_time = bug_006_results["details"].get("load_time", 0)
        expected_limit = bug_006_results["details"].get("expected_limit", 2.0)
        
        # Take screenshot after performance test
        self.test_data_manager.take_screenshot("TC004_after_performance_test")
        
        if bug_006_results["reproduced"]:
            # Performance issue reproduced
            self.test_data_manager.take_screenshot("TC004_performance_fail")
            pytest.fail(f"BUG006 reproduced: Load time {load_time}s exceeds {expected_limit}s limit")
        else:
            # Performance acceptable
            self.test_data_manager.take_screenshot("TC004_performance_pass")
            assert load_time <= expected_limit, f"Pop-up loaded in {load_time}s (within {expected_limit}s limit)"
    
    @pytest.mark.critical
    @pytest.mark.critical 
    def test_tc010_product_popup_content_matching(self):
        """
        TC010: Product-Popup Content Matching
        Manual Result: FAIL - BUG007 (90% incorrect product mapping)
        Expected: Pop-up product matches page product
        """
        # Navigate to a specific product page (Mug)
        mug_product_url = f"{TestUrlData.BASE_URL}?product=mug"  # Adjust URL as needed
        self.driver.get(mug_product_url)
        time.sleep(2)
        
        # Take screenshot of product page
        self.test_data_manager.take_screenshot("TC010_product_page")
        
        # Validate BUG007: Content mapping
        bug_007_results = self.test_data_manager.validate_bug_007_content_mapping(
            self.popup_page, self.product_page, expected_product="Mug"
        )
        
        # Take screenshot after content validation
        self.test_data_manager.take_screenshot("TC010_content_validation")
        
        if bug_007_results["reproduced"]:
            # Content mapping issue reproduced
            self.test_data_manager.take_screenshot("TC010_content_mapping_fail")
            pytest.fail(f"BUG007 reproduced: Incorrect product mapping. Details: {bug_007_results['details']}")
        else:
            # Content mapping correct
            self.test_data_manager.take_screenshot("TC010_content_mapping_pass")
            assert True, "Product content mapping is correct"
    
    @pytest.mark.critical
    @pytest.mark.critical
    def test_tc023_add_to_cart_functionality(self):
        """
        TC023: Add to Cart Functionality
        Manual Result: FAIL - BUG002 (Add to Cart button not working)
        Expected: Product added to cart successfully
        """
        # Take screenshot before Add to Cart test
        self.test_data_manager.take_screenshot("TC023_before_add_to_cart")
        
        # Validate BUG002: Add to Cart functionality
        bug_002_results = self.test_data_manager.validate_bug_002_add_to_cart(self.popup_page)
        
        # Take screenshot after Add to Cart test
        self.test_data_manager.take_screenshot("TC023_after_add_to_cart")
        
        if bug_002_results["reproduced"]:
            # Add to Cart issue reproduced
            self.test_data_manager.take_screenshot("TC023_add_to_cart_fail")
            pytest.fail(f"BUG002 reproduced: Add to Cart not working. Details: {bug_002_results['details']}")
        else:
            # Add to Cart working
            self.test_data_manager.take_screenshot("TC023_add_to_cart_pass")
            assert True, "Add to Cart functionality working correctly"
    
    @pytest.mark.medium
    @pytest.mark.critical 
    def test_tc005_popup_content_validation(self):
        """
        TC005: Pop-up Content Validation
        Manual Result: FAIL - BUG007 (Content issues)
        Expected: Pop-up displays correct English content
        """
        # Trigger popup
        if not self.popup_page.trigger_popup_and_verify():
            pytest.skip("Cannot trigger popup - skipping content validation due to BUG001")
        
        # Take screenshot of popup content
        self.test_data_manager.take_screenshot("TC005_popup_content")
        
        # Get popup content
        popup_content = self.popup_page.get_popup_content_text()
        popup_title = self.popup_page.get_popup_title()
        
        # Validate content is not empty
        assert popup_content or popup_title, "Pop-up should have visible content"
        
        # Check for expected content (based on manual findings)
        expected_content = ["Turkish", "English"]  # Adjust based on actual expected content
        
        content_found = False
        for expected in expected_content:
            if expected.lower() in popup_content.lower() or expected.lower() in popup_title.lower():
                content_found = True
                break
        
        if content_found:
            self.test_data_manager.take_screenshot("TC005_content_valid")
            assert True, "Pop-up content validation passed"
        else:
            self.test_data_manager.take_screenshot("TC005_content_invalid")
            pytest.fail(f"Pop-up content validation failed. Content: '{popup_content}', Title: '{popup_title}'")
    
    @pytest.mark.medium
    @pytest.mark.critical 
    def test_tc006_popup_redisplay(self):
        """
        TC006: Pop-up Re-display Test
        Manual Result: PARTIAL - Pop-up can be re-triggered
        Expected: Pop-up displays again after being closed
        """
        # First display cycle
        if not self.popup_page.trigger_popup_and_verify():
            pytest.skip("Cannot trigger popup initially - skipping redisplay test due to BUG001")
        
        # Close popup
        if not self.popup_page.close_popup_and_verify():
            pytest.skip("Cannot close popup - skipping redisplay test due to BUG008")
        
        # Take screenshot before redisplay
        self.test_data_manager.take_screenshot("TC006_before_redisplay")
        
        # Second display cycle
        redisplay_success = self.popup_page.trigger_popup_and_verify()
        
        # Take screenshot after redisplay attempt
        self.test_data_manager.take_screenshot("TC006_after_redisplay")
        
        if redisplay_success:
            self.test_data_manager.take_screenshot("TC006_redisplay_success")
            assert True, "Pop-up successfully redisplayed"
        else:
            self.test_data_manager.take_screenshot("TC006_redisplay_fail")
            pytest.fail("Pop-up failed to redisplay after being closed")
    
    def teardown_method(self):
        """Cleanup after each test method."""
        try:
            # Generate bug reproduction report
            if hasattr(self, 'test_data_manager'):
                bug_report = self.test_data_manager.generate_bug_reproduction_report()
                print(f"\n📊 Bug Reproduction Summary: {bug_report['bugs_reproduced']}/{bug_report['total_bugs_tested']} bugs reproduced")
        except Exception as e:
            print(f"Error in teardown: {e}")
# ============================================================================
    # CROSS-BROWSER COMPATIBILITY TESTS
    # ============================================================================
    
    @pytest.mark.critical
    @pytest.mark.browser
    def test_tc018_firefox_browser_test(self):
        """
        TC018: Firefox Browser Test
        Manual Result: FAIL - BUG005 (Firefox complete failure)
        Expected: Pop-up works in Firefox browser
        """
        # Take screenshot before Firefox test
        self.test_data_manager.take_screenshot("TC018_firefox_before")
        
        # Validate BUG005: Firefox compatibility
        bug_005_results = self.test_data_manager.validate_cross_browser_compatibility(
            self.popup_page, browser="firefox"
        )
        
        # Attempt to trigger popup in Firefox
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            # Wait for popup to appear
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of Firefox popup state
            self.test_data_manager.take_screenshot("TC018_firefox_popup_state")
            
            if popup_appeared:
                # Firefox popup working - bug may be fixed
                self.test_data_manager.take_screenshot("TC018_firefox_success")
                assert True, "Firefox popup functionality working"
            else:
                # BUG005 reproduced - Firefox failure
                self.test_data_manager.take_screenshot("TC018_firefox_failure")
                pytest.fail(f"BUG005 reproduced: Firefox popup failed. Details: {bug_005_results}")
        else:
            # Cannot find trigger button in Firefox
            self.test_data_manager.take_screenshot("TC018_firefox_no_trigger")
            pytest.fail("BUG005 confirmed: Firefox trigger button not found")
    
    @pytest.mark.critical
    @pytest.mark.browser
    def test_tc019_safari_browser_test(self):
        """
        TC019: Safari Browser Test
        Manual Result: FAIL - BUG005 (Safari complete failure)
        Expected: Pop-up works in Safari browser
        """
        # Take screenshot before Safari test
        self.test_data_manager.take_screenshot("TC019_safari_before")
        
        # Validate BUG005: Safari compatibility
        bug_005_results = self.test_data_manager.validate_cross_browser_compatibility(
            self.popup_page, browser="safari"
        )
        
        # Attempt to trigger popup in Safari
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            # Wait for popup to appear
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of Safari popup state
            self.test_data_manager.take_screenshot("TC019_safari_popup_state")
            
            if popup_appeared:
                # Safari popup working - bug may be fixed
                self.test_data_manager.take_screenshot("TC019_safari_success")
                assert True, "Safari popup functionality working"
            else:
                # BUG005 reproduced - Safari failure
                self.test_data_manager.take_screenshot("TC019_safari_failure")
                pytest.fail(f"BUG005 reproduced: Safari popup failed. Details: {bug_005_results}")
        else:
            # Cannot find trigger button in Safari
            self.test_data_manager.take_screenshot("TC019_safari_no_trigger")
            pytest.fail("BUG005 confirmed: Safari trigger button not found")
    
    @pytest.mark.critical
    @pytest.mark.browser
    def test_tc020_cross_browser_compatibility(self):
        """
        TC020: Cross-Browser Compatibility Test
        Manual Result: FAIL - BUG005 (Cross-browser issues)
        Expected: Pop-up works consistently across all browsers
        """
        # Take screenshot before cross-browser test
        self.test_data_manager.take_screenshot("TC020_cross_browser_before")
        
        # Get current browser info
        current_browser = self.driver.capabilities.get('browserName', 'unknown').lower()
        
        # Validate BUG005: Cross-browser compatibility
        bug_005_results = self.test_data_manager.validate_cross_browser_compatibility(
            self.popup_page, browser=current_browser
        )
        
        # Test popup functionality
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of cross-browser popup state
            self.test_data_manager.take_screenshot(f"TC020_{current_browser}_popup_state")
            
            if popup_appeared:
                # Cross-browser popup working
                self.test_data_manager.take_screenshot(f"TC020_{current_browser}_success")
                assert True, f"Cross-browser popup working in {current_browser}"
            else:
                # BUG005 reproduced - cross-browser failure
                self.test_data_manager.take_screenshot(f"TC020_{current_browser}_failure")
                pytest.fail(f"BUG005 reproduced: Cross-browser popup failed in {current_browser}")
        else:
            # Cross-browser trigger button issue
            self.test_data_manager.take_screenshot(f"TC020_{current_browser}_no_trigger")
            pytest.fail(f"BUG005 confirmed: Cross-browser trigger button not found in {current_browser}")
    
    # ============================================================================
    # MOBILE TESTING
    # ============================================================================
    
    @pytest.mark.critical
    @pytest.mark.mobile
    def test_tc021_mobile_popup_functionality(self):
        """
        TC021: Mobile Popup Functionality
        Manual Result: FAIL - BUG004 (Mobile 0% functionality)
        Expected: Pop-up works on mobile devices
        """
        # Take screenshot before mobile test
        self.test_data_manager.take_screenshot("TC021_mobile_before")
        
        # Validate BUG004: Mobile functionality
        bug_004_results = self.test_data_manager.validate_mobile_functionality(
            self.popup_page, device_type="mobile"
        )
        
        # Test mobile popup functionality
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of mobile popup state
            self.test_data_manager.take_screenshot("TC021_mobile_popup_state")
            
            if popup_appeared:
                # Mobile popup working - bug may be fixed
                self.test_data_manager.take_screenshot("TC021_mobile_success")
                assert True, "Mobile popup functionality working"
            else:
                # BUG004 reproduced - mobile failure
                self.test_data_manager.take_screenshot("TC021_mobile_failure")
                pytest.fail(f"BUG004 reproduced: Mobile popup failed. Details: {bug_004_results}")
        else:
            # Mobile trigger button issue
            self.test_data_manager.take_screenshot("TC021_mobile_no_trigger")
            pytest.fail("BUG004 confirmed: Mobile trigger button not found")
    
    @pytest.mark.critical
    @pytest.mark.mobile
    def test_tc022_tablet_popup_functionality(self):
        """
        TC022: Tablet Popup Functionality
        Manual Result: FAIL - BUG004 (Tablet 0% functionality)
        Expected: Pop-up works on tablet devices
        """
        # Take screenshot before tablet test
        self.test_data_manager.take_screenshot("TC022_tablet_before")
        
        # Validate BUG004: Tablet functionality
        bug_004_results = self.test_data_manager.validate_mobile_functionality(
            self.popup_page, device_type="tablet"
        )
        
        # Test tablet popup functionality
        trigger_success = self.popup_page.click_show_instantly_button()
        
        if trigger_success:
            popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
            
            # Take screenshot of tablet popup state
            self.test_data_manager.take_screenshot("TC022_tablet_popup_state")
            
            if popup_appeared:
                # Tablet popup working - bug may be fixed
                self.test_data_manager.take_screenshot("TC022_tablet_success")
                assert True, "Tablet popup functionality working"
            else:
                # BUG004 reproduced - tablet failure
                self.test_data_manager.take_screenshot("TC022_tablet_failure")
                pytest.fail(f"BUG004 reproduced: Tablet popup failed. Details: {bug_004_results}")
        else:
            # Tablet trigger button issue
            self.test_data_manager.take_screenshot("TC022_tablet_no_trigger")
            pytest.fail("BUG004 confirmed: Tablet trigger button not found")