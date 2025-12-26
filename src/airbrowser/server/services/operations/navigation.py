"""Navigation operations."""

import os
from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import HistoryAction
from .response import error as _error
from .response import success as _success


class NavigationOperations:
    """Handles browser navigation operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def navigate_browser(self, browser_id: str, url: str, timeout: int | None = None) -> dict[str, Any]:
        """Navigate browser to a specific URL."""
        try:
            if timeout is None:
                timeout = int(os.environ.get("NAVIGATE_TIMEOUT_DEFAULT", 60))

            action = BrowserAction(action="navigate", url=url, timeout=timeout)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Navigation failed: {str(e)}")

    def get_url(self, browser_id: str) -> dict[str, Any]:
        """Get the current URL of the browser."""
        try:
            action = BrowserAction(action="get_url")
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            current_url = None
            if isinstance(result.data, dict):
                current_url = result.data.get("result") or result.data.get("url")

            return _success(data={"url": current_url}, message=result.message)

        except Exception as e:
            return _error(f"Get URL failed: {str(e)}")

    def go_back(self, browser_id: str) -> dict[str, Any]:
        """Navigate back in browser history."""
        try:
            action = BrowserAction(action="go_back")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Go back failed: {str(e)}")

    def go_forward(self, browser_id: str) -> dict[str, Any]:
        """Navigate forward in browser history."""
        try:
            action = BrowserAction(action="go_forward")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Go forward failed: {str(e)}")

    def refresh(self, browser_id: str) -> dict[str, Any]:
        """Refresh the current page."""
        try:
            action = BrowserAction(action="refresh")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"Refresh failed: {str(e)}")

    def history(self, browser_id: str, action: HistoryAction) -> dict[str, Any]:
        """Execute browser history navigation.

        Args:
            browser_id: The browser instance ID
            action: HistoryAction enum (BACK, FORWARD, or REFRESH)

        Returns:
            Result dict with success status
        """
        if action == HistoryAction.BACK:
            return self.go_back(browser_id)
        elif action == HistoryAction.FORWARD:
            return self.go_forward(browser_id)
        elif action == HistoryAction.REFRESH:
            return self.refresh(browser_id)
        else:
            return _error(f"Invalid history action: {action}")
