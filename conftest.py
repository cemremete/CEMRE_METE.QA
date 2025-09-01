"""
Pytest configuration file for Insider Test Automation Project
Contains fixtures, setup/teardown methods, and global test configurations.
"""

import pytest
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


# Test Configuration
TEST_URL = "https://piratesquad.rocks/?campBuilderTest=1&insBuild=MTYwODc=&insVar=YzE3MjU=&routeAlias=custom&queryHash=77e2ecf59905618c6426e9aa8cf7407c47293623d7496e3148944c81aeffce95"
BASE_URL = "https://www.piratesquad.rocks/"
SCREENSHOT_DIR = "screenshots"
FAILED_SCREENSHOT_DIR = os.path.join(SCREENSHOT_DIR, "failed")
PASSED_SCREENSHOT_DIR = os.path.join(SCREENSHOT_DIR, "passed")

# Create screenshot directories
os.makedirs(FAILED_SCREENSHOT_DIR, exist_ok=True)
os.makedirs(PASSED_SCREENSHOT_DIR, exist_ok=True)


def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, safari"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920,1080",
        help="Browser window size (width,height)"
    )


@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line option."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Get headless mode setting from command line option."""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def window_size(request):
    """Get window size from command line option."""
    size = request.config.getoption("--window-size")
    width, height = size.split(",")
    return int(width), int(height)


@pytest.fixture(scope="function")
def driver(request, browser_name, headless_mode, window_size):
    """
    WebDriver fixture that provides browser instance for each test.
    Supports Chrome, Firefox, and Safari browsers.
    """
    driver_instance = None
    
    try:
        if browser_name.lower() == "chrome":
            driver_instance = _get_chrome_driver(headless_mode, window_size)
        elif browser_name.lower() == "firefox":
            driver_instance = _get_firefox_driver(headless_mode, window_size)
        elif browser_name.lower() == "safari":
            driver_instance = _get_safari_driver(window_size)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Set implicit wait
        driver_instance.implicitly_wait(10)
        
        # Store driver info for reporting
        request.node.driver_info = {
            "browser": browser_name,
            "headless": headless_mode,
            "window_size": window_size
        }
        
        yield driver_instance
        
    except Exception as e:
        pytest.fail(f"Failed to initialize {browser_name} driver: {str(e)}")
    
    finally:
        if driver_instance:
            driver_instance.quit()


def _get_chrome_driver(headless_mode, window_size):
    """Initialize Chrome WebDriver with options."""
    chrome_options = ChromeOptions()
    
    if headless_mode:
        chrome_options.add_argument("--headless")
    
    # Chrome-specific options for better stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    
    # Performance optimizations
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    service = ChromeService(r"C:\Users\cemre\Documents\chromedriver\chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)


def _get_firefox_driver(headless_mode, window_size):
    """Initialize Firefox WebDriver with options."""
    firefox_options = FirefoxOptions()
    
    if headless_mode:
        firefox_options.add_argument("--headless")
    
    # Firefox-specific options
    firefox_options.add_argument(f"--width={window_size[0]}")
    firefox_options.add_argument(f"--height={window_size[1]}")
    
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=firefox_options)


def _get_safari_driver(window_size):
    """Initialize Safari WebDriver."""
    # Note: Safari doesn't support headless mode
    driver = webdriver.Safari()
    driver.set_window_size(window_size[0], window_size[1])
    return driver


@pytest.fixture(scope="function")
def test_url():
    """Provide the test URL for tests."""
    return TEST_URL


