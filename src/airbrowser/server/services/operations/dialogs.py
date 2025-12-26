"""Dialog handling operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import DialogAction
from .response import error as _error
from .response import success as _success


class DialogOperations:
    """Handles browser dialog operations (alert, confirm, prompt)."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def handle_dialog(
        self, browser_id: str, action: str = "accept", text: str | None = None
    ) -> dict[str, Any]:
        """Handle a browser dialog.

        Args:
            browser_id: Browser instance ID
            action: "accept" or "dismiss"
            text: Optional text for prompt dialogs
        """
        try:
            browser_action = BrowserAction(
                action="handle_dialog", options={"action": action, "text": text}
            )
            result = self.browser_pool.execute_action(browser_id, browser_action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"handle_dialog failed: {str(e)}")

    def get_dialog(self, browser_id: str) -> dict[str, Any]:
        """Get current dialog text without dismissing it."""
        try:
            action = BrowserAction(action="get_dialog")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"get_dialog failed: {str(e)}")

    # ==================== Combined Method ====================

    def dialog(self, browser_id: str, action: DialogAction, text: str | None = None) -> dict[str, Any]:
        """Manage browser dialogs.

        Args:
            browser_id: The browser instance ID
            action: DialogAction enum (GET, ACCEPT, or DISMISS)
            text: Optional text for prompt dialogs (for ACCEPT action)
        """
        if action == DialogAction.GET:
            return self.get_dialog(browser_id)
        elif action in (DialogAction.ACCEPT, DialogAction.DISMISS):
            return self.handle_dialog(browser_id, action.value, text)
        else:
            return _error(f"Invalid action: {action}")
