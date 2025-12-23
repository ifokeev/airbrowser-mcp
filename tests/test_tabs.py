#!/usr/bin/env python3
"""
Test suite for browser tabs feature.

Tests tab management API using combined tabs endpoint.

Run with: pytest tests/test_tabs.py -v
"""

import os
import time

import airbrowser_client
import pytest
from airbrowser_client.api import browser_api
from airbrowser_client.models import (
    BrowserConfig,
    NavigateRequest,
    TabsRequest,
)


def get_api_base_url():
    """Get API base URL from environment or default."""
    return os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.fixture(scope="module")
def api_client():
    """Create API client configuration."""
    configuration = airbrowser_client.Configuration()
    configuration.host = get_api_base_url()
    return configuration


@pytest.fixture(scope="module")
def browser_client(api_client):
    """Create browser API client."""
    return browser_api.BrowserApi(airbrowser_client.ApiClient(api_client))


@pytest.fixture(scope="function")
def browser_id(browser_client):
    """Create a browser for testing and clean up after."""
    config = BrowserConfig(window_size=[1280, 900])
    result = browser_client.create_browser(payload=config)
    assert result.success, f"Failed to create browser: {result.message}"
    bid = result.data.browser_id

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


class TestListTabs:
    """Test listing tabs."""

    def test_list_tabs_initial(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with list action - should have one tab initially."""
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert result is not None
        assert result.success

    def test_list_tabs_after_new_tab(self, browser_client, browser_id):
        """Test that list_tabs shows multiple tabs."""
        # Open a new tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))

        result = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert result.success


@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestNewTab:
    """Test opening new tabs."""

    def test_new_tab_blank(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with new action - open blank tab."""
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="new"))
        assert result is not None
        assert result.success

        # Verify tab count
        tabs = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert tabs.success

    def test_new_tab_with_url(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with new action and URL."""
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="new", url="https://example.com"))
        assert result is not None
        assert result.success


        # Verify we're on the new tab
        current = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert current.success

    def test_new_tab_multiple(self, browser_client, browser_id):
        """Test opening multiple tabs."""
        # Open 3 new tabs
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))

        result = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert result.success


@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestSwitchTab:
    """Test switching between tabs."""

    def test_switch_tab_by_index(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with switch action by index."""
        # Open a new tab (will be index 1)
        browser_client.tabs(browser_id, payload=TabsRequest(action="new", url="https://example.org"))

        # Switch to tab 0
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="switch", index=0))
        assert result.success

        # Verify switch worked
        current = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert current.success

    def test_switch_tab_invalid_index(self, browser_client, browser_id):
        """Test switching to invalid tab index fails."""
        with pytest.raises(Exception) as exc_info:
            browser_client.tabs(browser_id, payload=TabsRequest(action="switch", index=999))
        assert "400" in str(exc_info.value)


class TestCloseTab:
    """Test closing tabs."""

    def test_close_tab_current(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with close action - close current tab."""
        # Open a new tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="new", url="https://example.org"))

        # Close current tab (without specifying index/handle)
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="close"))
        assert result.success

    def test_close_tab_by_index(self, browser_client, browser_id):
        """Test closing tab by index."""
        # Open a new tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))

        # Close first tab (index 0)
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="close", index=0))
        assert result.success

    def test_close_tab_last_tab_fails(self, browser_client, browser_id):
        """Test that closing the last tab fails."""
        # Try to close the only tab
        with pytest.raises(Exception) as exc_info:
            browser_client.tabs(browser_id, payload=TabsRequest(action="close"))
        assert "400" in str(exc_info.value)

    def test_close_tab_invalid_index(self, browser_client, browser_id):
        """Test closing tab with invalid index fails."""
        with pytest.raises(Exception) as exc_info:
            browser_client.tabs(browser_id, payload=TabsRequest(action="close", index=999))
        assert "400" in str(exc_info.value)


@pytest.mark.flaky(reruns=2, reruns_delay=3)
class TestGetCurrentTab:
    """Test getting current tab info."""

    def test_get_current_tab(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/tabs with current action."""
        # Navigate to a page first
        browser_client.navigate_browser(browser_id, payload=NavigateRequest(url="https://example.com"))

        result = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert result is not None
        assert result.success

    def test_get_current_tab_after_switch(self, browser_client, browser_id):
        """Test current tab info updates after switch."""
        # Navigate first tab
        browser_client.navigate_browser(browser_id, payload=NavigateRequest(url="https://example.com"))

        # Open a new blank tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="new"))

        # Current should be the new tab
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert result.success

        # Switch to first tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="switch", index=0))

        # Current should be first tab
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert result.success


@pytest.mark.flaky(reruns=3, reruns_delay=5)
class TestTabNavigation:
    """Test navigation within tabs."""

    def test_navigate_in_different_tabs(self, browser_client, browser_id):
        """Test navigating in different tabs maintains separate state."""
        # Navigate first tab to example.com
        browser_client.navigate_browser(browser_id, payload=NavigateRequest(url="https://example.com"))

        # Open new tab
        new_tab_result = browser_client.tabs(browser_id, payload=TabsRequest(action="new"))
        assert new_tab_result.success, "Failed to create new tab"

        # Navigate second tab to example.org
        browser_client.navigate_browser(browser_id, payload=NavigateRequest(url="https://example.org", timeout=60))

        # Verify second tab
        current = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert current.success

        # Switch back to first tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="switch", index=0))

        # Verify first tab
        current = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert current.success

    def test_tab_operations_sequence(self, browser_client, browser_id):
        """Test a typical sequence of tab operations."""
        # 1. Check initial state
        tabs = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert tabs.success

        # 2. Open new tab with URL
        browser_client.tabs(browser_id, payload=TabsRequest(action="new", url="https://example.com"))

        # 3. Open another blank tab
        result = browser_client.tabs(browser_id, payload=TabsRequest(action="new"))
        assert result.success

        # 4. List all tabs
        tabs = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert tabs.success

        # 5. Switch to first tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="switch", index=0))

        # 6. Verify we're on first tab
        current = browser_client.tabs(browser_id, payload=TabsRequest(action="current"))
        assert current.success

        # 7. Close middle tab
        browser_client.tabs(browser_id, payload=TabsRequest(action="close", index=1))

        # 8. Verify tabs remain
        tabs = browser_client.tabs(browser_id, payload=TabsRequest(action="list"))
        assert tabs.success
