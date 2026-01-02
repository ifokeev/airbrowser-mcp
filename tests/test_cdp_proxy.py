#!/usr/bin/env python3
"""
Test suite for CDP (Chrome DevTools Protocol) proxy feature.

Tests CDP endpoint retrieval and WebSocket proxy functionality.

Run with: pytest tests/test_cdp_proxy.py -v
"""

import json
import os
import re

import pytest
from airbrowser_client.models import (
    CookiesRequest,
    CreateBrowserRequest,
    ExecuteCdpRequest,
    NavigateBrowserRequest,
)

# WebSocket client for testing proxy
try:
    import websocket
except ImportError:
    websocket = None


def get_cdp_ws_url(browser_id: str) -> str:
    """Get the WebSocket URL for CDP proxy that works from test container.

    The external_url from the API uses localhost which doesn't work from
    the test container. We need to use the browser-pool hostname instead.
    """
    # BROWSER_POOL_URL is set in compose.test.yml (e.g., http://browser-pool:8000)
    api_base = os.environ.get("BROWSER_POOL_URL", "http://browser-pool:8000")
    # Extract host and port, convert to WebSocket URL
    # http://browser-pool:8000 -> ws://browser-pool:18080
    match = re.match(r"https?://([^:]+):(\d+)", api_base)
    if match:
        host = match.group(1)
        # CDP proxy runs on nginx port 18080, not Flask port 8000
        ws_url = f"ws://{host}:18080/browser/{browser_id}/cdp"
    else:
        # Fallback
        ws_url = f"ws://browser-pool:18080/browser/{browser_id}/cdp"
    return ws_url


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
class TestGetCdpEndpoint:
    """Test CDP endpoint retrieval."""

    def test_get_cdp_endpoint_returns_success(self, browser_client, browser_id):
        """Test GET /browser/{browser_id}/get_cdp_endpoint returns success."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result is not None
        assert result.success is True
        assert result.message == "CDP endpoint retrieved successfully"

    def test_get_cdp_endpoint_returns_websocket_url(self, browser_client, browser_id):
        """Test that response includes internal websocket_url."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        assert "websocket_url" in data
        assert data["websocket_url"].startswith("ws://")
        assert "/devtools/browser/" in data["websocket_url"]

    def test_get_cdp_endpoint_returns_external_url(self, browser_client, browser_id):
        """Test that response includes external_url for proxy access."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        assert "external_url" in data
        assert data["external_url"].startswith("ws://") or data["external_url"].startswith("wss://")
        assert f"/browser/{browser_id}/cdp" in data["external_url"]

    def test_get_cdp_endpoint_returns_debugger_address(self, browser_client, browser_id):
        """Test that response includes debugger_address."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        assert "debugger_address" in data
        # Format should be host:port
        assert ":" in data["debugger_address"]

    def test_get_cdp_endpoint_returns_browser_version(self, browser_client, browser_id):
        """Test that response includes browser version info."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        assert "browser_version" in data
        assert "Chrome" in data["browser_version"]

    def test_get_cdp_endpoint_returns_protocol_version(self, browser_client, browser_id):
        """Test that response includes CDP protocol version."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        assert "protocol_version" in data

    def test_get_cdp_endpoint_invalid_browser_fails(self, browser_client):
        """Test that invalid browser_id returns error."""
        from airbrowser_client.exceptions import NotFoundException

        try:
            result = browser_client.get_cdp_endpoint("invalid-browser-id-12345")
            # If no exception, check result indicates failure
            assert result.success is False
        except NotFoundException:
            pass  # Expected for HTTP 404

    def test_get_cdp_endpoint_external_url_includes_base_path(self, browser_client, browser_id):
        """Test that external_url respects BASE_PATH environment variable."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        data = result.data
        base_path = os.environ.get("BASE_PATH", "")

        if base_path:
            assert base_path in data["external_url"]
        # Without BASE_PATH, URL should be ws://host/browser/{id}/cdp
        assert f"/browser/{browser_id}/cdp" in data["external_url"]


@pytest.mark.browser
@pytest.mark.skipif(websocket is None, reason="websocket-client not installed")
class TestCdpWebSocketProxy:
    """Test CDP WebSocket proxy functionality."""

    def test_cdp_proxy_connection(self, browser_client, browser_id):
        """Test that WebSocket proxy accepts connections."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        # Use the helper to get URL that works from test container
        ws_url = get_cdp_ws_url(browser_id)

        # Connect via proxy
        ws = websocket.create_connection(ws_url, timeout=10)
        assert ws.connected
        ws.close()

    def test_cdp_proxy_send_receive(self, browser_client, browser_id):
        """Test sending CDP commands and receiving responses via proxy."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        ws_url = get_cdp_ws_url(browser_id)

        # Connect via proxy
        ws = websocket.create_connection(ws_url, timeout=10)

        try:
            # Send Browser.getVersion command
            cmd = json.dumps({"id": 1, "method": "Browser.getVersion"})
            ws.send(cmd)

            # Receive response
            ws.settimeout(5)
            response = ws.recv()
            data = json.loads(response)

            # Verify response structure
            assert "id" in data
            assert data["id"] == 1
            assert "result" in data
            assert "product" in data["result"]
            assert "Chrome" in data["result"]["product"]
        finally:
            ws.close()

    def test_cdp_proxy_page_navigate(self, browser_client, browser_id):
        """Test CDP Page.navigate command via proxy."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        ws_url = get_cdp_ws_url(browser_id)
        ws = websocket.create_connection(ws_url, timeout=10)

        try:
            # Navigate to example.com using CDP
            cmd = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://example.com"}})
            ws.send(cmd)

            ws.settimeout(10)
            response = ws.recv()
            data = json.loads(response)

            # Verify navigation was initiated
            assert "id" in data
            assert data["id"] == 1
            # Page.navigate returns frameId on success
            if "result" in data:
                assert "frameId" in data["result"]
        finally:
            ws.close()

    def test_cdp_proxy_target_get_targets(self, browser_client, browser_id):
        """Test CDP Target.getTargets command via proxy."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        ws_url = get_cdp_ws_url(browser_id)
        ws = websocket.create_connection(ws_url, timeout=10)

        try:
            # Get all targets
            cmd = json.dumps({"id": 1, "method": "Target.getTargets"})
            ws.send(cmd)

            ws.settimeout(5)
            response = ws.recv()
            data = json.loads(response)

            assert "id" in data
            assert data["id"] == 1
            assert "result" in data
            assert "targetInfos" in data["result"]
            # Should have at least one target (the browser page)
            assert len(data["result"]["targetInfos"]) >= 1
        finally:
            ws.close()

    def test_cdp_proxy_multiple_commands(self, browser_client, browser_id):
        """Test sending multiple CDP commands in sequence."""
        result = browser_client.get_cdp_endpoint(browser_id)
        assert result.success

        ws_url = get_cdp_ws_url(browser_id)
        ws = websocket.create_connection(ws_url, timeout=10)

        try:
            # Send multiple commands
            commands = [
                {"id": 1, "method": "Browser.getVersion"},
                {"id": 2, "method": "Target.getTargets"},
                {"id": 3, "method": "SystemInfo.getInfo"},
            ]

            ws.settimeout(5)

            for cmd in commands:
                ws.send(json.dumps(cmd))
                response = ws.recv()
                data = json.loads(response)

                assert "id" in data
                assert data["id"] == cmd["id"]
                # Each command should have either result or error
                assert "result" in data or "error" in data
        finally:
            ws.close()

    def test_cdp_proxy_invalid_browser_fails(self, browser_client):
        """Test that connecting to invalid browser returns error."""
        # Try to connect to non-existent browser
        invalid_url = get_cdp_ws_url("invalid-browser-id-xyz")

        with pytest.raises(Exception):
            # Should fail to connect or get error on handshake
            ws = websocket.create_connection(invalid_url, timeout=5)
            ws.close()


@pytest.mark.browser
class TestExecuteCdp:
    """Test execute_cdp endpoint for direct CDP command execution via REST API."""

    def test_execute_cdp_get_cookies(self, browser_client, browser_id):
        """Test executing Network.getAllCookies CDP command."""
        result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Network.getAllCookies"))
        assert result.success
        # CDP response is returned directly in data
        assert "cookies" in result.data

    def test_execute_cdp_get_version(self, browser_client, browser_id):
        """Test executing Browser.getVersion CDP command."""
        result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Browser.getVersion"))
        assert result.success
        # CDP response is returned directly in data
        assert "product" in result.data
        assert "Chrome" in result.data["product"]

    def test_execute_cdp_set_cookie(self, browser_client, browser_id):
        """Test setting a cookie via CDP directly."""
        # Navigate first
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )

        # Set cookie via CDP
        result = browser_client.execute_cdp(
            browser_id,
            payload=ExecuteCdpRequest(
                method="Network.setCookie",
                params={
                    "name": "cdp_cookie",
                    "value": "cdp_value",
                    "domain": "example.com",
                    "path": "/",
                },
            ),
        )
        assert result.success

        # Verify cookie was set
        get_result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Network.getAllCookies"))
        cookies = get_result.data["cookies"]
        assert any(c.get("name") == "cdp_cookie" for c in cookies)

    def test_execute_cdp_invalid_method(self, browser_client, browser_id):
        """Test executing an invalid CDP command."""
        result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Invalid.nonExistentMethod"))
        # Should fail gracefully
        assert not result.success or "error" in str(result.data).lower()

    def test_execute_cdp_page_info(self, browser_client, browser_id):
        """Test getting page information via CDP."""
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )

        # Get targets (pages)
        result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Target.getTargets"))
        assert result.success
        assert "targetInfos" in result.data


@pytest.mark.browser
class TestCookiesCdpIntegration:
    """Integration tests combining cookies endpoint and CDP."""

    def test_cookies_match_cdp(self, browser_client, browser_id):
        """Test that cookies endpoint and CDP return same cookies."""
        # Set a cookie via the cookies endpoint
        browser_client.navigate_browser(
            browser_id, payload=NavigateBrowserRequest(url="https://example.com", timeout=30)
        )
        browser_client.cookies(
            browser_id,
            payload=CookiesRequest(
                action="set", cookie={"name": "sync_test", "value": "sync_value", "domain": "example.com"}
            ),
        )

        # Get via cookies endpoint
        cookies_result = browser_client.cookies(browser_id, payload=CookiesRequest(action="get"))
        cookies_via_endpoint = cookies_result.data.get("cookies", cookies_result.data)

        # Get via CDP
        cdp_result = browser_client.execute_cdp(browser_id, payload=ExecuteCdpRequest(method="Network.getAllCookies"))
        cookies_via_cdp = cdp_result.data["cookies"]

        # Both should have the test cookie
        endpoint_names = {c.get("name") for c in cookies_via_endpoint}
        cdp_names = {c.get("name") for c in cookies_via_cdp}

        assert "sync_test" in endpoint_names
        assert "sync_test" in cdp_names
