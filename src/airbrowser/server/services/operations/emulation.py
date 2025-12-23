"""Device emulation operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .enums import EmulateAction


class EmulationOperations:
    """Handles device emulation operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def emulate(
        self,
        browser_id: str,
        action: EmulateAction = EmulateAction.SET,
        device: str | None = None,
        width: int | None = None,
        height: int | None = None,
        device_scale_factor: float | None = None,
        mobile: bool | None = None,
        user_agent: str | None = None,
    ) -> dict[str, Any]:
        """Manage device emulation.

        Args:
            browser_id: Browser instance ID
            action: EmulateAction enum (SET, CLEAR, or LIST_DEVICES)
            device: Device preset name (e.g., "iPhone 14", "iPad") - for SET action
            width: Custom viewport width - for SET action
            height: Custom viewport height - for SET action
            device_scale_factor: Pixel ratio - for SET action
            mobile: Enable touch events - for SET action
            user_agent: Custom user agent - for SET action
        """
        # Handle clear and list_devices actions
        if action == EmulateAction.CLEAR:
            return self.clear_emulation(browser_id)
        elif action == EmulateAction.LIST_DEVICES:
            return self.list_devices(browser_id)
        elif action != EmulateAction.SET:
            return {"success": False, "error": f"Invalid action: {action}"}

        # Set emulation
        try:
            options = {}
            if device:
                options["device"] = device
            if width:
                options["width"] = width
            if height:
                options["height"] = height
            if device_scale_factor:
                options["device_scale_factor"] = device_scale_factor
            if mobile is not None:
                options["mobile"] = mobile
            if user_agent:
                options["user_agent"] = user_agent

            browser_action = BrowserAction(action="emulate", options=options)
            result = self.browser_pool.execute_action(browser_id, browser_action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"emulate failed: {str(e)}"}

    def list_devices(self, browser_id: str) -> dict[str, Any]:
        """List available device presets."""
        try:
            action = BrowserAction(action="list_devices")
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"list_devices failed: {str(e)}"}

    def clear_emulation(self, browser_id: str) -> dict[str, Any]:
        """Clear device emulation and restore defaults."""
        try:
            action = BrowserAction(action="clear_emulation")
            result = self.browser_pool.execute_action(browser_id, action)

            return {
                "success": result.success,
                "message": result.message,
                "data": result.data if result.success else None,
                "error": result.message if not result.success else None,
            }

        except Exception as e:
            return {"success": False, "error": f"clear_emulation failed: {str(e)}"}
