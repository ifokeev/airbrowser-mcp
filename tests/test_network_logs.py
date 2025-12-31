#!/usr/bin/env python3
"""
Test suite for CDP-based network logging feature.

Tests network logging API using network_logs endpoint with enable/disable/get/clear actions.

Run with: pytest tests/test_network_logs.py -v
"""

import time

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    NavigateBrowserRequest,
    NetworkLogsRequest,
)


@pytest.fixture(scope="function")
def browser_id(browser_client):
    """Create a browser for testing and clean up after."""
    config = CreateBrowserRequest(window_size=[1280, 900])
    result = browser_client.create_browser(payload=config)
    assert result.success, f"Failed to create browser: {result.message}"
    bid = result.data["browser_id"]

    yield bid

    # Cleanup - disable network logging and close browser
    try:
        browser_client.network_logs(bid, payload=NetworkLogsRequest(action="disable"))
    except Exception:
        pass
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestEnableNetworkLogging:
    """Test enabling network logging."""

    def test_enable_network_logging(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/network_logs with enable action."""
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        assert result is not None
        assert result.success
        assert "enabled" in result.message.lower() or result.data.get("status") == "success"

    def test_enable_network_logging_already_enabled(self, browser_client, browser_id):
        """Test enabling network logging when already enabled."""
        # Enable first time
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))

        # Enable again - should still succeed
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        assert result.success
        assert "already enabled" in result.message.lower() or "enabled" in result.message.lower()


@pytest.mark.browser
class TestDisableNetworkLogging:
    """Test disabling network logging."""

    def test_disable_network_logging(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/network_logs with disable action."""
        # Enable first
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))

        # Then disable
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="disable"))
        assert result is not None
        assert result.success
        assert "disabled" in result.message.lower() or result.data.get("status") == "success"

    def test_disable_network_logging_already_disabled(self, browser_client, browser_id):
        """Test disabling network logging when already disabled."""
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="disable"))
        assert result.success
        assert "disabled" in result.message.lower()


@pytest.mark.browser
class TestGetNetworkLogs:
    """Test getting network logs."""

    def test_get_network_logs_empty(self, browser_client, browser_id):
        """Test getting network logs when none captured."""
        # Enable logging
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))

        # Get logs immediately (should be empty or minimal)
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert result is not None
        assert result.success
        assert "events" in result.data or "total_events" in result.data

    def test_get_network_logs_after_navigation(self, browser_client, browser_id):
        """Test getting network logs after navigation captures events."""
        # Enable logging BEFORE navigation
        enable_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        assert enable_result.success

        # Wait for CDP connection
        time.sleep(0.5)

        # Navigate to trigger network activity
        nav_result = browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        assert nav_result.success

        # Wait for network events to be captured
        time.sleep(2)

        # Get logs
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert result.success
        assert result.data is not None

        # Should have captured some events
        total_events = result.data.get("total_events", 0)
        events = result.data.get("events", [])
        assert total_events > 0 or len(events) > 0, "Expected network events to be captured"

        # Verify event structure
        if events:
            event = events[0]
            assert "method" in event, "Event should have 'method' field"
            assert event["method"].startswith("Network."), "Event method should start with 'Network.'"

    def test_get_network_logs_with_limit(self, browser_client, browser_id):
        """Test getting network logs with limit parameter."""
        # Enable and navigate
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        time.sleep(0.5)
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://httpbin.org/get", timeout=30)
        )
        time.sleep(2)

        # Get with limit
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get", limit=5))
        assert result.success

        events = result.data.get("events", [])
        assert len(events) <= 5, "Limit should be respected"


@pytest.mark.browser
class TestClearNetworkLogs:
    """Test clearing network logs."""

    def test_clear_network_logs(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/network_logs with clear action."""
        # Enable and navigate to capture some events
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        time.sleep(0.5)
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        time.sleep(2)

        # Verify we have events
        get_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert get_result.data.get("total_events", 0) > 0, "Should have events before clearing"

        # Clear logs
        clear_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="clear"))
        assert clear_result.success
        assert "cleared" in clear_result.message.lower() or clear_result.data.get("status") == "success"

        # Verify logs are cleared
        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert result.data.get("total_events", 0) == 0, "Events should be cleared"


@pytest.mark.browser
class TestNetworkLoggingWorkflow:
    """Test complete network logging workflow."""

    def test_full_workflow(self, browser_client, browser_id):
        """Test complete enable -> navigate -> get -> clear -> disable workflow."""
        # 1. Enable network logging
        enable_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        assert enable_result.success, "Enable should succeed"

        # 2. Wait for CDP connection
        time.sleep(0.5)

        # 3. Navigate to capture events
        nav_result = browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://httpbin.org/html", timeout=30)
        )
        assert nav_result.success, "Navigation should succeed"

        # 4. Wait for events
        time.sleep(2)

        # 5. Get and verify events
        get_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert get_result.success, "Get should succeed"
        assert get_result.data.get("total_events", 0) > 0, "Should have events"
        assert get_result.data.get("enabled") is True, "Should report enabled=True"

        # 6. Check event types
        events = get_result.data.get("events", [])
        methods = [e.get("method") for e in events]
        assert any("requestWillBeSent" in m for m in methods), "Should have request events"
        assert any("responseReceived" in m for m in methods), "Should have response events"

        # 7. Clear logs
        clear_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="clear"))
        assert clear_result.success, "Clear should succeed"

        # 8. Verify cleared
        get_result2 = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert get_result2.data.get("total_events", 0) == 0, "Events should be cleared"

        # 9. Disable logging
        disable_result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="disable"))
        assert disable_result.success, "Disable should succeed"

    def test_logging_survives_multiple_navigations(self, browser_client, browser_id):
        """Test that network logging continues across multiple navigations."""
        # Enable
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        time.sleep(0.5)

        # First navigation
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        time.sleep(1)

        # Get count after first nav
        result1 = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        count1 = result1.data.get("total_events", 0)

        # Second navigation
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.org", timeout=30)
        )
        time.sleep(1)

        # Get count after second nav - should have more events
        result2 = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        count2 = result2.data.get("total_events", 0)

        assert count2 > count1, "Events should accumulate across navigations"


@pytest.mark.browser
class TestNetworkLoggingEventContent:
    """Test network log event content and structure."""

    def test_event_contains_request_info(self, browser_client, browser_id):
        """Test that network events contain request information."""
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        time.sleep(0.5)

        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://httpbin.org/get", timeout=30)
        )
        time.sleep(2)

        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        events = result.data.get("events", [])

        # Find a requestWillBeSent event
        request_events = [e for e in events if e.get("method") == "Network.requestWillBeSent"]
        assert len(request_events) > 0, "Should have request events"

        # Check structure
        event = request_events[0]
        assert "params" in event, "Event should have params"
        assert "timestamp" in event, "Event should have timestamp"

    def test_event_contains_response_info(self, browser_client, browser_id):
        """Test that network events contain response information."""
        browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="enable"))
        time.sleep(0.5)

        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://httpbin.org/status/200", timeout=30)
        )
        time.sleep(2)

        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        events = result.data.get("events", [])

        # Find a responseReceived event
        response_events = [e for e in events if e.get("method") == "Network.responseReceived"]
        assert len(response_events) > 0, "Should have response events"
