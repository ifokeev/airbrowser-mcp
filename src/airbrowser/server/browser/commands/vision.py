"""Vision-based browser commands using AI models."""

import logging
import math
import time
from typing import Any

from airbrowser.server.browser.smart_targeting import Point, Rect, resolve_detect_target
from airbrowser.server.utils.screenshots import take_screenshot
from airbrowser.server.vision.config import load_vision_settings, resolve_vision_stream
from airbrowser.server.vision.coordinates import detect_element_coordinates
from airbrowser.server.vision.openai_compatible import OpenAICompatibleVisionClient

logger = logging.getLogger(__name__)


def resolve_vision_model(command: dict[str, Any]) -> str:
    """Resolve the model for a single vision request."""
    requested = (command.get("model") or "").strip()
    if requested:
        return requested

    settings = load_vision_settings()
    if settings is None:
        raise RuntimeError("Vision client not configured")

    return settings.model


def _transform_to_screen_coords(driver, coords: dict[str, Any], fx: float = 0.5, fy: float = 0.5) -> dict[str, Any]:
    """Transform screenshot coordinates to screen coordinates.

    Args:
        driver: Selenium driver instance
        coords: Coordinate dict with x, y, width, height, image_size (required)
        fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right)
        fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom)

    Raises:
        ValueError: If image_size is missing from coords
    """
    img_size = coords.get("image_size")
    if not img_size:
        raise ValueError("image_size is required in coords - should be set by detect_element_coordinates")

    img_w = img_size["width"]
    img_h = img_size["height"]

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


def _point_to_payload(point: Point | None) -> dict[str, int] | None:
    if point is None:
        return None
    return {"x": int(round(point.x)), "y": int(round(point.y))}