@pytest.fixture(scope="function")
def base_url():
    """Provide the base URL for tests."""
    return BASE_URL


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture screenshots for test calls (not setup/teardown)
    if call.when == "call":
        driver = getattr(item.funcargs.get('driver'), 'driver', item.funcargs.get('driver'))
        
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if report.failed:
                # Take screenshot on failure
                screenshot_name = f"FAILED_{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(FAILED_SCREENSHOT_DIR, screenshot_name)
                
                try:
                    driver.save_screenshot(screenshot_path)
                    print(f"\n[SUCCESS] Screenshot saved: {screenshot_path}")
                    
                    # Add screenshot path to report for HTML reporting
                    if hasattr(report, 'extra'):
                        report.extra.append({
                            'name': 'Screenshot',
                            'path': screenshot_path,
                            'content_type': 'image/png'
                        })
                    
                except Exception as e:
                    print(f"\n[ERROR] Failed to take screenshot: {str(e)}")
            
            elif report.passed:
                # Optionally take screenshot on success (for documentation)
                screenshot_name = f"PASSED_{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(PASSED_SCREENSHOT_DIR, screenshot_name)
                
                try:
                    driver.save_screenshot(screenshot_path)
                    print(f"\n[SUCCESS] Success screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"\n[WARNING] Failed to take success screenshot: {str(e)}")


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical priority"
    )
    config.addinivalue_line(
        "markers", "high: mark test as high priority"
    )
    config.addinivalue_line(
        "markers", "medium: mark test as medium priority"
    )
    config.addinivalue_line(
        "markers", "low: mark test as low priority"
    )
    config.addinivalue_line(
        "markers", "browser_chrome: run test only on Chrome"
    )
    config.addinivalue_line(
        "markers", "browser_firefox: run test only on Firefox"
    )
    config.addinivalue_line(
        "markers", "browser_safari: run test only on Safari"
    )
    config.addinivalue_line(
        "markers", "mobile: mark test for mobile testing"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "cross_browser: cross-browser compatibility tests"
    )
    config.addinivalue_line(
        "markers", "responsive: responsive design tests"
    )
    config.addinivalue_line(
        "markers", "browser: general browser tests"
    )
    config.addinivalue_line(
        "markers", "tablet: tablet device tests"
    )
    config.addinivalue_line(
        "markers", "ui: user interface tests"
    )
    config.addinivalue_line(
        "markers", "functional: functional tests"
    )
    config.addinivalue_line(
        "markers", "negative: negative test cases"
    )
    config.addinivalue_line(
        "markers", "edge_case: edge case scenarios"
    )
    config.addinivalue_line(
        "markers", "accessibility: accessibility tests"
    )
    config.addinivalue_line(
        "markers", "memory: memory leak tests"
    )
    config.addinivalue_line(
        "markers", "slow: tests that take longer than 30 seconds"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add browser-specific markers
        if "chrome" in item.name.lower():
            item.add_marker(pytest.mark.browser_chrome)
        if "firefox" in item.name.lower():
            item.add_marker(pytest.mark.browser_firefox)
        if "safari" in item.name.lower():
            item.add_marker(pytest.mark.browser_safari)
        
        # Add priority markers based on test file or name
        if "critical" in item.name.lower() or "p1" in item.name.lower():
            item.add_marker(pytest.mark.critical)
        elif "high" in item.name.lower() or "p2" in item.name.lower():
            item.add_marker(pytest.mark.high)
        elif "performance" in item.name.lower():
            item.add_marker(pytest.mark.performance)


@pytest.fixture(scope="function")
def performance_timer():
    """Fixture to measure test execution time."""
    start_time = time.time()
    yield
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\n[TIMER] Test execution time: {execution_time:.2f} seconds")


# Custom assertion helpers
def assert_popup_visible(popup_page, timeout=10):
    """Custom assertion for popup visibility."""
    assert popup_page.is_popup_visible(timeout), "Pop-up should be visible but is not"


def assert_popup_not_visible(popup_page, timeout=10):
    """Custom assertion for popup not being visible."""
    assert not popup_page.is_popup_visible(timeout), "Pop-up should not be visible but is"


def assert_performance_within_limit(actual_time, limit_seconds, operation_name):
    """Custom assertion for performance testing."""
    assert actual_time <= limit_seconds, f"{operation_name} took {actual_time:.2f}s, should be <= {limit_seconds}s"


# Test data fixtures
@pytest.fixture(scope="session")
def test_data():
    """Provide test data for tests."""
    return {
        "expected_popup_content": "Turkish",
        "expected_product_name": "Mug",
        "performance_limits": {
            "popup_load_time": 2.0,
            "popup_close_time": 0.5
        },
        "browser_list": ["chrome", "firefox", "safari"],
        "mobile_viewports": [
            {"width": 375, "height": 667},  # iPhone SE
            {"width": 414, "height": 896},  # iPhone 11 Pro Max
            {"width": 768, "height": 1024}  # iPad
        ]
    }