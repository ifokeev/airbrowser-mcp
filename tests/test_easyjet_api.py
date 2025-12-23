#!/usr/bin/env python3
"""
EasyJet flight search test using the generated Python client and Browser Pool API
Based on undetected-testing/raw_easyjet.py
Run with: pytest tests/test_easyjet_api.py -v
"""

import os
import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api
from airbrowser_client.models import BrowserConfig, NavigateRequest


def get_api_base_url():
    """Get API base URL from environment or default."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.mark.slow
@pytest.mark.browser
@pytest.mark.flaky(reruns=2, reruns_delay=5)
def test_easyjet_page_loads():
    """Test that EasyJet page can be loaded with UC mode

    Note: This test may fail due to EasyJet's bot detection or network issues.
    """

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))

    browser_id = None

    try:
        # Create browser with UC mode
        browser_config = BrowserConfig(window_size=[1920, 1080])
        result = browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        time.sleep(3)

        # Navigate to EasyJet
        nav_request = NavigateRequest(url="https://www.easyjet.com/en/")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success

        time.sleep(5)

        # Take screenshot
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result.success

        # Verify URL contains easyjet
        url_result = browser_client.get_url(browser_id)
        assert url_result.success
        current_url = url_result.data.url

        assert "easyjet" in current_url.lower(), f"Not on EasyJet, URL: {current_url}"
        print(f"EasyJet page loaded at: {current_url}")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass


@pytest.mark.browser
@pytest.mark.flaky(reruns=2, reruns_delay=5)
def test_easyjet_simple_navigation():
    """Simple test to verify EasyJet page loads without UC mode

    Note: This test may fail due to EasyJet's bot detection or network issues.
    """

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))

    browser_id = None

    try:
        # Create browser without UC mode for faster test
        browser_config = BrowserConfig(window_size=[1920, 1080])
        result = browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        time.sleep(2)

        # Navigate to EasyJet
        nav_request = NavigateRequest(url="https://www.easyjet.com/en/")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success

        time.sleep(3)

        # Take screenshot
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result.success

        # Verify URL
        url_result = browser_client.get_url(browser_id)
        assert url_result.success
        print("EasyJet page loaded successfully")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass
