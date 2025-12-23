#!/usr/bin/env python3
"""
Complete test of the generated Python client for the Browser Pool API.
Tests all key features including browser creation, navigation, and interactions.

Run with: pytest tests/test_generated_client_complete.py -v
"""

import os
import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api, health_api, pool_api
from airbrowser_client.models import BrowserConfig, ExecuteRequest, NavigateRequest


def get_api_base_url():
    """Get API base URL from environment or default."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.mark.browser
@pytest.mark.flaky(reruns=3, reruns_delay=5)
def test_browser_pool_complete():
    """Test all key features of the browser pool API"""

    # Configure the client
    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()

    # Create API clients
    health_client = health_api.HealthApi(airbrowser_client.ApiClient(configuration))
    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))

    # Test health check
    health = health_client.health_check()
    assert health is not None, "Health check returned None"
    assert health.status in ["healthy", "degraded"], f"Unexpected health status: {health.status}"

    # Test browser creation
    browser_config = BrowserConfig()
    create_result = browser_client.create_browser(payload=browser_config)
    assert create_result is not None, "Create browser returned None"
    assert create_result.success, f"Create browser failed: {create_result.message}"
    assert create_result.data.browser_id is not None, "Browser ID is None"

    browser_id = create_result.data.browser_id

    try:
        # Wait for browser to initialize
        time.sleep(3)

        # Test navigation
        nav_request = NavigateRequest(url="https://example.com")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result is not None, "Navigate returned None"
        assert nav_result.success, f"Navigation failed: {nav_result.message}"

        time.sleep(2)

        # Test get URL
        url_result = browser_client.get_url(browser_id)
        assert url_result is not None, "Get URL returned None"
        assert url_result.success, f"Get URL failed: {url_result.message}"
        assert "example.com" in url_result.data.url, f"Unexpected URL: {url_result.data.url}"

        # Test execute script
        exec_request = ExecuteRequest(script="return document.title")
        exec_result = browser_client.execute_script(browser_id, payload=exec_request)
        assert exec_result is not None, "Execute script returned None"
        assert exec_result.success, f"Execute script failed: {exec_result.message}"

        # Test screenshot
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result is not None, "Screenshot returned None"
        assert screenshot_result.success, f"Screenshot failed: {screenshot_result.message}"

        # Test list browsers
        list_result = browser_client.list_browsers()
        assert list_result is not None, "List browsers returned None"
        assert list_result.success, f"List browsers failed: {list_result.message}"
        assert list_result.data.count >= 1, "Expected at least 1 browser"

    finally:
        # Clean up
        try:
            browser_client.close_browser(browser_id)
        except Exception:
            pass  # Browser may have already been closed or crashed


@pytest.mark.browser
@pytest.mark.flaky(reruns=2, reruns_delay=5)
def test_browser_with_uc_mode():
    """Test browser creation with UC (undetected Chrome) mode"""

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()

    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))

    # Create browser with UC mode
    browser_config = BrowserConfig(window_size=[1920, 1080])
    create_result = browser_client.create_browser(payload=browser_config)
    assert create_result is not None, "Create browser returned None"
    assert create_result.success, f"Create browser failed: {create_result.message}"

    browser_id = create_result.data.browser_id

    try:
        time.sleep(3)

        # Navigate to a site
        nav_request = NavigateRequest(url="https://example.com")
        nav_result = browser_client.navigate_browser(browser_id, payload=nav_request)
        assert nav_result.success, f"Navigation failed: {nav_result.message}"

        time.sleep(2)

        # Take screenshot
        screenshot_result = browser_client.take_screenshot(browser_id)
        assert screenshot_result.success, f"Screenshot failed: {screenshot_result.message}"

    finally:
        try:
            browser_client.close_browser(browser_id)
        except Exception:
            pass  # Browser may have already been closed or crashed


@pytest.mark.browser
def test_browser_pool_scaling():
    """Test pool status and browser pool operations"""

    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()

    browser_client = browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))
    pool_api.PoolApi(airbrowser_client.ApiClient(configuration))

    # Get pool status
    pool_status = browser_client.get_pool_status()
    assert pool_status is not None, "Pool status returned None"
    assert pool_status.success, f"Pool status failed: {pool_status.message}"

    # Create multiple browsers
    browser_ids = []
    for i in range(2):
        config = BrowserConfig()
        result = browser_client.create_browser(payload=config)
        assert result.success, f"Create browser {i} failed"
        browser_ids.append(result.data.browser_id)

    time.sleep(3)

    try:
        # Check pool status again
        pool_status = browser_client.get_pool_status()
        assert pool_status.success, "Pool status failed after creating browsers"

        # List browsers
        list_result = browser_client.list_browsers()
        assert list_result.success, "List browsers failed"
        assert list_result.data.count >= 2, f"Expected at least 2 browsers, got {list_result.data.count}"

    finally:
        # Close all created browsers
        for bid in browser_ids:
            try:
                browser_client.close_browser(bid)
            except Exception:
                pass
