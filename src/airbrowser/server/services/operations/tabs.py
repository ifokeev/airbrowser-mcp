"""Tab operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import TabAction
from .response import error as _error
from .response import success as _success


class TabOperations:
    """Handles browser tab operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def list_tabs(self, browser_id: str) -> dict[str, Any]:
        """List all tabs in the browser."""
        try:
            action = BrowserAction(action="list_tabs")
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            tabs = []
            if isinstance(result.data, dict):
                tabs = result.data.get("tabs", [])

            return _success(
                data={
                    "tabs": tabs,
                    "count": len(tabs),
                    "current_index": result.data.get("current_index", 0) if result.data else 0,
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"List tabs failed: {str(e)}")

    def new_tab(self, browser_id: str, url: str | None = None) -> dict[str, Any]:
        """Open a new tab, optionally navigating to a URL."""
        try:
            action = BrowserAction(action="new_tab", options={"url": url} if url else None)
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            return _success(
                data={
                    "handle": result.data.get("handle") if result.data else None,
                    "index": result.data.get("index") if result.data else None,
                    "url": result.data.get("url") if result.data else None,
                    "title": result.data.get("title") if result.data else None,
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"New tab failed: {str(e)}")

    def switch_tab(self, browser_id: str, index: int | None = None, handle: str | None = None) -> dict[str, Any]:
        """Switch to a specific tab by index or handle."""
        try:
            options = {}
            if index is not None:
                options["index"] = index
            if handle:
                options["handle"] = handle

            action = BrowserAction(action="switch_tab", options=options if options else None)
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            return _success(
                data={
                    "handle": result.data.get("handle") if result.data else None,
                    "index": result.data.get("index") if result.data else None,
                    "url": result.data.get("url") if result.data else None,
                    "title": result.data.get("title") if result.data else None,
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"Switch tab failed: {str(e)}")

    def close_tab(self, browser_id: str, index: int | None = None, handle: str | None = None) -> dict[str, Any]:
        """Close a specific tab by index or handle. If neither provided, closes current tab."""
        try:
            options = {}
            if index is not None:
                options["index"] = index
            if handle:
                options["handle"] = handle

            action = BrowserAction(action="close_tab", options=options if options else None)
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            return _success(
                data={
                    "closed_handle": result.data.get("closed_handle") if result.data else None,
                    "remaining_tabs": result.data.get("remaining_tabs") if result.data else None,
                    "current_handle": result.data.get("current_handle") if result.data else None,
                    "current_url": result.data.get("current_url") if result.data else None,
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"Close tab failed: {str(e)}")

    def get_current_tab(self, browser_id: str) -> dict[str, Any]:
        """Get information about the current tab."""
        try:
            action = BrowserAction(action="get_current_tab")
            result = self.browser_pool.execute_action(browser_id, action)

            if not result.success:
                return _error(result.message)

            return _success(
                data={
                    "handle": result.data.get("handle") if result.data else None,
                    "index": result.data.get("index") if result.data else None,
                    "url": result.data.get("url") if result.data else None,
                    "title": result.data.get("title") if result.data else None,
                    "total_tabs": result.data.get("total_tabs") if result.data else None,
                },
                message=result.message,
            )

        except Exception as e:
            return _error(f"Get current tab failed: {str(e)}")

    # ==================== Combined Method ====================

    def tabs(
        self,
        browser_id: str,
        action: TabAction,
        url: str | None = None,
        index: int | None = None,
        handle: str | None = None,
    ) -> dict[str, Any]:
        """Manage browser tabs.

        Args:
            browser_id: The browser instance ID
            action: TabAction enum (LIST, NEW, SWITCH, CLOSE, or CURRENT)
            url: URL to open (for NEW action)
            index: Tab index (for SWITCH or CLOSE actions)
            handle: Tab handle (for SWITCH or CLOSE actions)
        """
        if action == TabAction.LIST:
            return self.list_tabs(browser_id)
        elif action == TabAction.NEW:
            return self.new_tab(browser_id, url)
        elif action == TabAction.SWITCH:
            return self.switch_tab(browser_id, index, handle)
        elif action == TabAction.CLOSE:
            return self.close_tab(browser_id, index, handle)
        elif action == TabAction.CURRENT:
            return self.get_current_tab(browser_id)
        else:
            return _error(f"Invalid action: {action}")
