#!/usr/bin/env python3
"""
Test suite for browser kill and restore functionality.

Tests the kill (save state) and restore operations without container restart.

Run with: pytest tests/test_kill_restore.py -v
"""

import pytest
from airbrowser_client.models import (
    BrowsersRequest,
    CreateBrowserRequest,
    NavigateBrowserRequest,
    TabsRequest,
)


@pytest.fixture(scope="function", autouse=True)
def clean_state(browser_client):
    """Clean up any existing browsers and saved state before each test."""
    # First restore any saved state (clears the state file)
    browser_client.browsers(payload=BrowsersRequest(action="restore"))
    # Then close all browsers (including any restored ones)
    browser_client.browsers(payload=BrowsersRequest(action="close_all"))
    yield


@pytest.fixture(scope="function")
def browser_id(browser_client):
    """Create a browser for testing and clean up after."""
    config = CreateBrowserRequest(window_size=[1280, 900])
    result = browser_client.create_browser(payload=config)
    assert result.success, f"Failed to create browser: {result.message}"
    bid = result.data["browser_id"]

    yield bid

    # Cleanup - try to close if still exists
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestKillBrowser:
    """Test killing a single browser."""

    def test_kill_browser_saves_state(self, browser_client, browser_id):
        """Test that kill saves browser state before terminating."""
        # Navigate to a page first
        browser_client.navigate_browser(
            browser_id,
            payload=NavigateBrowserRequest(url="https://example.com", timeout=60),
        )

        # Kill the browser (saves state)
        result = browser_client.browsers(payload=BrowsersRequest(action="kill", browser_id=browser_id))
        assert result.success, f"Kill failed: {result.message}"
        assert result.data is not None
        assert result.data.get("browser_id") == browser_id

        # Verify browser is gone
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        browser_ids = [b["browser_id"] for b in list_result.data.get("browsers", [])]
        assert browser_id not in browser_ids, "Browser should be closed after kill"

    def test_kill_nonexistent_browser_fails(self, browser_client):
        """Test that killing a nonexistent browser returns an error."""
        result = browser_client.browsers(payload=BrowsersRequest(action="kill", browser_id="nonexistent-id"))
        assert not result.success, "Should fail for nonexistent browser"


@pytest.mark.browser
class TestKillAll:
    """Test killing all browsers."""

    def test_kill_all_saves_state(self, browser_client):
        """Test that kill_all saves state for all browsers."""
        # Create two browsers
        result1 = browser_client.create_browser(payload=CreateBrowserRequest())
        result2 = browser_client.create_browser(payload=CreateBrowserRequest())
        assert result1.success and result2.success

        bid1 = result1.data["browser_id"]
        bid2 = result2.data["browser_id"]

        # Navigate each to different pages
        browser_client.navigate_browser(
            bid1,
            payload=NavigateBrowserRequest(url="https://example.com", timeout=60),
        )
        browser_client.navigate_browser(
            bid2,
            payload=NavigateBrowserRequest(url="https://example.org", timeout=60),
        )

        # Kill all browsers
        result = browser_client.browsers(payload=BrowsersRequest(action="kill_all"))
        assert result.success, f"Kill all failed: {result.message}"
        assert result.data.get("killed") == 2

        # Verify all browsers are gone
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        assert list_result.data.get("count", 0) == 0

    def test_kill_all_with_no_browsers(self, browser_client):
        """Test that kill_all succeeds even with no browsers."""
        # First close any existing browsers
        browser_client.browsers(payload=BrowsersRequest(action="close_all"))

        # Kill all (should succeed with 0 killed)
        result = browser_client.browsers(payload=BrowsersRequest(action="kill_all"))
        assert result.success
        assert result.data.get("killed") == 0


