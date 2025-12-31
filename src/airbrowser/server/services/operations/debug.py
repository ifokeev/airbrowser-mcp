"""Debug operations (console logs, network requests)."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import LogAction
from .response import error as _error
from .response import success as _success


class DebugOperations:
    """Handles debugging and logging operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def get_console_logs(self, browser_id: str, limit: int = 200) -> dict[str, Any]:
        """List recent browser console log messages (best-effort)."""
        try:
            action = BrowserAction(action="get_console_logs", options={"limit": limit})
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            logs = None
            if isinstance(result.data, dict):
                logs = result.data.get("logs")

            data = result.data or {}
            data["logs"] = logs
            return _success(data=data, message=result.message)

        except Exception as e:
            return _error(f"get_console_logs failed: {str(e)}")

    def clear_console_logs(self, browser_id: str) -> dict[str, Any]:
        """Clear buffered console messages (best-effort)."""
        try:
            action = BrowserAction(action="clear_console_logs")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"clear_console_logs failed: {str(e)}")

    def enable_network_logging(self, browser_id: str) -> dict[str, Any]:
        """Enable CDP Network logging to capture network events.

        Must be called before navigating to capture network traffic.
        Events are buffered and can be retrieved with get action.
        """
        try:
            action = BrowserAction(action="enable_network_logging")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message or "Network logging enabled")
            return _error(result.message)

        except Exception as e:
            return _error(f"enable_network_logging failed: {str(e)}")

    def disable_network_logging(self, browser_id: str) -> dict[str, Any]:
        """Disable CDP Network logging."""
        try:
            action = BrowserAction(action="disable_network_logging")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message or "Network logging disabled")
            return _error(result.message)

        except Exception as e:
            return _error(f"disable_network_logging failed: {str(e)}")

    def get_network_logs(self, browser_id: str, limit: int = 500) -> dict[str, Any]:
        """Get buffered CDP Network events.

        Network logging must be enabled first with the enable action.
        Returns captured Network.* CDP events.
        """
        try:
            action = BrowserAction(action="get_network_logs", options={"limit": limit})
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            return _success(data=result.data, message="Network logs retrieved")

        except Exception as e:
            return _error(f"get_network_logs failed: {str(e)}")

    def clear_network_logs(self, browser_id: str) -> dict[str, Any]:
        """Clear buffered CDP Network events."""
        try:
            action = BrowserAction(action="clear_network_logs")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"clear_network_logs failed: {str(e)}")

    # ==================== Combined Methods ====================

    def console_logs(self, browser_id: str, action: LogAction, limit: int = 200) -> dict[str, Any]:
        """Manage console logs.

        Args:
            browser_id: The browser instance ID
            action: LogAction enum (GET or CLEAR)
            limit: Maximum logs to return (for GET action)
        """
        if action == LogAction.GET:
            return self.get_console_logs(browser_id, limit)
        elif action == LogAction.CLEAR:
            return self.clear_console_logs(browser_id)
        else:
            return _error(f"Invalid action: {action}")

    def network_logs(self, browser_id: str, action: LogAction, limit: int = 500) -> dict[str, Any]:
        """Manage network logs.

        Args:
            browser_id: The browser instance ID
            action: LogAction enum (GET, CLEAR, ENABLE, or DISABLE)
            limit: Maximum logs to return (for GET action)
        """
        if action == LogAction.GET:
            return self.get_network_logs(browser_id, limit)
        elif action == LogAction.CLEAR:
            return self.clear_network_logs(browser_id)
        elif action == LogAction.ENABLE:
            return self.enable_network_logging(browser_id)
        elif action == LogAction.DISABLE:
            return self.disable_network_logging(browser_id)
        else:
            return _error(f"Invalid action: {action}")

    def get_cdp_endpoint(self, browser_id: str) -> dict[str, Any]:
        """Get Chrome DevTools Protocol WebSocket endpoint URL.

        Returns both internal and external WebSocket URLs:
        - websocket_url: Direct internal connection (ws://127.0.0.1:PORT/devtools/...)
        - external_url: Proxied via nginx (ws://host:18080/browser/{browser_id}/cdp)

        Args:
            browser_id: The browser instance ID

        Returns:
            dict with websocket_url, external_url, debugger_address, browser version info
        """
        import os

        try:
            action = BrowserAction(action="get_cdp_endpoint")
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            # Extract the inner data from IPC response
            cdp_data = result.data.get("data", {}) if isinstance(result.data, dict) else {}

            # Add external URL for proxied access via nginx
            # API_BASE_URL defaults to http://localhost:18080 (nginx gateway)
            api_base = os.environ.get("API_BASE_URL", "http://localhost:18080")
            base_path = os.environ.get("BASE_PATH", "")
            # Convert http:// to ws:// and https:// to wss://
            ws_base = api_base.replace("http://", "ws://").replace("https://", "wss://")
            cdp_data["external_url"] = f"{ws_base}{base_path}/browser/{browser_id}/cdp"

            return _success(data=cdp_data, message="CDP endpoint retrieved successfully")

        except Exception as e:
            return _error(f"get_cdp_endpoint failed: {str(e)}")
