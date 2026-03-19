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
        self,
        browser_id: str,
        prompt: str,
        fx: float | None = None,
        fy: float | None = None,
        model: str | None = None,
        hit_test: str = "off",
        auto_snap: str = "off",
        snap_radius: float = 96,
        include_debug: bool = False,
    ) -> dict[str, Any]:
        """
        Detect element coordinates using vision models without clicking.

        Args:
            browser_id: Browser instance identifier
            prompt: Natural language description of element to find
            fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right).
                If None, auto-bias is applied for wide elements (0.25 for aspect ratio > 10).
            fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom).
            model: Optional vision model override for this request.
            hit_test: Detect-time validation mode: off, warn, or strict.
            auto_snap: Auto-snap mode: off, nearest_clickable, or nearest_interactive.
            snap_radius: Maximum snap radius in CSS pixels.
            include_debug: Include debug diagnostics when available.

        Returns:
            Dictionary with coordinate information
        """
        # Only include fx/fy if explicitly set - allows vision handler to apply auto-bias
        options: dict[str, Any] = {"prompt": prompt}
        if fx is not None:
            options["fx"] = fx
        if fy is not None:
            options["fy"] = fy
        if model is not None:
            options["model"] = model
        options["hit_test"] = hit_test
        options["auto_snap"] = auto_snap
        options["snap_radius"] = snap_radius
        options["include_debug"] = include_debug
        action = BrowserAction(action="detect_coordinates", options=options)
        result = self.browser_pool.execute_action(browser_id, action)

        raw_data = result.data if isinstance(result.data, dict) else {}
        coord_data = raw_data.get("coordinates", {}) if isinstance(raw_data, dict) else {}
        detect_data = {
            "prompt": prompt,
            "screenshot_url": coord_data.get("screenshot_url"),
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
            "outcome_status": coord_data.get("outcome_status"),
            "reason": coord_data.get("reason"),
            "reason_detail": coord_data.get("reason_detail"),
            "resolved_target": coord_data.get("resolved_target"),
            "resolved_click_point": coord_data.get("resolved_click_point"),
            "snap_result": coord_data.get("snap_result"),
            "recommended_next_action": coord_data.get("recommended_next_action"),
            "image_size": coord_data.get("image_size"),
            "transform_info": coord_data.get("transform_info"),
        }
        if coord_data.get("debug") is not None:
            detect_data["debug"] = coord_data.get("debug")

        outcome_status = coord_data.get("outcome_status")
        logical_success = result.success
        if isinstance(outcome_status, str):
            logical_success = not outcome_status.startswith("fail_")
        elif isinstance(raw_data.get("success"), bool):
            logical_success = raw_data["success"]

        if logical_success:
            return _success(data=detect_data, message=result.message)
        if coord_data:
            return {"success": False, "message": result.message, "data": detect_data}
        return _error(result.message)

    def what_is_visible(self, browser_id: str, model: str | None = None) -> dict[str, Any]:
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
            model: Optional vision model override for this request.

        Returns:
            Dictionary with comprehensive page state analysis
        """
        try:
            options = {"model": model} if model is not None else {}
            action = BrowserAction(action="what_is_visible", options=options)
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
