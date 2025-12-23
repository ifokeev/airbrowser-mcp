"""Page content operations (screenshot, content, execute JS)."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter


class PageOperations:
    """Handles page content operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def take_screenshot(self, browser_id: str, full_page: bool = False) -> dict[str, Any]:
        """Take a screenshot of the browser."""
        try:
            action = BrowserAction(action="screenshot")
            result = self.browser_pool.execute_action(browser_id, action)

            screenshot_url = None
            screenshot_path = None
            if result.success and isinstance(result.data, dict):
                # Browser command returns 'url' and 'path', not 'screenshot_url'
                screenshot_url = result.data.get("url") or result.data.get("path")
                screenshot_path = result.data.get("path") or screenshot_url

            return {
                "success": result.success,
                "message": result.message,
                "data": {
                    "screenshot_url": screenshot_url,
                    "screenshot_path": screenshot_path,
                },
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"Screenshot failed: {str(e)}"}

    def get_content(self, browser_id: str) -> dict[str, Any]:
        """Get the page content."""
        try:
            action = BrowserAction(action="get_content")
            result = self.browser_pool.execute_action(browser_id, action)

            html = None
            title = None
            url = None
            if result.success and isinstance(result.data, dict):
                html = result.data.get("content") or result.data.get("page_source")
                title = result.data.get("title")
                url = result.data.get("url")

            return {
                "success": result.success,
                "message": result.message,
                "data": {
                    "html": html,
                    "title": title,
                    "url": url,
                },
                "error": None if result.success else result.message,
            }
        except Exception as e:
            return {"success": False, "error": f"get_content failed: {str(e)}"}

    def execute_script(self, browser_id: str, script: str) -> dict[str, Any]:
        """Execute JavaScript code in the browser."""
        try:
            action = BrowserAction(action="execute_script", text=script)
            result = self.browser_pool.execute_action(browser_id, action)

            script_result = None
            if result.success and isinstance(result.data, dict):
                raw_result = result.data.get("result")
                # Wrap result in dict for schema compatibility (Raw field becomes dict in OpenAPI)
                script_result = {"value": raw_result} if raw_result is not None else None

            return {
                "success": result.success,
                "message": result.message,
                "data": {
                    "result": script_result,
                },
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"JavaScript execution failed: {str(e)}"}

    def resize(self, browser_id: str, width: int, height: int) -> dict[str, Any]:
        """Resize the browser viewport."""
        try:
            action = BrowserAction(action="resize", options={"width": width, "height": height})
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"Resize failed: {str(e)}"}

    def snapshot(self, browser_id: str, snapshot_type: str = "dom") -> dict[str, Any]:
        """Take a DOM or accessibility tree snapshot."""
        try:
            action = BrowserAction(action="snapshot", options={"type": snapshot_type})
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"Snapshot failed: {str(e)}"}