@pytest.mark.browser
class TestRestore:
    """Test restoring killed browsers."""

    def test_restore_after_kill(self, browser_client):
        """Test restoring a browser after killing it."""
        # Create and navigate browser
        create_result = browser_client.create_browser(payload=CreateBrowserRequest())
        assert create_result.success
        browser_id = create_result.data["browser_id"]

        browser_client.navigate_browser(
            browser_id,
            payload=NavigateBrowserRequest(url="https://example.com", timeout=60),
        )

        # Kill the browser
        kill_result = browser_client.browsers(payload=BrowsersRequest(action="kill", browser_id=browser_id))
        assert kill_result.success

        # Restore
        restore_result = browser_client.browsers(payload=BrowsersRequest(action="restore"))
        assert restore_result.success, f"Restore failed: {restore_result.message}"
        assert restore_result.data.get("restored") == 1

        # Get the new browser ID
        browsers = restore_result.data.get("browsers", [])
        assert len(browsers) == 1
        new_browser_id = browsers[0]["new_id"]

        # Verify URL was restored
        tabs_after = browser_client.tabs(new_browser_id, payload=TabsRequest(action="current"))
        url_after = tabs_after.data.get("url", "") if tabs_after.data else ""

        # URLs should match (or at least both contain example.com)
        assert "example.com" in url_after, f"URL not restored. Expected example.com, got {url_after}"

        # Cleanup
        browser_client.close_browser(new_browser_id)

    def test_restore_with_multiple_tabs(self, browser_client):
        """Test restoring a browser with multiple tabs."""
        # Create browser
        create_result = browser_client.create_browser(payload=CreateBrowserRequest())
        assert create_result.success
        browser_id = create_result.data["browser_id"]

        # Navigate first tab
        browser_client.navigate_browser(
            browser_id,
            payload=NavigateBrowserRequest(url="https://example.com", timeout=60),
        )

        # Open second tab
        browser_client.tabs(
            browser_id,
            payload=TabsRequest(action="new", url="https://example.org"),
        )

        # Kill browser
        kill_result = browser_client.browsers(payload=BrowsersRequest(action="kill", browser_id=browser_id))
        assert kill_result.success
        tabs_saved = kill_result.data.get("tabs_saved", 0)
        assert tabs_saved == 2, f"Expected 2 tabs saved, got {tabs_saved}"

        # Restore
        restore_result = browser_client.browsers(payload=BrowsersRequest(action="restore"))
        assert restore_result.success

        # Get restored browser
        browsers = restore_result.data.get("browsers", [])
        assert len(browsers) == 1
        new_browser_id = browsers[0]["new_id"]
        assert browsers[0]["tabs"] == 2

        # Verify tabs were restored
        tabs_result = browser_client.tabs(new_browser_id, payload=TabsRequest(action="list"))
        tab_count = tabs_result.data.get("count", 0) if tabs_result.data else 0
        assert tab_count == 2, f"Expected 2 tabs restored, got {tab_count}"

        # Cleanup
        browser_client.close_browser(new_browser_id)

    def test_restore_with_no_saved_state(self, browser_client):
        """Test that restore succeeds even with no saved state."""
        # First ensure no saved state by closing all browsers normally
        browser_client.browsers(payload=BrowsersRequest(action="close_all"))

        # Restore should succeed with 0 restored
        result = browser_client.browsers(payload=BrowsersRequest(action="restore"))
        assert result.success
        assert result.data.get("restored") == 0


@pytest.mark.browser
class TestKillRestoreRoundTrip:
    """Test full kill and restore round trip."""

    def test_kill_all_and_restore_all(self, browser_client):
        """Test killing all browsers and restoring them."""
        # Create multiple browsers
        browsers_created = []
        for i in range(2):
            result = browser_client.create_browser(payload=CreateBrowserRequest())
            assert result.success
            bid = result.data["browser_id"]
            browsers_created.append(bid)

            # Navigate each
            browser_client.navigate_browser(
                bid,
                payload=NavigateBrowserRequest(url=f"https://example.com/page{i}", timeout=60),
            )

        # Verify browsers exist
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        assert list_result.data.get("count") == 2

        # Kill all
        kill_result = browser_client.browsers(payload=BrowsersRequest(action="kill_all"))
        assert kill_result.success
        assert kill_result.data.get("killed") == 2

        # Verify all gone
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        assert list_result.data.get("count") == 0

        # Restore all
        restore_result = browser_client.browsers(payload=BrowsersRequest(action="restore"))
        assert restore_result.success
        assert restore_result.data.get("restored") == 2

        # Verify all restored
        list_result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        assert list_result.data.get("count") == 2

        # Cleanup
        browser_client.browsers(payload=BrowsersRequest(action="close_all"))
