"""GUI click operations."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .response import error as _error
from .response import success as _success


class GuiOperations:
    """Handles GUI-based click operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def gui_click(
        self,
        browser_id: str,
        selector: str | None = None,
        x: float | None = None,
        y: float | None = None,
        timeframe: float = 0.25,
        fx: float | None = None,
        fy: float | None = None,
    ) -> dict[str, Any]:
        """Perform GUI click on element by selector or at specific coordinates.

        Args:
            browser_id: The browser instance ID
            selector: CSS selector for element to click (selector mode)
            x: X coordinate to click (coordinate mode)
            y: Y coordinate to click (coordinate mode)
            timeframe: Time to move mouse to target
            fx: Fractional X offset within element (0.0-1.0, selector mode only)
            fy: Fractional Y offset within element (0.0-1.0, selector mode only)

        Use selector for element-based clicks, or x/y for coordinate-based clicks.
        """
        try:
            # Coordinate mode: x and y provided
            if x is not None and y is not None:
                options = {"x": x, "y": y, "timeframe": timeframe}
                action = BrowserAction(action="gui_click_xy", options=options)
                result = self.browser_pool.execute_action(browser_id, action)
            # Selector mode: selector provided
            elif selector is not None:
                options = {"timeframe": timeframe}
                if fx is not None:
                    options["fx"] = fx
                if fy is not None:
                    options["fy"] = fy
                action = BrowserAction(action="gui_click", selector=selector, options=options)
                result = self.browser_pool.execute_action(browser_id, action)
            else:
                return _error("Either 'selector' or both 'x' and 'y' must be provided.")

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"gui_click failed: {str(e)}")

    def gui_click_xy(self, browser_id: str, x: float, y: float, timeframe: float = 0.25) -> dict[str, Any]:
        """Click at specific coordinates."""
        try:
            options = {"x": x, "y": y, "timeframe": timeframe}
            action = BrowserAction(action="gui_click_xy", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"gui_click_xy failed: {str(e)}")

    def gui_type_xy(self, browser_id: str, x: float, y: float, text: str, timeframe: float = 0.25) -> dict[str, Any]:
        """Click at coordinates then type text using GUI automation."""
        try:
            options = {"x": x, "y": y, "text": text, "timeframe": timeframe}
            action = BrowserAction(action="gui_type_xy", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"gui_type_xy failed: {str(e)}")

    def gui_hover_xy(self, browser_id: str, x: float, y: float, timeframe: float = 0.25) -> dict[str, Any]:
        """Hover at specific coordinates using GUI automation."""
        try:
            options = {"x": x, "y": y, "timeframe": timeframe}
            action = BrowserAction(action="gui_hover_xy", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"gui_hover_xy failed: {str(e)}")

    def gui_press_keys_xy(
        self, browser_id: str, x: float, y: float, keys: str, timeframe: float = 0.25
    ) -> dict[str, Any]:
        """Click at coordinates then press special keys."""
        try:
            options = {"x": x, "y": y, "keys": keys, "timeframe": timeframe}
            action = BrowserAction(action="gui_press_keys_xy", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                return _success(data=result.data, message=result.message)
            return _error(result.message)

        except Exception as e:
            return _error(f"gui_press_keys_xy failed: {str(e)}")
