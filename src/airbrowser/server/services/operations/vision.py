"""Vision-based operations using AI models."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter
from .response import error as _error
from .response import success as _success


class VisionOperations:
    """Handles vision-based AI operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def detect_coordinates(
        self, browser_id: str, prompt: str, fx: float | None = None, fy: float | None = None
    ) -> dict[str, Any]:
        """
        Detect element coordinates using vision models without clicking.

        Args:
            browser_id: Browser instance identifier
            prompt: Natural language description of element to find
            fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right).
                If None, auto-bias is applied for wide elements (0.25 for aspect ratio > 10).
            fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom).

        Returns:
            Dictionary with coordinate information
        """
        try:
            # Only include fx/fy if explicitly set - allows vision handler to apply auto-bias
            options: dict[str, Any] = {"prompt": prompt}
            if fx is not None:
                options["fx"] = fx
            if fy is not None:
                options["fy"] = fy
            action = BrowserAction(action="detect_coordinates", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                coord_data = result.data.get("coordinates", {}) if isinstance(result.data, dict) else {}
                return _success(
                    data={
                        "prompt": prompt,
                        "screenshot_url": coord_data.get("screenshot_url") or coord_data.get("screenshot_path"),
                        "confidence": coord_data.get("confidence"),
                        "click_point": coord_data.get("click_point"),
                        "bounding_box": {
                            "x": coord_data.get("x"),
                            "y": coord_data.get("y"),
                            "width": coord_data.get("width"),
                            "height": coord_data.get("height"),
                        }
                        if coord_data.get("x") is not None
                        else None,
                    },
                    message=result.message,
                )
            else:
                # Include extra data for debugging failed detections
                error_data = {
                    "prompt": prompt,
                    "models_tried": (result.data.get("models_tried") if isinstance(result.data, dict) else []),
                    "screenshot_url": (result.data.get("screenshot_url") or result.data.get("screenshot_path") if isinstance(result.data, dict) else None),
                }
                return _error(result.message)

        except Exception as e:
            return _error(f"Coordinate detection failed: {str(e)}")

    def what_is_visible(self, browser_id: str) -> dict[str, Any]:
        """
        Comprehensive page state analysis - what's visible on the current page.

        Uses AI vision to analyze the current page state including:
        - Form fields (filled/empty/required)
        - Checkboxes and radio buttons (selected/unselected)
        - CAPTCHA presence and state
        - Buttons and available actions
        - Error/success messages
        - Multi-step form progress
        - Overall page purpose and state

        Args:
            browser_id: Browser instance identifier

        Returns:
            Dictionary with comprehensive page state analysis
        """
        try:
            action = BrowserAction(action="what_is_visible")
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                data = result.data if isinstance(result.data, dict) else {}
                return _success(
                    data={
                        "analysis": data.get("analysis"),
                        "model": data.get("model"),
                        "screenshot_url": data.get("screenshot_url"),
                        "timestamp": data.get("timestamp"),
                    },
                    message=result.message,
                )
            else:
                return _error(result.message)

        except Exception as e:
            return _error(f"Page analysis failed: {str(e)}")
