"""
Test Data Manager for Insider Test Automation Project
Centralized management of test data, URLs, and configuration values.
Enhanced with reporting, CI/CD, performance, and security testing capabilities.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class TestUrlData:
    """Test URLs configuration."""
    BASE_URL = "https://www.piratesquad.rocks/"
    TEST_URL = "https://piratesquad.rocks/?campBuilderTest=1&insBuild=MTYwODc=&insVar=YzE3MjU=&routeAlias=custom&queryHash=77e2ecf59905618c6426e9aa8cf7407c47293623d7496e3148944c81aeffce95"
    
    # Page URLs
    HOMEPAGE = BASE_URL
    CLOTHES_CATEGORY = f"{BASE_URL}clothes"
    ACCESSORIES_CATEGORY = f"{BASE_URL}accessories"
    ART_CATEGORY = f"{BASE_URL}art"
    CART_PAGE = f"{BASE_URL}cart"
    
    # Product URLs (examples)
    MUG_PRODUCT = f"{BASE_URL}product/mug"


@dataclass
class TestData:
    """Test data constants."""
    
    # Expected content
    EXPECTED_POPUP_CONTENT = "Turkish"
    EXPECTED_PRODUCT_NAME = "Mug"
    
    # Performance limits (in seconds)
    POPUP_LOAD_TIME_LIMIT = 2.0
    POPUP_CLOSE_TIME_LIMIT = 0.5
    PAGE_LOAD_TIME_LIMIT = 5.0
    
    # Browser configurations
    SUPPORTED_BROWSERS = ["chrome", "firefox", "safari"]
    DEFAULT_BROWSER = "chrome"
    
    # Window sizes
    DESKTOP_WINDOW_SIZE = (1920, 1080)
    LAPTOP_WINDOW_SIZE = (1366, 768)
    TABLET_WINDOW_SIZE = (768, 1024)
    MOBILE_WINDOW_SIZE = (375, 667)
    
    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = 10
    LONG_TIMEOUT = 30
    SHORT_TIMEOUT = 5
    
    # Test priorities
    CRITICAL_PRIORITY = "P1"
    HIGH_PRIORITY = "P2"
    MEDIUM_PRIORITY = "P3"
    LOW_PRIORITY = "P4"


class MobileDevices:
    """Mobile device configurations for testing."""
    
    IPHONE_SE = {
        "deviceName": "iPhone SE",
        "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    
    IPHONE_12 = {
        "deviceName": "iPhone 12",
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    
    IPHONE_12_PRO_MAX = {
        "deviceName": "iPhone 12 Pro Max",
        "deviceMetrics": {"width": 428, "height": 926, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    
    IPAD = {
        "deviceName": "iPad",
        "deviceMetrics": {"width": 768, "height": 1024, "pixelRatio": 2.0},
        "userAgent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
    }
    
    SAMSUNG_GALAXY_S21 = {
        "deviceName": "Samsung Galaxy S21",
        "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
    }
    
    @classmethod
    def get_all_devices(cls) -> List[Dict]:
        """Get all mobile device configurations."""
        return [
            cls.IPHONE_SE,
            cls.IPHONE_12,
            cls.IPHONE_12_PRO_MAX,
            cls.IPAD,
            cls.SAMSUNG_GALAXY_S21
        ]
    
    @classmethod
    def get_device_by_name(cls, device_name: str) -> Dict:
        """Get device configuration by name."""
        devices = {
            "iPhone SE": cls.IPHONE_SE,
            "iPhone 12": cls.IPHONE_12,
            "iPhone 12 Pro Max": cls.IPHONE_12_PRO_MAX,
            "iPad": cls.IPAD,
            "Samsung Galaxy S21": cls.SAMSUNG_GALAXY_S21
        }
        return devices.get(device_name, cls.IPHONE_SE)


class TestScenarios:
    """Test scenario data and configurations."""
    
    # Critical test scenarios based on manual findings
    CRITICAL_SCENARIOS = [
        {
            "id": "TC001",
            "title": "Pop-up Display Test",
            "priority": "P1",
            "expected_result": "Pop-up displays successfully",
            "known_issues": ["BUG001", "BUG007"]
        },
        {
            "id": "TC002",
            "title": "Pop-up Close via X Button",
            "priority": "P1",
            "expected_result": "Pop-up closes successfully",
            "known_issues": ["BUG008"]
        },
        {
            "id": "TC023",
            "title": "Add to Cart Functionality",
            "priority": "P1",
            "expected_result": "Product added to cart",
            "known_issues": ["BUG002"]
        }
    ]
    
    # Performance test scenarios
    PERFORMANCE_SCENARIOS = [
        {
            "id": "TC004",
            "title": "Pop-up Load Performance",
            "priority": "P1",
            "time_limit": 2.0,
            "known_issues": ["BUG006"]
        },
        {
            "id": "TC015",
            "title": "Pop-up Open Speed",
            "priority": "P2",
            "time_limit": 1.0,
            "known_issues": ["BUG006"]
        }
    ]
    
    # Cross-browser test scenarios
    BROWSER_SCENARIOS = [
        {
            "id": "TC017",
            "title": "Chrome Browser Test",
            "browser": "chrome",
            "priority": "P1",
            "known_issues": ["BUG001", "BUG002"]
        },
        {
            "id": "TC018",
            "title": "Firefox Browser Test",
            "browser": "firefox",
            "priority": "P1",
            "known_issues": ["BUG005"]
        },
        {
            "id": "TC019",
            "title": "Safari Browser Test",
            "browser": "safari",
            "priority": "P1",
            "known_issues": ["BUG005"]
        }
    ]


class BugData:
    """Known bug data for test validation."""
    
    CRITICAL_BUGS = {
        "BUG001": {
            "title": "Production Blocker - URL Parameter Dependency",
            "severity": "Critical",
            "priority": "P1",
            "description": "System only works with specific URL parameters",
            "affected_tests": ["TC001", "TC017", "TC018", "TC019"]
        },
        "BUG002": {
            "title": "Add to Cart Button Not Working",
            "severity": "Critical",
            "priority": "P1",
            "description": "Add to Cart functionality completely broken",
            "affected_tests": ["TC023"]
        },
        "BUG003": {
            "title": "Price Update Error",
            "severity": "Critical",
            "priority": "P1",
            "description": "Discounts not reflecting correctly",
            "affected_tests": ["TC024"]
        },
        "BUG004": {
            "title": "Mobile/Tablet 0% Functionality",
            "severity": "Critical",
            "priority": "P1",
            "description": "Complete failure on mobile devices",
            "affected_tests": ["TC020", "TC021"]
        },
        "BUG005": {
            "title": "Firefox/Safari Complete Failure",
            "severity": "Critical",
            "priority": "P1",
            "description": "Cross-browser compatibility broken",
            "affected_tests": ["TC018", "TC019"]
        },
        "BUG006": {
            "title": "Performance Critical - 4.49s Delay",
            "severity": "High",
            "priority": "P2",
            "description": "Load time exceeds 2-second standard",
            "affected_tests": ["TC004", "TC015"]
        },
        "BUG007": {
            "title": "Content Critical - 90% Incorrect Product Mapping",
            "severity": "Critical",
            "priority": "P1",
            "description": "Wrong products shown in pop-up",
            "affected_tests": ["TC010", "TC005"]
        },
        "BUG008": {
            "title": "UX Critical - Pop-up Close Buttons Not Working",
            "severity": "High",
            "priority": "P2",
            "description": "Close functionality non-responsive",
            "affected_tests": ["TC002", "TC003"]
        },
        "BUG009": {
            "title": "Memory Critical - Memory Leak Detected",
            "severity": "High",
            "priority": "P2",
            "description": "Memory usage increases over time",
            "affected_tests": ["TC025"]
        },
        "BUG010": {
            "title": "Overlay Critical - Background Overlay Missing",
            "severity": "High",
            "priority": "P2",
            "description": "No background overlay for pop-up",
            "affected_tests": ["TC014"]
        }
    }
    
    @classmethod
    def get_bugs_for_test(cls, test_id: str) -> List[str]:
        """Get list of known bugs affecting a specific test."""
        affecting_bugs = []
        for bug_id, bug_info in cls.CRITICAL_BUGS.items():
            if test_id in bug_info.get("affected_tests", []):
                affecting_bugs.append(bug_id)
        return affecting_bugs
    
    @classmethod
    def is_test_expected_to_fail(cls, test_id: str) -> bool:
        """Check if a test is expected to fail due to known bugs."""
        return len(cls.get_bugs_for_test(test_id)) > 0


class EnvironmentConfig:
    """Environment-specific configuration."""
    
    def __init__(self):
        self.environment = os.getenv("TEST_ENV", "test").lower()
        self.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.browser = os.getenv("BROWSER", "chrome").lower()
        self.parallel = os.getenv("PARALLEL", "false").lower() == "true"
        self.screenshot_on_failure = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
        self.screenshot_on_success = os.getenv("SCREENSHOT_ON_SUCCESS", "false").lower() == "true"
    
    def get_base_url(self) -> str:
        """Get base URL based on environment."""
        urls = {
            "dev": "https://dev.piratesquad.rocks/",
            "test": "https://test.piratesquad.rocks/",
            "staging": "https://staging.piratesquad.rocks/",
            "prod": "https://www.piratesquad.rocks/"
        }
        return urls.get(self.environment, TestUrlData.BASE_URL)
    
    def get_test_url(self) -> str:
        """Get test URL with parameters based on environment."""
        base_url = self.get_base_url()
        if self.environment == "test":
            return TestUrlData.TEST_URL
        else:
            # For other environments, might need different parameters
            return TestUrlData.TEST_URL.replace("piratesquad.rocks", base_url.split("//")[1].rstrip("/"))


# ============================================================================
# 1. TEST REPORTING & ANALYTICS
# ============================================================================

class TestReportingConfig:
    """Configuration for test reporting and analytics."""
    
    # Report formats
    REPORT_FORMATS = ["html", "json", "xml", "allure"]
    DEFAULT_FORMAT = "html"
    
    # Report locations
    REPORT_DIR = "reports"
    HTML_REPORT_DIR = f"{REPORT_DIR}/html"
    JSON_REPORT_DIR = f"{REPORT_DIR}/json"
    ALLURE_REPORT_DIR = f"{REPORT_DIR}/allure"
    
    # Analytics metrics
    METRICS_TO_TRACK = [
        "test_execution_time",
        "bug_reproduction_rate",
        "test_coverage_percentage",
        "performance_metrics",
        "browser_compatibility_score"
    ]
    
    # Dashboard configuration
    DASHBOARD_REFRESH_INTERVAL = 300  # 5 minutes
    RETENTION_PERIOD_DAYS = 30


class TestAnalytics:
    """Test analytics and metrics collection."""
    
    def __init__(self):
        self.execution_metrics = {}
        self.performance_data = {}
        self.bug_trends = {}
        self.coverage_data = {}
    
    def collect_execution_metrics(self, test_result: Dict) -> None:
        """Collect test execution metrics."""
        test_id = test_result.get("test_id")
        if test_id:
            self.execution_metrics[test_id] = {
                "status": test_result.get("status"),
                "execution_time": test_result.get("execution_time"),
                "browser": test_result.get("browser"),
                "timestamp": datetime.now().isoformat()
            }
    
    def calculate_bug_reproduction_rate(self) -> float:
        """Calculate bug reproduction rate."""
        total_bugs = len(self.bug_trends)
        reproduced_bugs = sum(1 for bug in self.bug_trends.values() if bug.get("reproduced"))
        return (reproduced_bugs / total_bugs * 100) if total_bugs > 0 else 0.0
    
    def generate_analytics_report(self) -> Dict:
        """Generate comprehensive analytics report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.execution_metrics),
            "bug_reproduction_rate": self.calculate_bug_reproduction_rate(),
            "performance_summary": self.performance_data,
            "coverage_summary": self.coverage_data
        }


