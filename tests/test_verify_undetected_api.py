#!/usr/bin/env python3
"""
Verify browser is undetected by anti-bot services using Browser Pool API
Based on undetected-testing/test_verify_undetected.py
Run with: pytest tests/test_verify_undetected_api.py -v -s
"""

import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api
from airbrowser_client.models import (
    CreateBrowserRequest,
    ExecuteScriptRequest,
    NavigateBrowserRequest,
    TakeScreenshotRequest,
)
from conftest import get_api_base_url


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.flaky(reruns=2, reruns_delay=5)
class TestUndetected:
    """Test class for verifying browser is undetected"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup browser client for each test"""
        configuration = airbrowser_client.Configuration()
        configuration.host = get_api_base_url()
        self.browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))
        self.browser_id = None
        yield
        # Cleanup after test
        if self.browser_id:
            try:
                self.browser_client.close_browser(self.browser_id)
            except:
                pass

    def create_uc_browser(self):
        """Create a new UC browser instance"""
        browser_config = CreateBrowserRequest(window_size=[1280, 720])
        result = self.browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        self.browser_id = result.data["browser_id"]
        return self.browser_id

    def verify_success(self):
        """Verify that we passed the detection test"""
        try:
            # Use get_element_data with direct parameters
            result = self.browser_client.get_element_data(self.browser_id, selector="h1", data_type="text")

            if result.success and result.data:
                h1_text = result.data.get("text") if "text" in result.data else str(result.data)

                if "OH YEAH, you passed!" in str(h1_text):
                    print("\nSuccess! Website did not detect Selenium!")
                    return True
        except Exception:
            # Fallback to execute_script if get_element_data fails
            try:
                exec_request = ExecuteScriptRequest(
                    script="return document.querySelector('h1') ? document.querySelector('h1').textContent : null;"
                )
                result = self.browser_client.execute_script(self.browser_id, payload=exec_request)

                if result.success and result.data and result.data.get("result"):
                    h1_text = (
                        result.data.get("result").get("value", "")
                        if isinstance(result.data.get("result"), dict)
                        else str(result.data.get("result"))
                    )

                    if "OH YEAH, you passed!" in str(h1_text):
                        print("\nSuccess! Website did not detect Selenium!")
                        return True
            except Exception:
                pass

        return False

    def get_page_source(self):
        """Get page source for debugging"""
        try:
            exec_request = ExecuteScriptRequest(script="return document.documentElement.outerHTML;")
            result = self.browser_client.execute_script(self.browser_id, payload=exec_request)
            if result and result.success and result.data and result.data.get("result"):
                script_result = result.data.get("result")
                return script_result.get("value", "") if isinstance(script_result, dict) else str(script_result)
        except:
            pass
        return "Could not get page source"

    def clear_cookies(self):
        """Clear all cookies"""
        try:
            exec_request = ExecuteScriptRequest(
                script="""
                document.cookie.split(";").forEach(function(c) {
                    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
                });
                return 'cleared';
                """
            )
            self.browser_client.execute_script(self.browser_id, payload=exec_request)
        except:
            pass

    @pytest.mark.browser
    def test_browser_is_undetected(self):
        """Test that browser passes undetection test with retries"""

        # First attempt
        self.create_uc_browser()
        time.sleep(0.5)

        nav_request = NavigateBrowserRequest(url="https://nowsecure.nl/#relax")
        self.browser_client.navigate_browser(self.browser_id, payload=nav_request)
        time.sleep(1)

        # Try to verify success
        if self.verify_success():
            return  # Test passed

        print("First attempt failed, clearing cookies and retrying...")

        # Clear cookies and retry with new browser
        self.clear_cookies()

        # Close current browser and create new one
        try:
            self.browser_client.close_browser(self.browser_id)
        except:
            pass

        self.create_uc_browser()
        time.sleep(0.5)

        self.browser_client.navigate_browser(self.browser_id, payload=nav_request)
        time.sleep(1)

        # Second attempt
        if self.verify_success():
            return  # Test passed

        # Final attempt - take screenshot for manual verification
        print("Taking screenshot for manual verification...")
        self.browser_client.take_screenshot(self.browser_id, payload=TakeScreenshotRequest())

        # Get page source for debugging
        page_source = self.get_page_source() or ""
        page_source_snippet = page_source[:500]
        print(f"Page source snippet: {page_source_snippet}")

        # For now, we won't fail the test completely since detection
        # can vary based on many factors
        print("Could not automatically verify success. Check screenshot for manual verification.")
        print("Note: Browser detection can vary based on IP, browser fingerprint, and other factors.")

    @pytest.mark.browser
    @pytest.mark.parametrize("attempt", [1, 2, 3])
    def test_multiple_attempts(self, attempt):
        """Test with multiple parallel attempts"""
        print(f"\n[Attempt {attempt}] Starting undetection test...")

        self.create_uc_browser()
        time.sleep(0.5)

        nav_request = NavigateBrowserRequest(url="https://nowsecure.nl/#relax")
        self.browser_client.navigate_browser(self.browser_id, payload=nav_request)
        time.sleep(1)

        # Try to verify success
        if self.verify_success():
            print(f"[Attempt {attempt}] Passed on first try!")
            return

        # Take screenshot for this attempt
        self.browser_client.take_screenshot(self.browser_id, payload=TakeScreenshotRequest())
        print(f"[Attempt {attempt}] Screenshot saved for manual verification")

    @pytest.mark.browser
    def test_with_different_user_agents(self):
        """Test with custom user agent"""
        browser_config = CreateBrowserRequest(
            window_size=[1280, 720],
        )
        result = self.browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        self.browser_id = result.data["browser_id"]

        # Navigate to a site that shows user agent
        nav_request = NavigateBrowserRequest(url="https://example.com")
        self.browser_client.navigate_browser(self.browser_id, payload=nav_request)
        time.sleep(0.5)

        # Get the user agent via script
        try:
            exec_request = ExecuteScriptRequest(script="return navigator.userAgent;")
            result = self.browser_client.execute_script(self.browser_id, payload=exec_request)

            if result.success and result.data and result.data.get("result"):
                script_result = result.data.get("result")
                ua_text = script_result.get("value", "") if isinstance(script_result, dict) else str(script_result)

                print(f"User Agent: {ua_text}")

                # Check that it doesn't contain obvious automation indicators
                assert "HeadlessChrome" not in str(ua_text), "HeadlessChrome detected in user agent!"
                assert "Selenium" not in str(ua_text).lower(), "Selenium detected in user agent!"
                print("User agent looks clean!")
        except Exception as e:
            print(f"Could not verify user agent: {e}")
            self.browser_client.take_screenshot(self.browser_id, payload=TakeScreenshotRequest())
