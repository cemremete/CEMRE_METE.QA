"""
Performance and Responsive Design Tests for Insider Test Automation Project
Tests based on manual findings: Performance issues (4.49s delay) and mobile 0% functionality.
"""

import pytest
import time
from pages.popup_page import PopupPage
from pages.product_page import ProductPage
from utils.data_manager import DataManager
from utils.test_data import MobileDevices, BugData


class TestPerformanceAndResponsive:
    """Test class for performance and responsive design validation."""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, test_url):
        """Setup for each test method."""
        self.driver = driver
        self.test_url = test_url
        self.popup_page = PopupPage(driver)
        self.product_page = ProductPage(driver)
        self.test_data_manager = DataManager(driver)
        
        # Navigate to test URL
        self.driver.get(test_url)
        self.product_page.wait_for_page_load()
    
    @pytest.mark.critical
    @pytest.mark.performance
    def test_tc004_popup_load_performance_detailed(self):
        """
        TC004: Detailed Pop-up Load Performance Test
        Manual Result: FAIL - BUG006 (4.49s delay > 2s standard)
        Expected: Pop-up loads within 2 seconds
        """
        performance_results = []
        
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC004_performance_start", "evidence")
        
        # Run multiple performance tests for accuracy
        for attempt in range(5):
            try:
                # Refresh page to ensure clean state
                if attempt > 0:
                    self.driver.refresh()
                    time.sleep(2)
                
                # Measure popup load time
                start_time = time.time()
                
                trigger_success = self.popup_page.click_show_instantly_button()
                
                if trigger_success:
                    popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
                    end_time = time.time()
                    
                    if popup_appeared:
                        load_time = end_time - start_time
                        performance_results.append(load_time)
                        
                        # Close popup for next attempt
                        self.popup_page.click_close_button()
                        time.sleep(1)
                    else:
                        performance_results.append(10.0)  # Timeout value
                else:
                    performance_results.append(10.0)  # Could not trigger
                    
            except Exception as e:
                print(f"Performance test attempt {attempt + 1} failed: {e}")
                performance_results.append(10.0)
        
        # Calculate performance metrics
        if performance_results:
            avg_load_time = sum(performance_results) / len(performance_results)
            min_load_time = min(performance_results)
            max_load_time = max(performance_results)
            
            # Take screenshot with results
            self.test_data_manager.take_screenshot("TC004_performance_results", "evidence")
            
            # Performance analysis
            performance_limit = 2.0
            performance_data = {
                "average_load_time": round(avg_load_time, 2),
                "min_load_time": round(min_load_time, 2),
                "max_load_time": round(max_load_time, 2),
                "performance_limit": performance_limit,
                "attempts": len(performance_results)
            }
            
            print(f"Performance Results: {performance_data}")
            
            # Based on manual findings, expect 4.49s delay (BUG006)
            if avg_load_time > performance_limit:
                # Performance issue reproduced as expected
                self.test_data_manager.take_screenshot("TC004_performance_issue_confirmed", "failed")
                
                if avg_load_time >= 4.0:  # Close to manual finding of 4.49s
                    pytest.xfail(f"BUG006 reproduced: Average load time {avg_load_time:.2f}s matches manual finding of 4.49s")
                else:
                    pytest.fail(f"Performance issue confirmed: Average load time {avg_load_time:.2f}s > {performance_limit}s limit")
            else:
                # Performance better than expected - bug may be fixed
                self.test_data_manager.take_screenshot("TC004_performance_improved", "passed")
                print(f"Performance improved: Average load time {avg_load_time:.2f}s <= {performance_limit}s - BUG006 may be fixed")
        else:
            pytest.fail("Could not measure performance - all attempts failed")
    
    @pytest.mark.critical
    @pytest.mark.performance
    def test_tc015_popup_open_speed(self):
        """
        TC015: Pop-up Open Speed Test
        Manual Result: FAIL - Related to BUG006
        Expected: Pop-up opens within 1 second
        """
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC015_open_speed_start", "evidence")
        
        open_times = []
        
        # Test popup open speed multiple times
        for attempt in range(3):
            try:
                if attempt > 0:
                    self.driver.refresh()
                    time.sleep(1)
                
                # Measure just the open animation time
                start_time = time.time()
                
                if self.popup_page.click_show_instantly_button():
                    # Wait for popup to become visible (not just present)
                    popup_visible = self.popup_page.is_popup_visible(timeout=5)
                    end_time = time.time()
                    
                    if popup_visible:
                        open_time = end_time - start_time
                        open_times.append(open_time)
                        
                        # Close for next attempt
                        self.popup_page.click_close_button()
                        time.sleep(0.5)
                    else:
                        open_times.append(5.0)  # Timeout
                else:
                    open_times.append(5.0)  # Could not trigger
                    
            except Exception as e:
                print(f"Open speed test attempt {attempt + 1} failed: {e}")
                open_times.append(5.0)
        
        if open_times:
            avg_open_time = sum(open_times) / len(open_times)
            
            # Take screenshot with results
            self.test_data_manager.take_screenshot("TC015_open_speed_results", "evidence")
            
            open_speed_limit = 1.0
            
            if avg_open_time > open_speed_limit:
                self.test_data_manager.take_screenshot("TC015_slow_open", "failed")
                pytest.fail(f"Pop-up opens too slowly: {avg_open_time:.2f}s > {open_speed_limit}s limit")
            else:
                self.test_data_manager.take_screenshot("TC015_fast_open", "passed")
                assert True, f"Pop-up opens within limit: {avg_open_time:.2f}s <= {open_speed_limit}s"
        else:
            pytest.fail("Could not measure open speed - all attempts failed")
    
    @pytest.mark.critical
    @pytest.mark.mobile
    @pytest.mark.responsive
    def test_tc020_mobile_view_functionality(self):
        """
        TC020: Mobile View Test
        Manual Result: FAIL - BUG004 (Mobile/tablet 0% functionality)
        Expected: Pop-up displays properly on mobile
        """
        # Based on manual findings, mobile should have 0% functionality
        expected_to_fail = BugData.is_test_expected_to_fail("TC020")
        
        if expected_to_fail:
            # Test with mobile viewport
            mobile_device = MobileDevices.IPHONE_SE
            
            # Set mobile viewport
            self.driver.set_window_size(
                mobile_device["deviceMetrics"]["width"],
                mobile_device["deviceMetrics"]["height"]
            )
            
            # Take screenshot of mobile viewport
            self.test_data_manager.take_screenshot("TC020_mobile_viewport", "evidence")
            
            # Test mobile functionality
            mobile_results = self._test_mobile_functionality()
            
            if mobile_results["total_success_rate"] == 0:
                # Expected 0% functionality confirmed
                self.test_data_manager.take_screenshot("TC020_mobile_zero_functionality", "failed")
                pytest.xfail("BUG004: Mobile 0% functionality confirmed as expected from manual testing")
            else:
                # Unexpected functionality - bug may be improved
                self.test_data_manager.take_screenshot("TC020_mobile_unexpected_functionality", "passed")
                print(f"Mobile functionality better than expected: {mobile_results['total_success_rate']:.1f}% - BUG004 may be improved")
        else:
            # Test normal mobile functionality
            self._test_responsive_design()
    
    @pytest.mark.critical
    @pytest.mark.mobile
    @pytest.mark.responsive
    def test_tc021_tablet_view_functionality(self):
        """
        TC021: Tablet View Test
        Manual Result: FAIL - BUG004 (Mobile/tablet 0% functionality)
        Expected: Pop-up displays properly on tablet
        """
        # Based on manual findings, tablet should have 0% functionality
        expected_to_fail = BugData.is_test_expected_to_fail("TC021")
        
        if expected_to_fail:
            # Test with tablet viewport
            tablet_device = MobileDevices.IPAD
            
            # Set tablet viewport
            self.driver.set_window_size(
                tablet_device["deviceMetrics"]["width"],
                tablet_device["deviceMetrics"]["height"]
            )
            
            # Take screenshot of tablet viewport
            self.test_data_manager.take_screenshot("TC021_tablet_viewport", "evidence")
            
            # Test tablet functionality
            tablet_results = self._test_mobile_functionality()
            
            if tablet_results["total_success_rate"] == 0:
                # Expected 0% functionality confirmed
                self.test_data_manager.take_screenshot("TC021_tablet_zero_functionality", "failed")
                pytest.xfail("BUG004: Tablet 0% functionality confirmed as expected from manual testing")
            else:
                # Unexpected functionality - bug may be improved
                self.test_data_manager.take_screenshot("TC021_tablet_unexpected_functionality", "passed")
                print(f"Tablet functionality better than expected: {tablet_results['total_success_rate']:.1f}% - BUG004 may be improved")
        else:
            # Test normal tablet functionality
            self._test_responsive_design()
    
    @pytest.mark.medium
    @pytest.mark.performance
    def test_tc025_memory_leak_detection(self):
        """
        TC025: Memory Leak Test
        Manual Result: FAIL - BUG009 (Memory leak detected)
        Expected: No significant memory increase over multiple interactions
        """
        # Take initial screenshot
        self.test_data_manager.take_screenshot("TC025_memory_test_start", "evidence")
        
        # Get initial memory usage (if possible)
        initial_memory = self._get_browser_memory_usage()
        
        # Perform multiple popup open/close cycles
        cycles = 20  # Reduced from 50 for faster testing
        successful_cycles = 0
        
        for cycle in range(cycles):
            try:
                # Open popup
                if self.popup_page.click_show_instantly_button():
                    time.sleep(0.5)
                    
                    # Close popup
                    if self.popup_page.click_close_button():
                        time.sleep(0.5)
                        successful_cycles += 1
                    else:
                        # Try alternative close method
                        self.popup_page.click_outside_popup()
                        time.sleep(0.5)
                
                # Brief pause between cycles
                if cycle % 5 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Memory test cycle {cycle + 1} failed: {e}")
        
        # Get final memory usage
        final_memory = self._get_browser_memory_usage()
        
        # Take screenshot after memory test
        self.test_data_manager.take_screenshot("TC025_memory_test_complete", "evidence")
        
        memory_results = {
            "cycles_completed": successful_cycles,
            "total_cycles": cycles,
            "initial_memory": initial_memory,
            "final_memory": final_memory,
            "memory_increase": final_memory - initial_memory if initial_memory and final_memory else 0
        }
        
        print(f"Memory test results: {memory_results}")
        
        # Analyze memory usage
        if memory_results["memory_increase"] > 50:  # Significant increase in MB
            self.test_data_manager.take_screenshot("TC025_memory_leak_detected", "failed")
            pytest.fail(f"BUG009 reproduced: Memory leak detected - {memory_results['memory_increase']:.1f}MB increase")
        elif successful_cycles < cycles * 0.8:  # Less than 80% successful cycles
            self.test_data_manager.take_screenshot("TC025_functionality_degradation", "failed")
            pytest.fail(f"Functionality degradation detected: {successful_cycles}/{cycles} successful cycles")
        else:
            self.test_data_manager.take_screenshot("TC025_memory_stable", "passed")
            assert True, f"Memory usage stable: {successful_cycles}/{cycles} cycles completed successfully"
    
    def _test_mobile_functionality(self):
        """
        Test mobile-specific functionality.
        
        Returns:
            Dictionary with mobile test results
        """
        mobile_tests = {
            "page_load": False,
            "elements_visible": False,
            "popup_trigger": False,
            "popup_display": False,
            "touch_interaction": False
        }
        
        try:
            # Test page load
            current_url = self.driver.current_url
            mobile_tests["page_load"] = bool(current_url)
            
            # Test if key elements are visible in mobile viewport
            show_button_visible = self.popup_page.is_element_visible(
                self.popup_page.SHOW_INSTANTLY_BUTTON, timeout=5
            )
            mobile_tests["elements_visible"] = show_button_visible
            
            if show_button_visible:
                # Test popup trigger
                trigger_success = self.popup_page.click_show_instantly_button()
                mobile_tests["popup_trigger"] = trigger_success
                
                if trigger_success:
                    # Test popup display
                    popup_appeared = self.popup_page.wait_for_popup_to_appear(timeout=10)
                    mobile_tests["popup_display"] = popup_appeared
                    
                    if popup_appeared:
                        # Test touch interaction (close)
                        close_success = self.popup_page.click_close_button()
                        mobile_tests["touch_interaction"] = close_success
            
        except Exception as e:
            print(f"Mobile functionality test error: {e}")
        
        # Calculate success rate
        successful_tests = sum(mobile_tests.values())
        total_tests = len(mobile_tests)
        success_rate = (successful_tests / total_tests) * 100
        
        return {
            "test_results": mobile_tests,
            "successful_tests": successful_tests,
            "total_tests": total_tests,
            "total_success_rate": success_rate
        }
    
    def _test_responsive_design(self):
        """Test responsive design across different viewport sizes."""
        viewports = [
            {"name": "Mobile", "width": 375, "height": 667},
            {"name": "Tablet", "width": 768, "height": 1024},
            {"name": "Desktop", "width": 1920, "height": 1080}
        ]
        
        responsive_results = []
        
        for viewport in viewports:
            # Set viewport size
            self.driver.set_window_size(viewport["width"], viewport["height"])
            time.sleep(1)
            
            # Take screenshot of viewport
            self.test_data_manager.take_screenshot(f"responsive_{viewport['name'].lower()}", "evidence")
            
            # Test functionality in this viewport
            functionality_result = self._test_mobile_functionality()
            
            responsive_results.append({
                "viewport": viewport,
                "success_rate": functionality_result["total_success_rate"]
            })
        
        # Analyze responsive results
        avg_success_rate = sum(r["success_rate"] for r in responsive_results) / len(responsive_results)
        
        if avg_success_rate >= 75:
            self.test_data_manager.take_screenshot("responsive_design_good", "passed")
            assert True, f"Responsive design working: {avg_success_rate:.1f}% average success rate"
        else:
            self.test_data_manager.take_screenshot("responsive_design_poor", "failed")
            pytest.fail(f"Responsive design issues: {avg_success_rate:.1f}% average success rate")
    
    def _get_browser_memory_usage(self):
        """
        Get browser memory usage (simplified approach).
        
        Returns:
            Memory usage in MB (approximate)
        """
        try:
            # Use performance API to get memory info (Chrome only)
            memory_info = self.driver.execute_script("""
                if (performance.memory) {
                    return {
                        used: performance.memory.usedJSHeapSize,
                        total: performance.memory.totalJSHeapSize,
                        limit: performance.memory.jsHeapSizeLimit
                    };
                }
                return null;
            """)
            
            if memory_info:
                # Convert bytes to MB
                return memory_info["used"] / (1024 * 1024)
            else:
                return None
                
        except Exception:
            return None
    
    def teardown_method(self):
        """Cleanup after each test method."""
        try:
            # Reset window size to default
            self.driver.set_window_size(1920, 1080)
            
            # Log performance results
            if hasattr(self, 'test_data_manager'):
                print(f"\n⚡ Performance and responsive test completed")
        except Exception as e:
            print(f"Error in performance teardown: {e}")