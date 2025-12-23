"""Debug operations (console logs, network requests)."""

import json
from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import LogAction


class DebugOperations:
    """Handles debugging and logging operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def get_console_logs(self, browser_id: str, limit: int = 200) -> dict[str, Any]:
        """List recent browser console log messages (best-effort)."""
        try:
            action = BrowserAction(action="get_console_logs", options={"limit": limit})
            result = self.browser_pool.execute_action(browser_id, action)

            logs = None
            if result.success and isinstance(result.data, dict):
                logs = result.data.get("logs")

            return {
                "success": result.success,
                "message": result.message,
                "logs": logs,
                "data": result.to_dict() if result.success else None,
                "error": None if result.success else result.message,
            }
        except Exception as e:
            return {"success": False, "error": f"get_console_logs failed: {str(e)}"}

    def clear_console_logs(self, browser_id: str) -> dict[str, Any]:
        """Clear buffered console messages (best-effort)."""
        try:
            action = BrowserAction(action="clear_console_logs")
            result = self.browser_pool.execute_action(browser_id, action)
            return {
                "success": result.success,
                "message": result.message,
                "data": result.to_dict() if result.success else None,
                "error": None if result.success else result.message,
            }
        except Exception as e:
            return {"success": False, "error": f"clear_console_logs failed: {str(e)}"}

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

            return {
                "success": result.success,
                "message": result.message,
                "events": events,
                "raw_logs": raw_logs,
                "data": result.to_dict() if result.success else None,
                "error": None if result.success else result.message,
            }
        except Exception as e:
            return {"success": False, "error": f"get_network_logs failed: {str(e)}"}

    def clear_network_logs(self, browser_id: str) -> dict[str, Any]:
        """Clear buffered performance/network logs (best-effort)."""
        try:
            action = BrowserAction(action="clear_performance_logs")
            result = self.browser_pool.execute_action(browser_id, action)
            return {
                "success": result.success,
                "message": result.message,
                "data": result.to_dict() if result.success else None,
                "error": None if result.success else result.message,
            }
        except Exception as e:
            return {"success": False, "error": f"clear_network_logs failed: {str(e)}"}

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
            return {"success": False, "error": f"Invalid action: {action}"}

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
            return {"success": False, "error": f"Invalid action: {action}"}
