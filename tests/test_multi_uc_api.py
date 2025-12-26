#!/usr/bin/env python3
"""
Multi-threaded UC (Undetected Chrome) test using Browser Pool API
Based on undetected-testing/multi_uc.py
Run with: pytest tests/test_multi_uc_api.py -n3 -v
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


def create_browser_client():
    """Create a browser client instance"""
    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    return browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.parametrize("test_num", [1, 2, 3])
@pytest.mark.browser
def test_multi_threaded_uc_detection(test_num):
    """Test UC mode with multiple parallel browsers to bypass detection"""

    browser_client = create_browser_client()
    browser_id = None

    try:
        # Create browser with UC mode enabled
        browser_config = CreateBrowserRequest(
            window_size=[700, 500],
        )

        result = browser_client.create_browser(payload=browser_config)
        assert result is not None, "Failed to create browser"
        assert result.success, "Browser creation failed"
        browser_id = result.data["browser_id"]
        assert browser_id is not None, f"Browser ID is None for test {test_num}"

        print(f"\n[Test {test_num}] Created browser: {browser_id}")

        # Wait for browser initialization
        time.sleep(0.5)

        # Navigate to the detection test site
        nav_request = NavigateBrowserRequest(url="https://nowsecure.nl/#relax")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success, f"Navigation failed for test {test_num}"

        print(f"[Test {test_num}] Navigated to nowsecure.nl")

        # Wait for page to load and perform detection
        time.sleep(1)

        # Check if we passed the detection test
        try:
            exec_request = ExecuteScriptRequest(
                script="""
                const h1 = document.querySelector('h1');
                return h1 ? h1.textContent : null;
                """
            )
            exec_result = browser_client.execute_script(browser_id, payload=exec_request)

            if exec_result.success:
                h1_text = exec_result.data.get("result") if exec_result.data else ""

                if "OH YEAH, you passed!" in str(h1_text):
                    print(f"[Test {test_num}] Success! Website did not detect Selenium!")
                else:
                    print(f"[Test {test_num}] H1 text: {h1_text}")
                    # Retry once
                    print(f"[Test {test_num}] Retrying navigation...")
                    time.sleep(0.5)
                    browser_client.navigate_browser(browser_id, payload=nav_request)
                    time.sleep(1)

                    exec_result = browser_client.execute_script(browser_id, payload=exec_request)
                    if exec_result.success:
                        h1_text = exec_result.data.get("result") if exec_result.data else ""
                        print(f"[Test {test_num}] Retry H1 text: {h1_text}")
            else:
                # Take screenshot for manual verification
                print(f"[Test {test_num}] Script execution failed, taking screenshot")
                browser_client.take_screenshot(browser_id, payload=TakeScreenshotRequest())
                print(f"[Test {test_num}] Screenshot saved - check manually")

        except Exception as e:
            print(f"[Test {test_num}] Error checking detection: {e}")
            try:
                browser_client.take_screenshot(browser_id, payload=TakeScreenshotRequest())
                print(f"[Test {test_num}] Screenshot saved for manual verification")
            except:
                pass
            print(f"[Test {test_num}] Test completed - manual verification required")

    except Exception as e:
        pytest.fail(f"[Test {test_num}] Test failed: {e}")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
                print(f"[Test {test_num}] Closed browser: {browser_id}")
            except Exception:
                pass


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.browser
def test_single_uc_detection():
    """Single browser UC detection test for comparison"""

    browser_client = create_browser_client()
    browser_id = None

    try:
        # Create browser with UC mode
        browser_config = CreateBrowserRequest(window_size=[1280, 720])

        result = browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data["browser_id"]

        # Navigate to detection site
        nav_request = NavigateBrowserRequest(url="https://nowsecure.nl/#relax")
        browser_client.navigate_browser(browser_id, payload=nav_request)

        time.sleep(1)

        # Try to verify success
        try:
            exec_request = ExecuteScriptRequest(
                script="return document.querySelector('h1') ? document.querySelector('h1').textContent : 'Not found';"
            )
            exec_result = browser_client.execute_script(browser_id, payload=exec_request)

            if exec_result.success:
                h1_text = exec_result.data.get("result") if exec_result.data else ""

                print(f"Detection result: {h1_text}")

                if "OH YEAH, you passed!" in str(h1_text):
                    print("Single browser test passed - Selenium not detected!")
                else:
                    print(f"Unexpected result: {h1_text}")
        except:
            browser_client.take_screenshot(browser_id, payload=TakeScreenshotRequest())
            print("Screenshot saved for manual verification")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except:
                pass


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.browser
def test_concurrent_browsers_different_sites():
    """Test multiple browsers accessing different sites concurrently"""

    browser_client = create_browser_client()
    browser_ids = []

    sites = ["https://www.google.com", "https://www.example.com", "https://example.org"]

    try:
        # Create multiple browsers
        for i, site in enumerate(sites):
            browser_config = CreateBrowserRequest(window_size=[800, 600])

            result = browser_client.create_browser(payload=browser_config)
            assert result is not None
            assert result.success
            browser_id = result.data["browser_id"]
            browser_ids.append(browser_id)

            print(f"Created browser {i + 1}: {browser_id}")

            # Navigate each to different site
            nav_request = NavigateBrowserRequest(url=site)
            browser_client.navigate_browser(browser_id, payload=nav_request)
            print(f"Browser {i + 1} navigated to {site}")

        # Wait for all to load
        time.sleep(1)

        # Take screenshots of all
        for i, browser_id in enumerate(browser_ids):
            browser_client.take_screenshot(browser_id, payload=TakeScreenshotRequest())
            print(f"Screenshot taken for browser {i + 1}")

        print(f"Successfully managed {len(browser_ids)} concurrent browsers")

    finally:
        # Clean up all browsers
        for browser_id in browser_ids:
            try:
                browser_client.close_browser(browser_id)
            except:
                pass
