#!/usr/bin/env python3
"""
Test suite for cookie management endpoints.

Tests cookie get/set/delete/clear operations using CDP for full cookie access.

Run with: pytest tests/test_cookies.py -v
"""

import time

import pytest
from airbrowser_client.models import (
    CookiesRequest,
    CreateBrowserRequest,
    NavigateBrowserRequest,
)


@pytest.fixture(scope="function")
def browser_id(browser_client):
    """Create a browser for testing and clean up after."""
    config = CreateBrowserRequest(window_size=[1280, 900])
    result = browser_client.create_browser(payload=config)
    assert result.success, f"Failed to create browser: {result.message}"
    bid = result.data["browser_id"]

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestGetCookies:
    """Test getting cookies."""

    def test_get_cookies_empty(self, browser_client, browser_id):
        """Test getting cookies when none exist."""
        result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        assert result is not None
        assert result.success
        assert "cookies" in result.data or isinstance(result.data, list)

    def test_get_cookies_after_navigation(self, browser_client, browser_id):
        """Test getting cookies after visiting a site that sets cookies."""
        # Navigate to httpbin which can set cookies (this endpoint redirects after setting cookie)
        browser_client.navigate_browser(
            browser_id,
            payload=NavigateBrowserRequest(url="https://httpbin.org/cookies/set?test_cookie=test_value", timeout=30),
        )

        # Wait for redirect to complete and cookie to be set
        time.sleep(1)

        # Get cookies
        result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        assert result.success
        cookies = result.data.get("cookies", result.data)
        assert isinstance(cookies, list)

        # Should have the test cookie
        cookie_names = [c.get("name") for c in cookies]
        assert "test_cookie" in cookie_names, f"Expected test_cookie in {cookie_names}"


@pytest.mark.browser
class TestSetCookie:
    """Test setting cookies."""

    def test_set_cookie(self, browser_client, browser_id):
        """Test setting a cookie."""
        # Navigate first to establish a domain
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )

        # Set a cookie
        cookie = {
            "name": "my_test_cookie",
            "value": "my_test_value",
            "domain": "example.com",
            "path": "/",
        }
        result = browser_client.cookies(browser_id, payload=CookiesRequest(action="set", cookie=cookie))
        assert result.success

        # Verify cookie was set
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        cookie_names = [c.get("name") for c in cookies]
        assert "my_test_cookie" in cookie_names

    def test_set_httponly_cookie(self, browser_client, browser_id):
        """Test setting an HttpOnly cookie (requires CDP)."""
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )

        # Set HttpOnly cookie
        cookie = {
            "name": "secure_session",
            "value": "secret123",
            "domain": "example.com",
            "path": "/",
            "httpOnly": True,
        }
        result = browser_client.cookies(browser_id, payload=CookiesRequest(action="set", cookie=cookie))
        assert result.success

        # Verify we can retrieve it (proves CDP is working)
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        session_cookies = [c for c in cookies if c.get("name") == "secure_session"]
        assert len(session_cookies) == 1
        assert session_cookies[0].get("httpOnly") is True


@pytest.mark.browser
class TestDeleteCookie:
    """Test deleting cookies."""

    def test_delete_cookie_by_name(self, browser_client, browser_id):
        """Test deleting a specific cookie by name."""
        # Navigate and set a cookie
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        cookie = {"name": "to_delete", "value": "delete_me", "domain": "example.com"}
        browser_client.cookies(browser_id, payload=CookiesRequest(action="set", cookie=cookie))

        # Verify cookie exists
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        assert any(c.get("name") == "to_delete" for c in cookies)

        # Delete the cookie
        delete_result = browser_client.cookies(
            browser_id, payload=CookiesRequest(action="delete", name="to_delete", domain="example.com")
        )
        assert delete_result.success

        # Verify cookie is gone
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        assert not any(c.get("name") == "to_delete" for c in cookies)


@pytest.mark.browser
class TestClearCookies:
    """Test clearing all cookies."""

    def test_clear_all_cookies(self, browser_client, browser_id):
        """Test clearing all cookies."""
        # Navigate and set multiple cookies
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        browser_client.cookies(
            browser_id,
            payload=CookiesRequest(action="set", cookie={"name": "c1", "value": "v1", "domain": "example.com"}),
        )
        browser_client.cookies(
            browser_id,
            payload=CookiesRequest(action="set", cookie={"name": "c2", "value": "v2", "domain": "example.com"}),
        )

        # Verify cookies exist
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        assert len(cookies) >= 2

        # Clear all cookies
        clear_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="clear"))
        assert clear_result.success

        # Verify cookies are cleared
        get_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies = get_result.data.get("cookies", get_result.data)
        # Note: May still have some browser-set cookies, but our test cookies should be gone
        cookie_names = [c.get("name") for c in cookies]
        assert "c1" not in cookie_names
        assert "c2" not in cookie_names
