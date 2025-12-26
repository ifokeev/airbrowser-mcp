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


def _transform_to_screen_coords(driver, coords: dict[str, Any], fx: float = 0.5, fy: float = 0.5) -> dict[str, Any]:
    """Transform screenshot coordinates to screen coordinates.

    Args:
        driver: Selenium driver instance
        coords: Coordinate dict with x, y, width, height, image_size
        fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right)
        fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom)
    """
    img_size = coords.get("image_size", {})
    img_w = img_size.get("width", 1920)
    img_h = img_size.get("height", 1080)

    # Store original coordinates for debugging
    original_x, original_y = coords["x"], coords["y"]
    original_w, original_h = coords["width"], coords["height"]

    try:
        wrect = driver.get_window_rect()
        win_x, win_y = float(wrect.get("x", 0)), float(wrect.get("y", 0))
        win_w = float(wrect.get("width", 0))
        win_h = float(wrect.get("height", 0))

        viewport_w = float(driver.execute_script("return window.innerWidth;"))
        viewport_h = float(driver.execute_script("return window.innerHeight;"))

        # Chrome offset (title bar, toolbar height)
        chrome_offset_y = win_h - viewport_h

        scale_x = viewport_w / img_w if img_w > 0 else 1.0
        scale_y = viewport_h / img_h if img_h > 0 else 1.0

        screen_x = win_x + coords["x"] * scale_x
        screen_y = (win_y + chrome_offset_y) + coords["y"] * scale_y
        width = int(coords["width"] * scale_x)
        height = int(coords["height"] * scale_y)

        coords["x"] = int(screen_x)
        coords["y"] = int(screen_y)
        coords["width"] = width
        coords["height"] = height
        coords["click_point"] = {
            "x": int(screen_x + width * fx),
            "y": int(screen_y + height * fy),
        }

        # Add transform debug info
        coords["transform_info"] = {
            "original": {"x": original_x, "y": original_y, "w": original_w, "h": original_h},
            "window_rect": {"x": win_x, "y": win_y, "w": win_w, "h": win_h},
            "viewport": {"w": viewport_w, "h": viewport_h},
            "chrome_offset_y": chrome_offset_y,
            "scale": {"x": scale_x, "y": scale_y},
        }

        logger.debug(
            f"Transform: original({original_x},{original_y}) -> screen({coords['x']},{coords['y']}), "
            f"window({win_x},{win_y},{win_w}x{win_h}), viewport({viewport_w}x{viewport_h}), "
            f"chrome_offset={chrome_offset_y}"
        )
    except Exception as e:
        logger.warning(f"Coordinate transform failed: {e}")
        coords["click_point"] = {
            "x": int(coords["x"] + coords["width"] * fx),
            "y": int(coords["y"] + coords["height"] * fy),
        }

    return coords


def handle_detect_coordinates(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Detect element coordinates using vision AI."""
    prompt = command.get("prompt")
    if not prompt:
        return {"status": "error", "message": "Prompt required"}

    # Fractional click offsets (0.0-1.0): 0.5 = center (default)
    fx_explicit = command.get("fx") is not None
    fy_explicit = command.get("fy") is not None
    fx = float(command.get("fx", 0.5))
    fy = float(command.get("fy", 0.5))
    # Clamp to valid range
    fx = max(0.0, min(1.0, fx))
    fy = max(0.0, min(1.0, fy))

    model = _get_model(command, "OPENROUTER_COORD_MODEL", DEFAULT_COORD_MODEL)

    try:
        screenshot = take_screenshot(driver, browser_id)
        coords = detect_element_coordinates(screenshot["path"], prompt, model)

        if coords.get("success"):
            # Auto left-bias for very wide elements (like search boxes with icons)
            # Only apply if fx was not explicitly set
            if not fx_explicit:
                width = coords.get("width", 0)
                height = coords.get("height", 1)
                aspect_ratio = width / height if height > 0 else 0
                if aspect_ratio > 10:  # Very wide element (e.g., search box)
                    fx = 0.25  # Click at 25% from left to avoid right-side icons
                    logger.debug(f"Auto left-bias: aspect_ratio={aspect_ratio:.1f}, using fx={fx}")

            coords = _transform_to_screen_coords(driver, coords, fx, fy)
            coords["screenshot_url"] = screenshot["url"]
            return {"status": "success", "message": f"Found: {prompt}", "coordinates": coords}
        else:
            return {
                "status": "error",
                "message": coords.get("error", "Element not found"),
                "screenshot_url": screenshot["url"],
            }

    except Exception as e:
        logger.error(f"Coordinate detection failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def handle_what_is_visible(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Page state analysis using AI vision."""
    model = _get_model(command, "OPENROUTER_ANALYSIS_MODEL", DEFAULT_ANALYSIS_MODEL)

    try:
        screenshot = take_screenshot(driver, browser_id)
        client = OpenRouterClient(model=model)

        if not client.is_available():
            return {"status": "error", "message": "OpenRouter not available", "screenshot_url": screenshot["url"]}

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
                "status": "success",
                "message": "Page analyzed",
                "analysis": result.get("explanation"),
                "model": model,
                "screenshot_url": screenshot["url"],
                "timestamp": time.time(),
            }
        else:
            return {
                "status": "error",
                "message": result.get("error", "Vision error"),
                "screenshot_url": screenshot["url"],
            }

    except Exception as e:
        logger.error(f"Page analysis failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
