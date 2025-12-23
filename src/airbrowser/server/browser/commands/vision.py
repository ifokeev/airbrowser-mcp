"""Vision-based browser commands using AI models."""

import logging
import os
import time
from typing import Any

from airbrowser.server.utils.screenshots import take_screenshot
from airbrowser.server.vision.coordinates import detect_element_coordinates
from airbrowser.server.vision.openrouter import OpenRouterClient

logger = logging.getLogger(__name__)

DEFAULT_COORD_MODEL = "google/gemini-3-flash-preview"
DEFAULT_ANALYSIS_MODEL = "google/gemini-3-flash-preview"


def _get_model(command: dict, env_var: str, default: str) -> str:
    """Get model from command, env, or default."""
    return command.get("model") or os.getenv(env_var, default)


def _transform_to_screen_coords(driver, coords: dict[str, Any]) -> dict[str, Any]:
    """Transform screenshot coordinates to screen coordinates."""
    img_size = coords.get("image_size", {})
    img_w = img_size.get("width", 1920)
    img_h = img_size.get("height", 1080)

    try:
        wrect = driver.get_window_rect()
        win_x, win_y = float(wrect.get("x", 0)), float(wrect.get("y", 0))
        win_h = float(wrect.get("height", 0))

        viewport_w = float(driver.execute_script("return window.innerWidth;"))
        viewport_h = float(driver.execute_script("return window.innerHeight;"))

        scale_x = viewport_w / img_w if img_w > 0 else 1.0
        scale_y = viewport_h / img_h if img_h > 0 else 1.0

        screen_x = win_x + coords["x"] * scale_x
        screen_y = (win_y + win_h - viewport_h) + coords["y"] * scale_y
        width = int(coords["width"] * scale_x)
        height = int(coords["height"] * scale_y)

        coords["x"] = int(screen_x)
        coords["y"] = int(screen_y)
        coords["width"] = width
        coords["height"] = height
        coords["click_point"] = {
            "x": int(screen_x + width / 2),
            "y": int(screen_y + height / 2),
        }
    except Exception as e:
        logger.warning(f"Coordinate transform failed: {e}")
        coords["click_point"] = {
            "x": coords["x"] + coords["width"] // 2,
            "y": coords["y"] + coords["height"] // 2,
        }

    return coords


def handle_detect_coordinates(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Detect element coordinates using vision AI."""
    prompt = command.get("prompt")
    if not prompt:
        return {"success": False, "error": "Prompt required"}

    model = _get_model(command, "OPENROUTER_COORD_MODEL", DEFAULT_COORD_MODEL)

    try:
        screenshot = take_screenshot(driver, browser_id)
        coords = detect_element_coordinates(screenshot["path"], prompt, model)

        if coords.get("success"):
            coords = _transform_to_screen_coords(driver, coords)
            coords["screenshot_url"] = screenshot["url"]
            return {"success": True, "message": f"Found: {prompt}", "coordinates": coords}
        else:
            return {
                "success": False,
                "error": coords.get("error", "Element not found"),
                "screenshot_url": screenshot["url"],
            }

    except Exception as e:
        logger.error(f"Coordinate detection failed: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


def handle_what_is_visible(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Page state analysis using AI vision."""
    model = _get_model(command, "OPENROUTER_ANALYSIS_MODEL", DEFAULT_ANALYSIS_MODEL)

    try:
        screenshot = take_screenshot(driver, browser_id)
        client = OpenRouterClient(model=model)

        if not client.is_available():
            return {"success": False, "error": "OpenRouter not available", "screenshot_url": screenshot["url"]}

        prompt = """Analyze this webpage. Report:
1. FORM FIELDS: inputs (filled/empty), required, validation errors
2. INTERACTIVE: checkboxes, radio buttons, dropdowns, buttons
3. CAPTCHA: present? type? solved?
4. MESSAGES: errors, success, loading
5. PROGRESS: multi-step? current step?
6. PURPOSE: what page? what to do next?

Be specific about field names and states."""

        result = client.explain_screenshot(screenshot["path"], prompt)

        if result.get("success"):
            return {
                "success": True,
                "message": "Page analyzed",
                "analysis": result.get("explanation"),
                "model": model,
                "screenshot_url": screenshot["url"],
                "timestamp": time.time(),
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Vision error"),
                "screenshot_url": screenshot["url"],
            }

    except Exception as e:
        logger.error(f"Page analysis failed: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
