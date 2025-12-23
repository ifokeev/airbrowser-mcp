"""Performance tracing operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import PerformanceAction


class PerformanceOperations:
    """Handles performance tracing operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def start_trace(self, browser_id: str, categories: str | None = None) -> dict[str, Any]:
        """Start performance tracing.

        Args:
            browser_id: Browser instance ID
            categories: Comma-separated trace categories (optional)
        """
        try:
            options = {}
            if categories:
                options["categories"] = categories

            action = BrowserAction(action="start_trace", options=options if options else None)
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"start_trace failed: {str(e)}"}

    def stop_trace(self, browser_id: str) -> dict[str, Any]:
        """Stop performance tracing and return trace data."""
        try:
            action = BrowserAction(action="stop_trace")
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"stop_trace failed: {str(e)}"}

    def get_metrics(self, browser_id: str) -> dict[str, Any]:
        """Get current performance metrics without tracing."""
        try:
            action = BrowserAction(action="get_metrics")
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"get_metrics failed: {str(e)}"}

    def analyze_insight(self, browser_id: str) -> dict[str, Any]:
        """Analyze page performance and return insights."""
        try:
            action = BrowserAction(action="analyze_insight")
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"analyze_insight failed: {str(e)}"}

    # ==================== Combined Method ====================

    def performance(
        self, browser_id: str, action: PerformanceAction, categories: str | None = None
    ) -> dict[str, Any]:
        """Manage performance tracing and metrics.

        Args:
            browser_id: The browser instance ID
            action: PerformanceAction enum (START_TRACE, STOP_TRACE, METRICS, or ANALYZE)
            categories: Trace categories (for START_TRACE action)
        """
        if action == PerformanceAction.START_TRACE:
            return self.start_trace(browser_id, categories)
        elif action == PerformanceAction.STOP_TRACE:
            return self.stop_trace(browser_id)
        elif action == PerformanceAction.METRICS:
            return self.get_metrics(browser_id)
        elif action == PerformanceAction.ANALYZE:
            return self.analyze_insight(browser_id)
        else:
            return {"success": False, "error": f"Invalid action: {action}"}
