#!/usr/bin/env python3
"""
Comprehensive test suite for all Airbrowser REST API endpoints.
Tests every endpoint to ensure the refactored code works correctly.

Run with: pytest tests/test_all_endpoints.py -v
"""

import pytest
from airbrowser_client.models import (
    BrowsersRequest,
    CreateBrowserRequest,
    ClickRequest,
    ConsoleLogsRequest,
    ExecuteScriptRequest,
    HistoryRequest,
    NavigateBrowserRequest,
    NetworkLogsRequest,
    PressKeysRequest,
    TakeScreenshotRequest,
    TypeTextRequest,
    WaitElementRequest,
)


@pytest.fixture(scope="class")
def browser_id(browser_client):
    """Create a browser for testing and clean up after. Shared within test class."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    assert result is not None, "Failed to create browser"
    assert result.success, f"Browser creation failed: {result.message}"
    assert result.data is not None, "Browser creation returned no data"
    assert result.data.get('browser_id') is not None, "Browser ID is None"

    bid = result.data['browser_id']

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


class TestHealthEndpoints:
    """Test health-related endpoints."""

    def test_health_check(self, health_client):
        """Test GET /health/ endpoint."""
        result = health_client.health_check()
        assert result is not None
        assert result.status in ["healthy", "degraded"]


class TestPoolEndpoints:
    """Test pool-related endpoints."""

    def test_pool_scale(self, pool_client):
        """Test POST /pool/scale endpoint."""
        # Scale to current max (no-op but validates endpoint works)
        result = pool_client.scale_pool(payload={"target_size": 10})
        assert result is not None
        assert result.success


class TestBrowserLifecycle:
    """Test browser lifecycle endpoints."""

    def test_create_browser(self, browser_client):
        """Test POST /browser/create endpoint."""
        config = CreateBrowserRequest()
        result = browser_client.create_browser(payload=config)
        assert result is not None
        assert result.success
        assert result.data.get('browser_id') is not None

        bid = result.data['browser_id']

        # Cleanup
        browser_client.close_browser(bid)

    def test_list_browsers(self, browser_client, browser_id):
        """Test POST /browser/browsers endpoint with list action."""
        from airbrowser_client.models import BrowsersRequest
        result = browser_client.browsers(payload=BrowsersRequest(action="list"))
        assert result is not None
        assert result.success
        assert result.data['count'] >= 1

    def test_close_browser(self, browser_client):
        """Test POST /browser/{browser_id}/close endpoint."""
        # Create a browser to close
        config = CreateBrowserRequest()
        create_result = browser_client.create_browser(payload=config)
        bid = create_result.data['browser_id']

        result = browser_client.close_browser(bid)
        assert result is not None


class TestNavigationEndpoints:
    """Test navigation endpoints."""

    def test_navigate(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/navigate endpoint."""
        request = NavigateBrowserRequest(url="https://example.com", timeout=60)
        result = browser_client.navigate_browser(browser_id, payload=request)
        assert result is not None
        assert result.success

    def test_get_url(self, browser_client, browser_id):
        """Test GET /browser/{browser_id}/url endpoint."""
        # First navigate somewhere
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.get_url(browser_id)
        assert result is not None
        assert result.success
        assert "example.com" in result.data.get('url', '')

    def test_history_back(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/history with back action."""
        # Navigate to two pages
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.org"))

        # Go back using history endpoint
        result = browser_client.history(browser_id, payload=HistoryRequest(action="back"))
        assert result is not None
        assert result.success

    def test_history_forward(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/history with forward action."""
        # Navigate and go back first
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.org"))
        browser_client.history(browser_id, payload=HistoryRequest(action="back"))

        # Go forward using history endpoint
        result = browser_client.history(browser_id, payload=HistoryRequest(action="forward"))
        assert result is not None
        assert result.success

    def test_history_refresh(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/history with refresh action."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.history(browser_id, payload=HistoryRequest(action="refresh"))
        assert result is not None
        assert result.success


class TestElementInteraction:
    """Test element interaction endpoints."""

    def test_click(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/click endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Wait for the h1 heading to be present first (more reliable than anchor)
        wait_request = WaitElementRequest(selector="h1", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Click on the h1 heading - simpler and more reliable than anchor
        request = ClickRequest(selector="h1", by="css", timeout=15)
        result = browser_client.click(browser_id, payload=request)
        assert result is not None
        assert result.success

    def test_type(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/type endpoint - using execute to create input."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Create an input element via JavaScript
        exec_request = ExecuteScriptRequest(
            script="""
            var input = document.createElement('input');
            input.id = 'test-input';
            input.style.cssText = 'width:200px;height:30px;';
            document.body.insertBefore(input, document.body.firstChild);
            return 'created';
        """,
            timeout=30,
        )
        browser_client.execute_script(browser_id, payload=exec_request)

        # Wait for the input to be present
        wait_request = WaitElementRequest(selector="#test-input", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Now type into it
        request = TypeTextRequest(selector="#test-input", text="test text", by="css", timeout=15)
        result = browser_client.type_text(browser_id, payload=request)
        assert result is not None
        assert result.success

    def test_wait_element(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/wait_element endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        request = WaitElementRequest(selector="h1", by="css", until="visible", timeout=10)
        result = browser_client.wait_element(browser_id, payload=request)
        assert result is not None
        assert result.success

    def test_check_element_exists(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/check_element with exists check."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.check_element(browser_id, selector="h1", by="css", check="exists")
        assert result is not None
        assert result.success

    def test_check_element_visible(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/check_element with visible check."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Test visible element
        result = browser_client.check_element(browser_id, selector="h1", by="css", check="visible")
        assert result is not None
        assert result.success

        # Test non-existent element
        result = browser_client.check_element(browser_id, selector="nonexistent-element", by="css", check="visible")
        assert result is not None
        assert result.success

    def test_press_keys_enter(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/press_keys with ENTER key."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Create an input element via JavaScript
        exec_request = ExecuteScriptRequest(
            script="""
            var input = document.createElement('input');
            input.id = 'test-input-keys';
            input.style.cssText = 'width:200px;height:30px;';
            document.body.insertBefore(input, document.body.firstChild);
            return 'created';
        """,
            timeout=30,
        )
        browser_client.execute_script(browser_id, payload=exec_request)

        # Wait for the input to be present
        wait_request = WaitElementRequest(selector="#test-input-keys", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Press ENTER key
        request = PressKeysRequest(selector="#test-input-keys", keys="ENTER", by="css")
        result = browser_client.press_keys(browser_id, payload=request)
        assert result is not None
        assert result.success
        assert result.data is not None
        # Check that the keys were actually pressed (not empty)
        assert "ENTER" in str(result.data)

    def test_press_keys_tab(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/press_keys with TAB key."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Create two input elements
        exec_request = ExecuteScriptRequest(
            script="""
            var input1 = document.createElement('input');
            input1.id = 'input-tab-1';
            var input2 = document.createElement('input');
            input2.id = 'input-tab-2';
            document.body.insertBefore(input2, document.body.firstChild);
            document.body.insertBefore(input1, document.body.firstChild);
            input1.focus();
            return 'created';
        """,
            timeout=30,
        )
        browser_client.execute_script(browser_id, payload=exec_request)

        # Wait for the input
        wait_request = WaitElementRequest(selector="#input-tab-1", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Press TAB key
        request = PressKeysRequest(selector="#input-tab-1", keys="TAB", by="css")
        result = browser_client.press_keys(browser_id, payload=request)
        assert result is not None
        assert result.success
        assert "TAB" in str(result.data)

    def test_press_keys_combination(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/press_keys with key combination (CTRL+a)."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Create an input with text
        exec_request = ExecuteScriptRequest(
            script="""
            var input = document.createElement('input');
            input.id = 'input-combo';
            input.value = 'some text to select';
            document.body.insertBefore(input, document.body.firstChild);
            input.focus();
            return 'created';
        """,
            timeout=30,
        )
        browser_client.execute_script(browser_id, payload=exec_request)

        # Wait for the input
        wait_request = WaitElementRequest(selector="#input-combo", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Press CTRL+a to select all
        request = PressKeysRequest(selector="#input-combo", keys="CTRL+a", by="css")
        result = browser_client.press_keys(browser_id, payload=request)
        assert result is not None
        assert result.success
        assert "CTRL+a" in str(result.data)

    def test_press_keys_escape(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/press_keys with ESCAPE key."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        # Create an input element for the ESCAPE test
        exec_request = ExecuteScriptRequest(
            script="""
            var input = document.createElement('input');
            input.id = 'input-escape';
            document.body.insertBefore(input, document.body.firstChild);
            input.focus();
            return 'created';
        """,
            timeout=30,
        )
        browser_client.execute_script(browser_id, payload=exec_request)

        # Wait for the input
        wait_request = WaitElementRequest(selector="#input-escape", by="css", until="visible", timeout=10)
        browser_client.wait_element(browser_id, payload=wait_request)

        # Press ESCAPE key
        request = PressKeysRequest(selector="#input-escape", keys="ESCAPE", by="css")
        result = browser_client.press_keys(browser_id, payload=request)
        assert result is not None
        assert result.success
        assert "ESCAPE" in str(result.data)


class TestPageContent:
    """Test page content endpoints."""

    def test_get_content(self, browser_client, browser_id):
        """Test GET /browser/{browser_id}/content endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.get_content(browser_id)
        assert result is not None
        assert result.success
        # Verify data structure matches schema
        assert result.data is not None, "Response data should not be None"
        assert result.data.get('title') is not None, "Page title should be returned"
        assert result.data.get('text') is not None, "Page text should be returned"
        assert "Example Domain" in result.data.get('title', '')
        assert "Example Domain" in result.data.get('text', '')

    def test_screenshot(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/screenshot endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.take_screenshot(browser_id, payload=TakeScreenshotRequest())
        assert result is not None
        assert result.success
        # Verify data structure matches schema
        assert result.data is not None, "Response data should not be None"
        assert result.data.get('screenshot_url') is not None, "Screenshot URL should be returned"
        assert "screenshot" in result.data.get('screenshot_url', '').lower()

    def test_execute_script(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/execute endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        request = ExecuteScriptRequest(script="return document.title;")
        result = browser_client.execute_script(browser_id, payload=request)
        assert result is not None
        assert result.success
        # Verify data structure matches schema
        assert result.data is not None, "Response data should not be None"
        assert result.data.get('result') is not None, "Script result should be returned"
        # Result is wrapped in {"value": actual_result} for schema compatibility
        script_result = result.data.get('result', {})
        assert "Example Domain" in (script_result.get("value", "") if isinstance(script_result, dict) else str(script_result))


class TestDebugEndpoints:
    """Test debug/logging endpoints."""

    def test_console_logs(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/console endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.console_logs(browser_id, payload=ConsoleLogsRequest(action="get"))
        assert result is not None
        assert result.success

    def test_network_logs(self, browser_client, browser_id):
        """Test POST /browser/{browser_id}/network endpoint."""
        browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url="https://example.com"))

        result = browser_client.network_logs(browser_id, payload=NetworkLogsRequest(action="get"))
        assert result is not None
        assert result.success


@pytest.mark.browser
class TestCloseAll:
    """Test close all browsers endpoint (runs separately after parallel tests)."""

    def test_close_all_browsers(self, browser_client):
        """Test POST /browser/browsers with close_all action."""
        # Create a test browser
        config = CreateBrowserRequest()
        browser_client.create_browser(payload=config)

        result = browser_client.browsers(payload=BrowsersRequest(action="close_all"))
        assert result is not None
        assert result.success
