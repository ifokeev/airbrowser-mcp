"""Vision-based operations using AI models."""

from typing import Any

from ...models import BrowserAction
from ..browser_pool import BrowserPoolAdapter


class VisionOperations:
    """Handles vision-based AI operations."""

    def __init__(self, browser_pool: BrowserPoolAdapter):
        self.browser_pool = browser_pool

    def detect_coordinates(self, browser_id: str, prompt: str) -> dict[str, Any]:
        """
        Detect element coordinates using vision models without clicking.

        Args:
            browser_id: Browser instance identifier
            prompt: Natural language description of element to find

        Returns:
            Dictionary with coordinate information
        """
        try:
            options = {"prompt": prompt}
            action = BrowserAction(action="detect_coordinates", options=options)
            result = self.browser_pool.execute_action(browser_id, action)

            if result.success:
                coord_data = result.data.get("coordinates", {}) if isinstance(result.data, dict) else {}
                return {
                    "success": True,
                    "message": result.message,
                    "prompt": prompt,
                    "coordinates": coord_data,
                    "screenshot_path": coord_data.get("screenshot_path"),
                    "model_used": coord_data.get("model_used"),
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
                    "data": result.to_dict(),
                }
            else:
                return {
                    "success": False,
                    "error": result.message,
                    "prompt": prompt,
                    "models_tried": (result.data.get("models_tried") if isinstance(result.data, dict) else []),
                    "screenshot_path": (result.data.get("screenshot_path") if isinstance(result.data, dict) else None),
                }

        except Exception as e:
            return {"success": False, "error": f"Coordinate detection failed: {str(e)}", "prompt": prompt}

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
                return {
                    "success": True,
                    "message": result.message,
                    "analysis": data.get("analysis"),
                    "model": data.get("model"),
                    "screenshot_url": data.get("screenshot_url"),
                    "timestamp": data.get("timestamp"),
                }
            else:
                return {
                    "success": False,
                    "error": result.message,
                    "screenshot_url": (result.data.get("screenshot_url") if isinstance(result.data, dict) else None),
                }

        except Exception as e:
            return {"success": False, "error": f"Page analysis failed: {str(e)}"}
