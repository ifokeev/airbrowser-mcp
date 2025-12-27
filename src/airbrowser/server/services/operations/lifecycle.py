"""Browser lifecycle operations (create, close, list)."""

import logging
from typing import Any

from ...models import BrowserConfig, get_window_size_from_env
from ..browser_pool import BrowserPoolAdapter
from .enums import BrowsersAction
from .response import error as _error
from .response import success as _success

logger = logging.getLogger(__name__)


class LifecycleOperations:
    """Handles browser lifecycle operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def create_browser(
        self,
        uc: bool = True,
        proxy: str | None = None,
        window_size: list[int] | None = None,
        user_agent: str | None = None,
        disable_gpu: bool = False,
        disable_images: bool = False,
        disable_javascript: bool = False,
        extensions: list[str] | None = None,
        custom_args: list[str] | None = None,
        profile_name: str | None = None,
    ) -> dict[str, Any]:
        """Create a new browser instance with specified configuration."""
        try:
            if window_size is None:
                window_size = get_window_size_from_env()
            if extensions is None:
                extensions = []
            if custom_args is None:
                custom_args = []

            config = BrowserConfig(
                uc=uc,
                proxy=proxy,
                user_agent=user_agent,
                window_size=tuple(window_size),
                disable_gpu=disable_gpu,
                disable_images=disable_images,
                disable_javascript=disable_javascript,
                extensions=extensions,
                custom_args=custom_args,
                profile_name=profile_name,
            )

            browser_id = self.browser_pool.create_browser(config)

            return _success(
                data={"browser_id": browser_id, "config": config.to_dict()},
                message="Browser created successfully",
            )

        except Exception as e:
            return _error(f"Failed to create browser: {str(e)}")

    def close_browser(self, browser_id: str) -> dict[str, Any]:
        """Close a specific browser instance."""
        try:
            success = self.browser_pool.close_browser(browser_id)

            if success:
                return _success(message=f"Browser {browser_id} closed successfully")
            else:
                return _error(f"Browser {browser_id} not found")

        except Exception as e:
            return _error(f"Failed to close browser: {str(e)}")

    def list_active_browsers(self) -> dict[str, Any]:
        """List all active browser instances."""
        try:
            browsers = self.browser_pool.list_browsers()
            browser_list = [browser.to_dict() for browser in browsers]

            return _success(
                data={"browsers": browser_list, "count": len(browser_list)},
                message=f"Found {len(browser_list)} active browsers",
            )

        except Exception as e:
            return _error(f"Failed to list browsers: {str(e)}")

    def get_browser_info(self, browser_id: str) -> dict[str, Any]:
        """Get detailed information about a specific browser."""
        try:
            instance = self.browser_pool.get_browser(browser_id)
            if not instance:
                return _error(f"Browser {browser_id} not found")

            browser_info = instance.to_info()

            return _success(
                data={"browser_info": browser_info.to_dict()},
                message=f"Browser {browser_id} information retrieved",
            )

        except Exception as e:
            return _error(f"Failed to get browser info: {str(e)}")

    def close_all_browsers(self) -> dict[str, Any]:
        """Close all active browser instances."""
        try:
            self.browser_pool.close_all_browsers()

            return _success(message="All browsers closed successfully")

        except Exception as e:
            return _error(f"Failed to close all browsers: {str(e)}")

    def kill_browser(self, browser_id: str) -> dict[str, Any]:
        """Kill a browser - saves state before terminating (can be restored later)."""
        try:
            result = self.browser_pool.kill_browser(browser_id)
            if result.get("status") == "success":
                return _success(
                    message=result.get("message", f"Browser {browser_id} killed"),
                    data=result.get("data", {}),
                )
            else:
                return _error(result.get("message", f"Failed to kill browser {browser_id}"))

        except Exception as e:
            return _error(f"Failed to kill browser: {str(e)}")

    def kill_all_browsers(self) -> dict[str, Any]:
        """Kill all browsers - saves state before terminating (can be restored later)."""
        try:
            result = self.browser_pool.kill_all_browsers()
            if result.get("status") == "success":
                return _success(
                    message=result.get("message", "Killed all browsers"),
                    data=result.get("data", {}),
                )
            else:
                return _error(result.get("message", "Failed to kill all browsers"))

        except Exception as e:
            return _error(f"Failed to kill all browsers: {str(e)}")

    def restore_browsers(self) -> dict[str, Any]:
        """Restore killed browsers from saved state."""
        try:
            result = self.browser_pool.restore_browsers()
            if result.get("status") == "success":
                return _success(
                    message=result.get("message", "Restored browsers"),
                    data=result.get("data", {}),
                )
            else:
                return _error(result.get("message", "Failed to restore browsers"))

        except Exception as e:
            return _error(f"Failed to restore browsers: {str(e)}")

    def browsers(self, action: BrowsersAction, browser_id: str | None = None) -> dict[str, Any]:
        """Admin browser operations: list, info, close_all, kill, kill_all, restore."""
        if action == BrowsersAction.LIST:
            return self.list_active_browsers()
        elif action == BrowsersAction.INFO:
            if not browser_id:
                return _error("browser_id required for info")
            return self.get_browser_info(browser_id)
        elif action == BrowsersAction.CLOSE_ALL:
            return self.close_all_browsers()
        elif action == BrowsersAction.KILL:
            if not browser_id:
                return _error("browser_id required for kill")
            return self.kill_browser(browser_id)
        elif action == BrowsersAction.KILL_ALL:
            return self.kill_all_browsers()
        elif action == BrowsersAction.RESTORE:
            return self.restore_browsers()
        return _error(f"Invalid action: {action}")