def _viewport_bbox_from_transform(coords: dict[str, Any]) -> Rect | None:
    transform_info = coords.get("transform_info") or {}
    original = transform_info.get("original") or {}
    scale = transform_info.get("scale") or {}
    try:
        return Rect(
            float(original["x"]) * float(scale["x"]),
            float(original["y"]) * float(scale["y"]),
            float(original["w"]) * float(scale["x"]),
            float(original["h"]) * float(scale["y"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def _hit_test_element_payload(hit_test_result: Any) -> dict[str, Any] | None:
    if hit_test_result is None:
        return None
    return {
        "tag": hit_test_result.tag,
        "text": hit_test_result.text,
        "interactive": hit_test_result.interactive,
    }


def _snap_candidate_payload(candidate: Any) -> dict[str, Any] | None:
    if candidate is None:
        return None
    return {
        "tag": candidate.tag,
        "text": candidate.text,
        "interactive": candidate.interactive,
    }


def _snap_distance_px(resolution: Any) -> float | None:
    if resolution.snap_candidate is None or resolution.original_viewport_point is None:
        return None
    nearest = resolution.snap_candidate.rect.nearest_point(resolution.original_viewport_point)
    return round(
        math.hypot(resolution.original_viewport_point.x - nearest.x, resolution.original_viewport_point.y - nearest.y),
        2,
    )


def _build_resolved_target_payload(resolution: Any) -> dict[str, Any] | None:
    point = _point_to_payload(resolution.resolved_screen_point)
    element = _snap_candidate_payload(resolution.snap_candidate) or _hit_test_element_payload(
        resolution.hit_test_result
    )
    if point is None and element is None:
        return None
    return {"point": point, "element": element}


def _build_snap_result_payload(resolution: Any, strategy: str) -> dict[str, Any]:
    if resolution.snap_candidate is None:
        return {
            "applied": False,
            "strategy": strategy,
            "distance_px": None,
            "snapped_element": None,
            "snapped_point": None,
        }

    return {
        "applied": True,
        "strategy": strategy,
        "distance_px": _snap_distance_px(resolution),
        "snapped_element": _snap_candidate_payload(resolution.snap_candidate),
        "snapped_point": _point_to_payload(resolution.resolved_screen_point),
    }


def _build_detect_debug_payload(coords: dict[str, Any], resolution: Any) -> dict[str, Any]:
    debug = {
        "transform_info": coords.get("transform_info"),
        "original_viewport_point": _point_to_payload(resolution.original_viewport_point),
        "resolved_viewport_point": _point_to_payload(resolution.resolved_viewport_point),
    }
    if resolution.hit_test_result is not None:
        debug["hit_test_result"] = {
            "point": _point_to_payload(resolution.original_screen_point),
            "viewport_point": _point_to_payload(resolution.hit_test_result.viewport_point),
            "element": _hit_test_element_payload(resolution.hit_test_result),
            "reason": resolution.hit_test_result.reason,
            "reason_detail": resolution.hit_test_result.reason_detail,
        }
    if resolution.snap_candidate is not None:
        debug["snap_candidate"] = _snap_candidate_payload(resolution.snap_candidate)
    return debug


def _build_detect_message(prompt: str, resolution: Any) -> str:
    if resolution.outcome_status == "snapped_match":
        return f"Found: {prompt}"
    if resolution.outcome_status == "exact_match":
        return f"Found: {prompt}"
    if resolution.outcome_status == "raw_vision_point":
        return f"Found: {prompt}"
    return resolution.reason_detail or resolution.reason or f"Found: {prompt}"


def handle_detect_coordinates(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Detect element coordinates using vision AI."""
    prompt = command.get("prompt")
    if not prompt:
        return {"status": "error", "message": "Prompt required"}

    # Fractional click offsets (0.0-1.0): 0.5 = center (default)
    fx_explicit = command.get("fx") is not None
    fx = float(command.get("fx", 0.5))
    fy = float(command.get("fy", 0.5))
    hit_test = command.get("hit_test", "off") or "off"
    auto_snap = command.get("auto_snap", "off") or "off"
    snap_radius = float(command.get("snap_radius", 96))
    include_debug = bool(command.get("include_debug", False))
    # Clamp to valid range
    fx = max(0.0, min(1.0, fx))
    fy = max(0.0, min(1.0, fy))

    try:
        screenshot = take_screenshot(driver, browser_id)
        settings = load_vision_settings()
        if settings is None:
            return {"status": "error", "message": "Vision client not configured", "screenshot_url": screenshot["url"]}

        model = resolve_vision_model(command)
        stream = resolve_vision_stream(command.get("stream"), settings)
        coords = detect_element_coordinates(screenshot["path"], prompt, model, stream=stream)

        if coords.get("success"):
            # Auto left-bias for very wide elements (like search boxes with icons)
            # Only apply if fx was not explicitly set
            width = coords.get("width", 0)
            height = coords.get("height", 1)
            aspect_ratio = width / height if height > 0 else 0
            if not fx_explicit and aspect_ratio > 10:
                # Very wide element (e.g., search box) - click left to avoid right-side icons
                fx = 0.25
                logger.debug(f"Auto left-bias: aspect_ratio={aspect_ratio:.1f}, using fx={fx}")

            coords = _transform_to_screen_coords(driver, coords, fx, fy)
            raw_click_point = Point(float(coords["click_point"]["x"]), float(coords["click_point"]["y"]))
            raw_bbox = _viewport_bbox_from_transform(coords)
            resolution = resolve_detect_target(
                driver=driver,
                raw_point=raw_click_point,
                raw_bbox=raw_bbox,
                hit_test_mode=hit_test,
                auto_snap=auto_snap,
                snap_radius=snap_radius,
            )

            coords["outcome_status"] = resolution.outcome_status
            coords["reason"] = resolution.reason
            coords["reason_detail"] = resolution.reason_detail
            coords["resolved_target"] = _build_resolved_target_payload(resolution)
            coords["resolved_click_point"] = _point_to_payload(resolution.resolved_screen_point)
            coords["snap_result"] = _build_snap_result_payload(resolution, auto_snap)
            coords["recommended_next_action"] = resolution.recommended_next_action
            coords["screenshot_url"] = screenshot["url"]
            if include_debug:
                coords["debug"] = _build_detect_debug_payload(coords, resolution)
            return {
                "status": "success",
                "success": resolution.success,
                "message": _build_detect_message(prompt, resolution),
                "coordinates": coords,
            }
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
    try:
        screenshot = take_screenshot(driver, browser_id)
        settings = load_vision_settings()
        if settings is None:
            return {"status": "error", "message": "Vision client not configured", "screenshot_url": screenshot["url"]}

        model = resolve_vision_model(command)
        stream = resolve_vision_stream(command.get("stream"), settings)
        client = OpenAICompatibleVisionClient(base_url=settings.base_url, api_key=settings.api_key, model=model)

        prompt = """Analyze this webpage. Report:
1. FORM FIELDS: inputs (filled/empty), required, validation errors
2. INTERACTIVE: checkboxes, radio buttons, dropdowns, buttons
3. CAPTCHA: present? type? solved?
4. MESSAGES: errors, success, loading
5. PROGRESS: multi-step? current step?
6. PURPOSE: what page? what to do next?

Be specific about field names and states."""

        result = client.explain_screenshot(screenshot["path"], prompt, stream=stream)

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
