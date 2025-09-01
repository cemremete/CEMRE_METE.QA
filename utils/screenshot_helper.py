"""
Screenshot Helper for Insider Test Automation Project
Handles automatic screenshot capture for test documentation and failure analysis.
"""

import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


class ScreenshotHelper:
    """Helper class for managing screenshots during test execution."""
    
    def __init__(self, driver, base_dir="screenshots"):
        """
        Initialize ScreenshotHelper.
        
        Args:
            driver: WebDriver instance
            base_dir: Base directory for storing screenshots
        """
        self.driver = driver
        self.base_dir = base_dir
        self.failed_dir = os.path.join(base_dir, "failed")
        self.passed_dir = os.path.join(base_dir, "passed")
        self.evidence_dir = os.path.join(base_dir, "evidence")
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create screenshot directories if they don't exist."""
        directories = [self.base_dir, self.failed_dir, self.passed_dir, self.evidence_dir]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def take_screenshot(self, test_name, status="evidence", description=""):
        """
        Take a screenshot with automatic naming and organization.
        
        Args:
            test_name: Name of the test
            status: Screenshot status ('failed', 'passed', 'evidence')
            description: Optional description for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
        
        # Clean test name for filename
        clean_test_name = self._clean_filename(test_name)
        
        # Determine directory based on status
        if status == "failed":
            directory = self.failed_dir
            prefix = "FAILED"
        elif status == "passed":
            directory = self.passed_dir
            prefix = "PASSED"
        else:
            directory = self.evidence_dir
            prefix = "EVIDENCE"
        
        # Create filename
        if description:
            clean_description = self._clean_filename(description)
            filename = f"{prefix}_{clean_test_name}_{clean_description}_{timestamp}.png"
        else:
            filename = f"{prefix}_{clean_test_name}_{timestamp}.png"
        
        filepath = os.path.join(directory, filename)
        
        try:
            # Take screenshot
            self.driver.save_screenshot(filepath)
            
            # Add metadata to screenshot if needed
            if status == "failed":
                self._add_failure_metadata(filepath, test_name, description)
            
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to take screenshot: {str(e)}")
            return None
    
    def take_failure_screenshot(self, test_name, error_message=""):
        """
        Take a screenshot specifically for test failures.
        
        Args:
            test_name: Name of the failed test
            error_message: Error message from the failure
            
        Returns:
            Path to the saved screenshot
        """
        return self.take_screenshot(test_name, "failed", error_message)
    
    def take_success_screenshot(self, test_name, step_description=""):
        """
        Take a screenshot for successful test completion.
        
        Args:
            test_name: Name of the successful test
            step_description: Description of the successful step
            
        Returns:
            Path to the saved screenshot
        """
        return self.take_screenshot(test_name, "passed", step_description)
    
    def take_evidence_screenshot(self, test_name, step_description):
        """
        Take a screenshot for test evidence/documentation.
        
        Args:
            test_name: Name of the test
            step_description: Description of the current step
            
        Returns:
            Path to the saved screenshot
        """
        return self.take_screenshot(test_name, "evidence", step_description)
    
    def take_comparison_screenshots(self, test_name, before_action, after_action):
        """
        Take before and after screenshots for comparison.
        
        Args:
            test_name: Name of the test
            before_action: Description of the before state
            after_action: Description of the after state
            
        Returns:
            Tuple of (before_screenshot_path, after_screenshot_path)
        """
        before_path = self.take_evidence_screenshot(test_name, f"BEFORE_{before_action}")
        
        # Small delay to ensure different timestamps
        time.sleep(0.1)
        
        after_path = self.take_evidence_screenshot(test_name, f"AFTER_{after_action}")
        
        return before_path, after_path
    
    def take_popup_lifecycle_screenshots(self, test_name):
        """
        Take screenshots of the complete popup lifecycle.
        
        Args:
            test_name: Name of the test
            
        Returns:
            Dictionary with screenshot paths for each stage
        """
        screenshots = {}
        
        # Before popup
        screenshots['before_popup'] = self.take_evidence_screenshot(
            test_name, "before_popup_trigger"
        )
        
        return screenshots
    
    def capture_popup_states(self, test_name, popup_page):
        """
        Capture screenshots of different popup states.
        
        Args:
            test_name: Name of the test
            popup_page: PopupPage instance
            
        Returns:
            Dictionary with screenshot paths
        """
        screenshots = {}
        
        # Initial state
        screenshots['initial'] = self.take_evidence_screenshot(test_name, "initial_state")
        
        # Trigger popup
        if popup_page.click_show_instantly_button():
            time.sleep(1)  # Wait for popup animation
            screenshots['popup_open'] = self.take_evidence_screenshot(test_name, "popup_opened")
            
            # Try to close popup
            if popup_page.click_close_button():
                time.sleep(1)  # Wait for close animation
                screenshots['popup_closed'] = self.take_evidence_screenshot(test_name, "popup_closed")
        
        return screenshots
    
    def _clean_filename(self, filename):
        """
        Clean filename by removing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Cleaned filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename
    
    def _add_failure_metadata(self, screenshot_path, test_name, error_message):
        """
        Add metadata overlay to failure screenshots.
        
        Args:
            screenshot_path: Path to the screenshot
            test_name: Name of the test
            error_message: Error message to overlay
        """
        try:
            # Open the screenshot
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)
            
            # Try to use a default font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Add red border to indicate failure
            width, height = image.size
            border_width = 5
            draw.rectangle([0, 0, width-1, height-1], outline="red", width=border_width)
            
            # Add failure information overlay
            overlay_height = 80
            overlay = Image.new('RGBA', (width, overlay_height), (255, 0, 0, 180))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add text to overlay
            overlay_draw.text((10, 10), f"FAILED: {test_name}", fill="white", font=font)
            overlay_draw.text((10, 30), f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                            fill="white", font=font)
            
            if error_message:
                # Truncate long error messages
                if len(error_message) > 80:
                    error_message = error_message[:77] + "..."
                overlay_draw.text((10, 50), f"Error: {error_message}", fill="white", font=font)
            
            # Paste overlay onto image
            image.paste(overlay, (0, 0), overlay)
            
            # Save the modified image
            image.save(screenshot_path)
            
        except Exception as e:
            print(f"⚠️ Failed to add metadata to screenshot: {str(e)}")
    
    def create_screenshot_report(self, test_results):
        """
        Create an HTML report with all screenshots.
        
        Args:
            test_results: Dictionary with test results and screenshot paths
            
        Returns:
            Path to the HTML report
        """
        report_path = os.path.join(self.base_dir, "screenshot_report.html")
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Screenshots Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .test-section { margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; }
                .test-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                .screenshot { margin: 10px 0; }
                .screenshot img { max-width: 300px; border: 1px solid #ccc; }
                .failed { border-left: 5px solid red; }
                .passed { border-left: 5px solid green; }
                .evidence { border-left: 5px solid blue; }
            </style>
        </head>
        <body>
            <h1>Test Screenshots Report</h1>
            <p>Generated on: {timestamp}</p>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for test_name, results in test_results.items():
            status_class = results.get('status', 'evidence')
            html_content += f"""
            <div class="test-section {status_class}">
                <div class="test-title">{test_name}</div>
            """
            
            for screenshot_path in results.get('screenshots', []):
                if os.path.exists(screenshot_path):
                    rel_path = os.path.relpath(screenshot_path, self.base_dir)
                    html_content += f"""
                    <div class="screenshot">
                        <img src="{rel_path}" alt="Screenshot for {test_name}">
                        <p>{os.path.basename(screenshot_path)}</p>
                    </div>
                    """
            
            html_content += "</div>"
        
        html_content += """
        </body>
        </html>
        """
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"📊 Screenshot report created: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Failed to create screenshot report: {str(e)}")
            return None
    
    def cleanup_old_screenshots(self, days_old=7):
        """
        Clean up screenshots older than specified days.
        
        Args:
            days_old: Number of days after which to delete screenshots
        """
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.png'):
                    file_path = os.path.join(root, file)
                    if os.path.getmtime(file_path) < cutoff_time:
                        try:
                            os.remove(file_path)
                            print(f"🗑️ Deleted old screenshot: {file_path}")
                        except Exception as e:
                            print(f"❌ Failed to delete {file_path}: {str(e)}")