# ============================================================================
# 2. CI/CD INTEGRATION
# ============================================================================

class CICDConfig:
    """CI/CD pipeline configuration."""
    
    # Pipeline triggers
    TRIGGERS = ["push", "pull_request", "manual", "scheduled"]
    
    # Environment mapping
    ENVIRONMENT_MAPPING = {
        "main": "production",
        "develop": "staging",
        "feature/*": "test",
        "hotfix/*": "staging"
    }
    
    # Notification channels
    NOTIFICATION_CHANNELS = ["email", "slack", "teams", "webhook"]
    
    # Pipeline stages
    PIPELINE_STAGES = [
        "code_analysis",
        "unit_tests",
        "integration_tests",
        "ui_tests",
        "performance_tests",
        "security_tests",
        "deployment"
    ]


class PipelineExecutor:
    """CI/CD pipeline execution management."""
    
    def __init__(self):
        self.current_stage = None
        self.stage_results = {}
        self.pipeline_status = "pending"
    
    def execute_stage(self, stage_name: str) -> bool:
        """Execute a specific pipeline stage."""
        self.current_stage = stage_name
        try:
            # Stage execution logic here
            self.stage_results[stage_name] = "success"
            return True
        except Exception as e:
            self.stage_results[stage_name] = f"failed: {str(e)}"
            return False
    
    def get_pipeline_status(self) -> Dict:
        """Get current pipeline status."""
        return {
            "status": self.pipeline_status,
            "current_stage": self.current_stage,
            "stage_results": self.stage_results,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# 3. TEST DATA MANAGEMENT
# ============================================================================

class TestDataManager:
    """Central manager for all test data."""
    
    def __init__(self):
        self.urls = TestUrlData()
        self.data = TestData()
        self.mobile_devices = MobileDevices()
        self.scenarios = TestScenarios()
        self.bugs = BugData()
        self.env_config = EnvironmentConfig()
        self.analytics = TestAnalytics()
        self.pipeline = PipelineExecutor()
    
    def get_test_data_for_scenario(self, scenario_id: str) -> Dict:
        """Get comprehensive test data for a specific scenario."""
        # Find scenario in different categories
        scenario = None
        for scenario_list in [
            self.scenarios.CRITICAL_SCENARIOS,
            self.scenarios.PERFORMANCE_SCENARIOS,
            self.scenarios.BROWSER_SCENARIOS
        ]:
            for s in scenario_list:
                if s["id"] == scenario_id:
                    scenario = s
                    break
            if scenario:
                break
        
        if not scenario:
            return {}
        
        # Get known bugs for this scenario
        known_bugs = self.bugs.get_bugs_for_test(scenario_id)
        expected_to_fail = self.bugs.is_test_expected_to_fail(scenario_id)
        
        return {
            "scenario": scenario,
            "known_bugs": known_bugs,
            "expected_to_fail": expected_to_fail,
            "test_url": self.env_config.get_test_url(),
            "base_url": self.env_config.get_base_url(),
            "timeouts": {
                "default": self.data.DEFAULT_TIMEOUT,
                "long": self.data.LONG_TIMEOUT,
                "short": self.data.SHORT_TIMEOUT
            },
            "performance_limits": {
                "popup_load": self.data.POPUP_LOAD_TIME_LIMIT,
                "popup_close": self.data.POPUP_CLOSE_TIME_LIMIT,
                "page_load": self.data.PAGE_LOAD_TIME_LIMIT
            }
        }
    
    def get_mobile_test_data(self) -> List[Dict]:
        """Get test data for mobile testing."""
        return self.mobile_devices.get_all_devices()
    
    def get_browser_test_data(self) -> List[str]:
        """Get list of browsers for cross-browser testing."""
        return self.data.SUPPORTED_BROWSERS
    
    def should_skip_test(self, test_id: str, browser: str = None) -> Tuple[bool, str]:
        """
        Determine if a test should be skipped based on known issues.
        
        Returns:
            Tuple of (should_skip, reason)
        """
        known_bugs = self.bugs.get_bugs_for_test(test_id)
        
        if not known_bugs:
            return False, ""
        
        # Check for browser-specific issues
        if browser:
            browser_specific_bugs = {
                "firefox": ["BUG005"],
                "safari": ["BUG005"],
                "mobile": ["BUG004"]
            }
            
            if any(bug in browser_specific_bugs.get(browser, []) for bug in known_bugs):
                return True, f"Known {browser} compatibility issue: {', '.join(known_bugs)}"
        
        # Check for critical bugs that make test impossible
        critical_blocking_bugs = ["BUG001", "BUG004", "BUG005"]
        if any(bug in critical_blocking_bugs for bug in known_bugs):
            return True, f"Critical blocking bug: {', '.join(known_bugs)}"
        
        return False, ""


# ============================================================================
# 4. PERFORMANCE TESTING
# ============================================================================

class PerformanceTestConfig:
    """Configuration for performance testing."""
    
    # Load testing parameters
    LOAD_TEST_USERS = [1, 5, 10, 25, 50, 100]
    RAMP_UP_TIME = 60  # seconds
    HOLD_TIME = 300  # seconds
    RAMP_DOWN_TIME = 60  # seconds
    
    # Performance thresholds
    RESPONSE_TIME_THRESHOLDS = {
        "excellent": 1.0,    # < 1 second
        "good": 2.0,         # < 2 seconds
        "acceptable": 5.0,    # < 5 seconds
        "poor": 10.0,        # < 10 seconds
        "unacceptable": 10.0  # > 10 seconds
    }
    
    # Memory usage thresholds
    MEMORY_THRESHOLDS = {
        "low": 100,      # < 100 MB
        "medium": 500,   # < 500 MB
        "high": 1000,    # < 1 GB
        "critical": 1000  # > 1 GB
    }


class PerformanceMetrics:
    """Performance metrics collection and analysis."""
    
    def __init__(self):
        self.response_times = []
        self.memory_usage = []
        self.cpu_usage = []
        self.throughput = []
        self.error_rates = []
    
    def add_response_time(self, response_time: float) -> None:
        """Add response time measurement."""
        self.response_times.append(response_time)
    
    def get_average_response_time(self) -> float:
        """Calculate average response time."""
        return sum(self.response_times) / len(self.response_times) if self.response_times else 0.0
    
    def get_percentile_response_time(self, percentile: int) -> float:
        """Get response time at specific percentile."""
        if not self.response_times:
            return 0.0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * percentile / 100)
        return sorted_times[index]
    
    def analyze_performance(self) -> Dict:
        """Analyze performance metrics."""
        return {
            "total_requests": len(self.response_times),
            "average_response_time": self.get_average_response_time(),
            "p50_response_time": self.get_percentile_response_time(50),
            "p90_response_time": self.get_percentile_response_time(90),
            "p95_response_time": self.get_percentile_response_time(95),
            "p99_response_time": self.get_percentile_response_time(99),
            "min_response_time": min(self.response_times) if self.response_times else 0.0,
            "max_response_time": max(self.response_times) if self.response_times else 0.0
        }


# ============================================================================
# 5. SECURITY TESTING
# ============================================================================

class SecurityTestConfig:
    """Configuration for security testing."""
    
    # OWASP Top 10 categories
    OWASP_CATEGORIES = [
        "injection",
        "broken_authentication",
        "sensitive_data_exposure",
        "xml_external_entities",
        "broken_access_control",
        "security_misconfiguration",
        "cross_site_scripting",
        "insecure_deserialization",
        "using_components_with_known_vulnerabilities",
        "insufficient_logging_and_monitoring"
    ]
    
    # Security test types
    SECURITY_TEST_TYPES = [
        "authentication_testing",
        "authorization_testing",
        "input_validation_testing",
        "session_management_testing",
        "encryption_testing",
        "api_security_testing"
    ]
    
    # Security headers to check
    SECURITY_HEADERS = [
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Referrer-Policy"
    ]


class SecurityTestData:
    """Security testing data and payloads."""
    
    # SQL Injection payloads
    SQL_INJECTION_PAYLOADS = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --",
        "admin'--",
        "1' OR '1' = '1' --"
    ]
    
    # XSS payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>",
        "';alert('XSS');//"
    ]
    
    # Authentication bypass payloads
    AUTH_BYPASS_PAYLOADS = [
        "admin:admin",
        "admin:password",
        "user:user",
        "test:test",
        "guest:guest"
    ]
    
    # File upload test files
    FILE_UPLOAD_TESTS = [
        "test.txt",
        "test.php",
        "test.jsp",
        "test.asp",
        "test.exe",
        "test.sh"
    ]


class SecurityTestManager:
    """Security testing execution and validation."""
    
    def __init__(self):
        self.security_config = SecurityTestConfig()
        self.test_data = SecurityTestData()
        self.test_results = {}
    
    def run_owasp_tests(self) -> Dict:
        """Run OWASP Top 10 security tests."""
        results = {}
        for category in self.security_config.OWASP_CATEGORIES:
            results[category] = self._test_owasp_category(category)
        return results
    
    def _test_owasp_category(self, category: str) -> Dict:
        """Test specific OWASP category."""
        # Implementation for each OWASP category
        return {
            "category": category,
            "status": "pending",
            "vulnerabilities_found": 0,
            "risk_level": "medium",
            "recommendations": []
        }
    
    def validate_security_headers(self, headers: Dict) -> Dict:
        """Validate security headers in response."""
        validation_results = {}
        for header in self.security_config.SECURITY_HEADERS:
            validation_results[header] = {
                "present": header in headers,
                "value": headers.get(header, "missing"),
                "secure": self._is_header_secure(header, headers.get(header, ""))
            }
        return validation_results
    
    def _is_header_secure(self, header: str, value: str) -> bool:
        """Check if security header value is secure."""
        # Implementation for header security validation
        return True  # Placeholder