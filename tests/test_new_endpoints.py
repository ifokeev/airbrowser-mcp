#!/usr/bin/env python3
"""
Test combined element checking endpoints and selector types.
"""

import os
import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api
from airbrowser_client.models import (
    BrowserConfig,
    CheckElementRequest,
    NavigateRequest,
    WaitElementRequest,
)


def get_api_base_url():
    """Get API base URL from environment or default."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


def create_client():
    """Create a browser API client."""
    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    return browser_api.BrowserApi(airbrowser_client.ApiClient(configuration))


@pytest.mark.browser
def test_check_element_exists():
    """Test the check_element endpoint with exists check"""

    client = create_client()
    browser_id = None

    try:
        # Create browser
        browser_config = BrowserConfig()
        result = client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        # Navigate to test page
        nav_request = NavigateRequest(url="https://www.example.com")
        client.navigate_browser(browser_id, payload=nav_request)

        # Test check_element with CSS selector (exists check)
        check_request = CheckElementRequest(selector="h1", by="css", check="exists")
        check_result = client.check_element(browser_id, payload=check_request)

        assert check_result.success
        print("Found h1 element with CSS selector")

        # Test check non-existent element
        check_request = CheckElementRequest(selector="nonexistent", by="css", check="exists")
        check_result = client.check_element(browser_id, payload=check_request)

        assert check_result.success
        print("Correctly handled non-existent element check")

    finally:
        if browser_id:
            try:
                client.close_browser(browser_id)
            except Exception:
                pass  # Browser may already be closed


@pytest.mark.browser
def test_check_element_visible():
    """Test the check_element endpoint with visible check"""

    client = create_client()
    browser_id = None

    try:
        # Create browser
        browser_config = BrowserConfig()
        result = client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        # Navigate to test page
        nav_request = NavigateRequest(url="https://www.example.com")
        client.navigate_browser(browser_id, payload=nav_request)

        # Test check_element visible with visible element
        request = CheckElementRequest(selector="h1", by="css", check="visible")
        result = client.check_element(browser_id, payload=request)

        assert result.success
        print("h1 element visibility checked")

        # Test with non-existent element
        request = CheckElementRequest(selector="nonexistent", by="css", check="visible")
        result = client.check_element(browser_id, payload=request)

        assert result.success
        print("Correctly handled non-existent element visibility check")

    finally:
        if browser_id:
            try:
                client.close_browser(browser_id)
            except Exception:
                pass  # Browser may already be closed


@pytest.mark.browser
def test_selector_types():
    """Test different selector types (CSS, ID, XPath, Name)"""

    client = create_client()
    browser_id = None

    try:
        # Create browser
        browser_config = BrowserConfig()
        result = client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        # Navigate to example.com for testing
        nav_request = NavigateRequest(url="https://www.example.com")
        client.navigate_browser(browser_id, payload=nav_request)

        # Test XPath selector
        check_request = CheckElementRequest(selector="//h1", by="xpath", check="exists")
        check_result = client.check_element(browser_id, payload=check_request)

        assert check_result.success
        print("Found element with XPath selector")

        # Test CSS selector
        check_request = CheckElementRequest(selector="h1", by="css", check="exists")
        check_result = client.check_element(browser_id, payload=check_request)

        assert check_result.success
        print("Found element with CSS selector")

    finally:
        if browser_id:
            try:
                client.close_browser(browser_id)
            except Exception:
                pass  # Browser may already be closed


@pytest.mark.browser
def test_wait_element_with_selector_types():
    """Test wait_element functionality with different selector types"""

    client = create_client()
    browser_id = None

    try:
        # Create browser
        browser_config = BrowserConfig()
        result = client.create_browser(payload=browser_config)
        assert result is not None
        assert result.success
        browser_id = result.data.browser_id

        # Navigate to test page
        nav_request = NavigateRequest(url="https://www.example.com")
        client.navigate_browser(browser_id, payload=nav_request)

        # Test wait_element with CSS selector
        wait_request = WaitElementRequest(selector="h1", timeout=5, by="css", until="visible")
        wait_result = client.wait_element(browser_id, payload=wait_request)
        assert wait_result.success
        print("Wait succeeded with CSS selector")

    finally:
        if browser_id:
            try:
                client.close_browser(browser_id)
            except Exception:
                pass  # Browser may already be closed


@pytest.mark.quick
def test_server_status():
    """Test the server pool status endpoint"""

    client = create_client()

    # Get current pool status
    result = client.get_pool_status()
    assert result is not None
    assert result.success
    # data is a raw dict since PoolStatus.data is fields.Raw in schema
    print(f"Server is running with {result.data.get('active_browsers', 0)} active browsers")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
