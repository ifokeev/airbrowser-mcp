#!/usr/bin/env python3
"""
ChatGPT test using the generated Python client and Browser Pool API

Run with: pytest tests/test_chatgpt_api.py -v
"""

import os
import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api
from airbrowser_client.models import (
    BrowserConfig,
    NavigateRequest,
)


def get_api_base_url():
    """Get API base URL from environment or default."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.browser
def test_chatgpt_interaction():
    """Test ChatGPT interaction using Browser Pool API with UC+CDP mode."""

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()

    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))
    browser_id = None

    try:
        # Create browser (UC+CDP enabled by default)
        browser_config = BrowserConfig(window_size=[1920, 1080])
        result = browser_client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id
        assert browser_id is not None

        time.sleep(1)

        # Navigate to ChatGPT
        nav_request = NavigateRequest(url="https://chatgpt.com/")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success
        time.sleep(1)

        # Take a screenshot for verification
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result.success
        print("Screenshot saved - ChatGPT page loaded")

    except Exception as e:
        pytest.fail(f"Test failed: {e}")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass


@pytest.mark.slow
@pytest.mark.external
@pytest.mark.browser
def test_chatgpt_page_loads():
    """Basic test that ChatGPT page can be loaded (without interaction)"""

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

        time.sleep(1)

        # Navigate to ChatGPT
        nav_request = NavigateRequest(url="https://chatgpt.com/")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success

        time.sleep(1)

        # Verify we're on ChatGPT by checking URL
        url_result = browser_client.get_url(browser_id)
        assert url_result.success
        current_url = url_result.data.url

        # ChatGPT may redirect, but should contain chatgpt or openai
        assert "chatgpt" in current_url.lower() or "openai" in current_url.lower(), f"Unexpected URL: {current_url}"

        # Take screenshot
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result.success
        print(f"ChatGPT page loaded at: {current_url}")

    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass
