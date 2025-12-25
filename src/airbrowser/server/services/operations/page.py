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
            if result.success and isinstance(result.data, dict):
                # Return URL only (path is internal Docker path, not accessible externally)
                screenshot_url = result.data.get("url") or result.data.get("screenshot_url")

            return {
                "success": result.success,
                "message": result.message,
                "data": {
                    "screenshot_url": screenshot_url,
                },
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"Screenshot failed: {str(e)}"}

    def get_content(self, browser_id: str, max_length: int = 50000) -> dict[str, Any]:
        """Get the visible text content of the page (no HTML tags).

        Returns the text that a user would see on the page, extracted from
        document.body.innerText. This is much more compact than raw HTML
        and suitable for LLM consumption.

        Args:
            browser_id: The browser instance ID
            max_length: Maximum text length to return (default 50000 chars)
        """
        try:
            # Get text content via JavaScript - much cleaner than HTML
            script = """
            return {
                text: document.body.innerText || document.body.textContent || '',
                title: document.title,
                url: window.location.href
            };
            """
            action = BrowserAction(action="execute_script", text=script)
            result = self.browser_pool.execute_action(browser_id, action)

            text = None
            title = None
            url = None
            truncated = False

            if result.success and isinstance(result.data, dict):
                script_result = result.data.get("result", {})
                if isinstance(script_result, dict):
                    text = script_result.get("text", "")
                    title = script_result.get("title", "")
                    url = script_result.get("url", "")

                    # Truncate if too long
                    if text and len(text) > max_length:
                        text = text[:max_length] + "\n\n... [truncated]"
                        truncated = True

            return {
                "success": result.success,
                "message": result.message,
                "data": {
                    "text": text,
                    "title": title,
                    "url": url,
                    "truncated": truncated,
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
