"""Debug operations (console logs, network requests)."""

import json
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

    def get_network_logs(self, browser_id: str, limit: int = 500) -> dict[str, Any]:
        """
        List recent network-related events from Chrome performance logs (best-effort).
        Returned items are parsed CDP events when available.
        """
        try:
            action = BrowserAction(action="get_performance_logs", options={"limit": limit})
            result = self.browser_pool.execute_action(browser_id, action)

            raw_logs = None
            events = []

            if result.success and isinstance(result.data, dict):
                raw_logs = result.data.get("logs") or []
                for entry in raw_logs:
                    if not isinstance(entry, dict):
                        continue
                    message_text = entry.get("message")
                    if not message_text or not isinstance(message_text, str):
                        continue
                    try:
                        parsed = json.loads(message_text)
                    except Exception:
                        continue
                    inner = parsed.get("message") if isinstance(parsed, dict) else None
                    if not isinstance(inner, dict):
                        continue
                    method = inner.get("method")
                    if isinstance(method, str) and method.startswith("Network."):
                        events.append(inner)

            if not result.success:
                return _error(result.message)

            return _success(
                data={
                    "events": events,
                    "raw_logs": raw_logs,
                    **(result.data or {}),
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"get_network_logs failed: {str(e)}")

    def clear_network_logs(self, browser_id: str) -> dict[str, Any]:
        """Clear buffered performance/network logs (best-effort)."""
        try:
            action = BrowserAction(action="clear_performance_logs")
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
            action: LogAction enum (GET or CLEAR)
            limit: Maximum logs to return (for GET action)
        """
        if action == LogAction.GET:
            return self.get_network_logs(browser_id, limit)
        elif action == LogAction.CLEAR:
            return self.clear_network_logs(browser_id)
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
