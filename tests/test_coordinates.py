#!/usr/bin/env python3
"""
Tests for coordinate detection and transformation logic.

These are unit tests that test the coordinate logic in isolation.
The actual functions are copied here to avoid complex import chains.

Tests:
- Gemini coordinate normalization (0-1000 to pixels)
- Coordinate bounds clamping
- Screen coordinate transformation

Run with: pytest tests/test_coordinates.py -v
"""

import json
import logging
import re
from typing import Any
from unittest.mock import MagicMock

# ============================================================================
# Copied from src/airbrowser/server/vision/coordinates.py
# These are pure functions that can be tested in isolation
# ============================================================================


def _normalize_gemini_coords(coords: dict[str, Any], img_w: int, img_h: int) -> dict[str, Any]:
    """Convert Gemini's 0-1000 normalized coordinates to pixels."""
    if not coords.get("success"):
        return coords
    try:
        coords["x"] = int(coords["x"] / 1000.0 * img_w)
        coords["y"] = int(coords["y"] / 1000.0 * img_h)
        coords["width"] = int(coords["width"] / 1000.0 * img_w)
        coords["height"] = int(coords["height"] / 1000.0 * img_h)
    except Exception as e:
        logging.warning(f"Failed to normalize Gemini coordinates: {e}")
    return coords


def _clamp_to_image_bounds(coords: dict[str, Any], img_w: int, img_h: int) -> dict[str, Any]:
    """Clamp coordinates to stay within image bounds."""
    if not coords.get("success"):
        return coords

    x, y = coords.get("x", 0), coords.get("y", 0)
    w, h = coords.get("width", 0), coords.get("height", 0)

    # Check if element is significantly outside viewport (more than 50% hidden)
    visible_h = min(y + h, img_h) - max(y, 0)
    visible_w = min(x + w, img_w) - max(x, 0)
    if visible_h < h * 0.5 or visible_w < w * 0.5:
        coords["partially_visible"] = True
        coords["visibility_warning"] = "Element is mostly off-screen, may need to scroll"

    # Clamp to image bounds
    coords["x"] = max(0, min(x, img_w - 1))
    coords["y"] = max(0, min(y, img_h - 1))
    # Ensure width/height don't extend past image
    coords["width"] = min(w, img_w - coords["x"])
    coords["height"] = min(h, img_h - coords["y"])

    return coords


def _parse_response(response: str) -> dict[str, Any]:
    """Parse vision model response to extract coordinates."""
    try:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            if data.get("found"):
                return {
                    "success": True,
                    "x": int(data.get("x", 0)),
                    "y": int(data.get("y", 0)),
                    "width": int(data.get("width", 0)),
                    "height": int(data.get("height", 0)),
                    "confidence": float(data.get("confidence", 0.0)),
                    "element_description": data.get("element", ""),
                }
            return {"success": False, "error": data.get("error", "Element not found")}

        # Fallback: extract numbers from text
        numbers = re.findall(r"\b\d+\b", response)
        if len(numbers) >= 4:
            return {
                "success": True,
                "x": int(numbers[0]),
                "y": int(numbers[1]),
                "width": int(numbers[2]),
                "height": int(numbers[3]),
                "confidence": 0.7,
                "element_description": "Parsed from text",
            }
    except Exception as e:
        logging.error(f"Failed to parse response: {e}")

    return {"success": False, "error": f"Could not parse: {response[:200]}..."}


# ============================================================================
# Copied from src/airbrowser/server/browser/commands/vision.py
# ============================================================================


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
    except Exception as e:
        logging.warning(f"Coordinate transform failed: {e}")
        coords["click_point"] = {
            "x": int(coords["x"] + coords["width"] * fx),
            "y": int(coords["y"] + coords["height"] * fy),
        }

    return coords


# ============================================================================
# Tests
# ============================================================================


class TestGeminiCoordinateNormalization:
    """Tests for Gemini 0-1000 normalized coordinate conversion."""

    def test_normalize_center_element(self):
        """Test normalizing coordinates for center element."""
        # Gemini returns 0-1000 normalized coords
        coords = {
            "success": True,
            "x": 500,  # center x in 0-1000
            "y": 500,  # center y in 0-1000
            "width": 100,
            "height": 50,
        }

        # Image is 1920x1080
        result = _normalize_gemini_coords(coords, 1920, 1080)

        assert result["x"] == 960  # 500/1000 * 1920
        assert result["y"] == 540  # 500/1000 * 1080
        assert result["width"] == 192  # 100/1000 * 1920
        assert result["height"] == 54  # 50/1000 * 1080

    def test_normalize_top_left(self):
        """Test normalizing coordinates for top-left element."""
        coords = {
            "success": True,
            "x": 0,
            "y": 0,
            "width": 100,
            "height": 100,
        }

        result = _normalize_gemini_coords(coords, 1920, 1080)

        assert result["x"] == 0
        assert result["y"] == 0

    def test_normalize_bottom_right(self):
        """Test normalizing coordinates for bottom-right element."""
        coords = {
            "success": True,
            "x": 900,  # near right edge
            "y": 900,  # near bottom edge
            "width": 100,
            "height": 100,
        }

        result = _normalize_gemini_coords(coords, 1920, 1080)

        assert result["x"] == 1728  # 900/1000 * 1920
        assert result["y"] == 972  # 900/1000 * 1080

    def test_normalize_skips_failed_coords(self):
        """Test that normalization is skipped for failed detection."""
        coords = {"success": False, "error": "Not found"}
        result = _normalize_gemini_coords(coords, 1920, 1080)

        assert result["success"] is False
        assert "x" not in result


class TestCoordinateClamping:
    """Tests for coordinate bounds clamping."""

    def test_clamp_coordinates_within_bounds(self):
        """Test that valid coordinates are unchanged."""
        coords = {
            "success": True,
            "x": 100,
            "y": 100,
            "width": 200,
            "height": 50,
        }

        result = _clamp_to_image_bounds(coords, 1920, 1080)

        assert result["x"] == 100
        assert result["y"] == 100
        assert result["width"] == 200
        assert result["height"] == 50
        assert "partially_visible" not in result

    def test_clamp_element_extending_past_right_edge(self):
        """Test clamping element that extends past right edge."""
        coords = {
            "success": True,
            "x": 1800,
            "y": 100,
            "width": 200,  # extends to 2000, past 1920
            "height": 50,
        }

        result = _clamp_to_image_bounds(coords, 1920, 1080)

        assert result["x"] == 1800
        assert result["width"] == 120  # clamped to fit within 1920

    def test_clamp_element_extending_past_bottom_edge(self):
        """Test clamping element that extends past bottom edge."""
        coords = {
            "success": True,
            "x": 100,
            "y": 1000,
            "width": 200,
            "height": 100,  # extends to 1100, past 1080
        }

        result = _clamp_to_image_bounds(coords, 1920, 1080)

        assert result["y"] == 1000
        assert result["height"] == 80  # clamped to fit within 1080

    def test_clamp_element_mostly_offscreen_adds_warning(self):
        """Test that mostly off-screen elements get a warning."""
        # Element at y=1050 with height=100 is mostly below viewport
        coords = {
            "success": True,
            "x": 100,
            "y": 1050,  # only 30px visible in 1080 viewport
            "width": 200,
            "height": 100,
        }

        result = _clamp_to_image_bounds(coords, 1920, 1080)

        assert result["partially_visible"] is True
        assert "visibility_warning" in result

    def test_clamp_element_at_exact_bottom_edge(self):
        """Test element at exact bottom edge of viewport."""
        # Element with bottom at exactly 837 (viewport height)
        coords = {
            "success": True,
            "x": 100,
            "y": 800,
            "width": 200,
            "height": 37,  # bottom at y=837
        }

        result = _clamp_to_image_bounds(coords, 1920, 837)

        assert result["y"] == 800
        assert result["height"] == 37
        assert "partially_visible" not in result

    def test_clamp_google_search_button_case(self):
        """Test the specific case that caused the Google Lens bug."""
        # This was the actual failing case: y=832, height=40 in 837-height image
        coords = {
            "success": True,
            "x": 1222,
            "y": 832,
            "width": 87,
            "height": 40,  # bottom at y=872, past 837
        }

        result = _clamp_to_image_bounds(coords, 1912, 837)

        # Should clamp height to stay within bounds
        assert result["y"] == 832
        assert result["height"] == 5  # clamped: 837 - 832 = 5
        assert result["partially_visible"] is True  # only 5/40 = 12.5% visible

    def test_clamp_skips_failed_coords(self):
        """Test that clamping is skipped for failed detection."""
        coords = {"success": False, "error": "Not found"}
        result = _clamp_to_image_bounds(coords, 1920, 1080)

        assert result["success"] is False


class TestScreenCoordinateTransform:
    """Tests for screen coordinate transformation."""

    def _create_mock_driver(self, win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080):
        """Create a mock driver with specified window/viewport dimensions."""
        driver = MagicMock()
        driver.get_window_rect.return_value = {"x": win_x, "y": win_y, "width": win_w, "height": win_h}
        driver.execute_script.side_effect = lambda script: {
            "return window.innerWidth;": viewport_w,
            "return window.innerHeight;": viewport_h,
        }.get(script)
        return driver

    def test_transform_no_offset_no_scale(self):
        """Test transform when window matches viewport (headless mode)."""
        driver = self._create_mock_driver(win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080)

        coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords)

        # No offset, no scale - coordinates unchanged
        assert result["x"] == 500
        assert result["y"] == 300
        assert result["click_point"]["x"] == 550  # 500 + 100/2
        assert result["click_point"]["y"] == 325  # 300 + 50/2

    def test_transform_with_chrome_offset(self):
        """Test transform when browser has chrome (title bar, toolbar)."""
        # Window is 1080 tall but viewport is only 900 (180px chrome)
        driver = self._create_mock_driver(win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=900)

        coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 900}}

        result = _transform_to_screen_coords(driver, coords)

        # Y should be offset by chrome height (180)
        assert result["x"] == 500
        assert result["y"] == 480  # 300 + 180
        assert result["click_point"]["y"] == 505  # 480 + 25

    def test_transform_with_window_position(self):
        """Test transform when window is not at (0,0)."""
        driver = self._create_mock_driver(win_x=100, win_y=50, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080)

        coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords)

        # Should add window position offset
        assert result["x"] == 600  # 500 + 100
        assert result["y"] == 350  # 300 + 50

    def test_transform_with_scale(self):
        """Test transform when screenshot size differs from viewport."""
        driver = self._create_mock_driver(win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080)

        # Screenshot is half the size of viewport
        coords = {"x": 250, "y": 150, "width": 50, "height": 25, "image_size": {"width": 960, "height": 540}}

        result = _transform_to_screen_coords(driver, coords)

        # Coordinates should be scaled up 2x
        assert result["x"] == 500  # 250 * 2
        assert result["y"] == 300  # 150 * 2
        assert result["width"] == 100  # 50 * 2
        assert result["height"] == 50  # 25 * 2

    def test_transform_includes_debug_info(self):
        """Test that transform includes debug info."""
        driver = self._create_mock_driver()

        coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords)

        assert "transform_info" in result
        assert "original" in result["transform_info"]
        assert "window_rect" in result["transform_info"]
        assert "viewport" in result["transform_info"]
        assert "chrome_offset_y" in result["transform_info"]
        assert "scale" in result["transform_info"]

    def test_transform_handles_exception(self):
        """Test that transform handles driver exceptions gracefully."""
        driver = MagicMock()
        driver.get_window_rect.side_effect = Exception("Driver error")

        coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords)

        # Should fall back to simple center calculation
        assert result["click_point"]["x"] == 550  # 500 + 100/2
        assert result["click_point"]["y"] == 325  # 300 + 50/2

    def test_transform_wide_element_clicks_center(self):
        """Test that wide elements still click at center."""
        driver = self._create_mock_driver(win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080)

        # Wide search box like Google's (1112px wide)
        coords = {"x": 400, "y": 300, "width": 1112, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords)

        # Always click at center, regardless of width
        # click_x = 400 + 1112/2 = 400 + 556 = 956
        assert result["click_point"]["x"] == 956
        assert result["click_point"]["y"] == 325  # 300 + 50/2


class TestResponseParsing:
    """Tests for vision model response parsing."""

    def test_parse_valid_json_response(self):
        """Test parsing valid JSON response."""
        response = (
            '{"found": true, "element": "button", "x": 100, "y": 200, "width": 50, "height": 30, "confidence": 0.95}'
        )
        result = _parse_response(response)

        assert result["success"] is True
        assert result["x"] == 100
        assert result["y"] == 200
        assert result["confidence"] == 0.95

    def test_parse_json_with_surrounding_text(self):
        """Test parsing JSON embedded in text."""
        response = 'Here is the result: {"found": true, "x": 100, "y": 200, "width": 50, "height": 30, "confidence": 0.9} Hope this helps!'
        result = _parse_response(response)

        assert result["success"] is True
        assert result["x"] == 100

    def test_parse_not_found_response(self):
        """Test parsing not found response."""
        response = '{"found": false, "error": "Element not visible"}'
        result = _parse_response(response)

        assert result["success"] is False
        assert result["error"] == "Element not visible"

    def test_parse_fallback_numbers(self):
        """Test fallback to extracting numbers from text."""
        response = "The element is at position 100 200 with size 50 30"
        result = _parse_response(response)

        assert result["success"] is True
        assert result["x"] == 100
        assert result["y"] == 200
        assert result["width"] == 50
        assert result["height"] == 30
        assert result["confidence"] == 0.7  # default for fallback


class TestFractionalClickOffset:
    """Tests for fx/fy fractional click offset parameters."""

    def _create_mock_driver(self, win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080):
        """Create a mock driver with specified window/viewport dimensions."""
        driver = MagicMock()
        driver.get_window_rect.return_value = {"x": win_x, "y": win_y, "width": win_w, "height": win_h}
        driver.execute_script.side_effect = lambda script: {
            "return window.innerWidth;": viewport_w,
            "return window.innerHeight;": viewport_h,
        }.get(script)
        return driver

    def test_fx_left_clicks_at_20_percent(self):
        """Test fx=0.2 clicks at 20% from left edge."""
        driver = self._create_mock_driver()

        coords = {"x": 400, "y": 300, "width": 1000, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords, fx=0.2, fy=0.5)

        # click_x = 400 + 1000 * 0.2 = 400 + 200 = 600
        assert result["click_point"]["x"] == 600
        # click_y = 300 + 50 * 0.5 = 300 + 25 = 325
        assert result["click_point"]["y"] == 325

    def test_fx_right_clicks_at_80_percent(self):
        """Test fx=0.8 clicks at 80% from left edge."""
        driver = self._create_mock_driver()

        coords = {"x": 400, "y": 300, "width": 1000, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords, fx=0.8, fy=0.5)

        # click_x = 400 + 1000 * 0.8 = 400 + 800 = 1200
        assert result["click_point"]["x"] == 1200
        assert result["click_point"]["y"] == 325

    def test_fy_top_clicks_at_20_percent(self):
        """Test fy=0.2 clicks at 20% from top edge."""
        driver = self._create_mock_driver()

        coords = {"x": 400, "y": 300, "width": 100, "height": 100, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords, fx=0.5, fy=0.2)

        # click_x = 400 + 100 * 0.5 = 450
        assert result["click_point"]["x"] == 450
        # click_y = 300 + 100 * 0.2 = 320
        assert result["click_point"]["y"] == 320

    def test_default_fx_fy_is_center(self):
        """Test that default fx=0.5, fy=0.5 clicks at center."""
        driver = self._create_mock_driver()

        coords = {"x": 400, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        # Test with no fx/fy (defaults)
        result = _transform_to_screen_coords(driver, coords)

        # click_x = 400 + 100 * 0.5 = 450
        assert result["click_point"]["x"] == 450
        # click_y = 300 + 50 * 0.5 = 325
        assert result["click_point"]["y"] == 325

    def test_google_search_box_with_fx_02(self):
        """Test Google search box scenario: fx=0.2 avoids right-side icons."""
        # Use matching viewport/image size to avoid scale factor
        driver = self._create_mock_driver(viewport_w=1912, viewport_h=837, win_h=837)

        # Google search box dimensions from actual log
        coords = {"x": 659, "y": 555, "width": 1074, "height": 38, "image_size": {"width": 1912, "height": 837}}

        # With fx=0.5 (center), would click at x = 659 + 1074*0.5 = 1196 (hits Google Lens)
        result_center = _transform_to_screen_coords(driver, coords.copy(), fx=0.5, fy=0.5)
        assert result_center["click_point"]["x"] == 1196

        # With fx=0.2, clicks at x = 659 + 1074*0.2 = 659 + 214 = 873 (hits text input)
        result_left = _transform_to_screen_coords(driver, coords.copy(), fx=0.2, fy=0.5)
        assert result_left["click_point"]["x"] == 873

    def test_fx_fy_edge_cases(self):
        """Test edge cases: fx=0.0 and fx=1.0."""
        driver = self._create_mock_driver()

        coords = {"x": 100, "y": 200, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        # fx=0.0 clicks at left edge
        result = _transform_to_screen_coords(driver, coords.copy(), fx=0.0, fy=0.5)
        assert result["click_point"]["x"] == 100  # 100 + 100*0.0 = 100

        # fx=1.0 clicks at right edge
        result = _transform_to_screen_coords(driver, coords.copy(), fx=1.0, fy=0.5)
        assert result["click_point"]["x"] == 200  # 100 + 100*1.0 = 200

    def test_fallback_uses_fx_fy(self):
        """Test that fallback (exception case) also uses fx/fy."""
        driver = MagicMock()
        driver.get_window_rect.side_effect = Exception("Driver error")

        coords = {"x": 400, "y": 300, "width": 1000, "height": 50, "image_size": {"width": 1920, "height": 1080}}

        result = _transform_to_screen_coords(driver, coords, fx=0.2, fy=0.5)

        # Fallback: click_x = 400 + 1000 * 0.2 = 600
        assert result["click_point"]["x"] == 600
        # Fallback: click_y = 300 + 50 * 0.5 = 325
        assert result["click_point"]["y"] == 325


# ============================================================================
# Auto-bias logic from src/airbrowser/server/browser/commands/vision.py
# This logic applies fx=0.25 for wide elements when fx is not explicitly set
# ============================================================================


def _apply_auto_bias(command: dict, coords: dict) -> tuple[float, float]:
    """
    Apply auto-bias for wide elements.

    Returns the fx, fy values to use for click point calculation.
    If fx/fy are explicitly set in command, uses those.
    If not set and element is very wide (aspect ratio > 10), applies left-bias (fx=0.25).
    """
    fx_explicit = command.get("fx") is not None
    fx = float(command.get("fx", 0.5))
    fy = float(command.get("fy", 0.5))

    # Clamp to valid range
    fx = max(0.0, min(1.0, fx))
    fy = max(0.0, min(1.0, fy))

    if coords.get("success"):
        width = coords.get("width", 0)
        height = coords.get("height", 1)
        aspect_ratio = width / height if height > 0 else 0

        if not fx_explicit and aspect_ratio > 10:
            # Very wide element (e.g., search box) - click left to avoid right-side icons
            fx = 0.25

    return fx, fy


class TestAutoBiasForWideElements:
    """Tests for auto-bias logic that adjusts click position for wide elements.

    This prevents clicking on icons at the right side of wide elements like
    Google's search box (which has camera/voice icons on the right).

    The auto-bias applies fx=0.25 (25% from left) when:
    - fx is NOT explicitly set by the caller
    - Element aspect ratio > 10 (very wide element)
    """

    def test_wide_element_without_explicit_fx_gets_auto_bias(self):
        """Wide element (aspect ratio > 10) without explicit fx should use fx=0.25."""
        # Google search box: 1074px wide, 38px tall = aspect ratio 28.3
        command = {"prompt": "search box"}  # No fx/fy
        coords = {"success": True, "width": 1074, "height": 38}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.25, "Wide element should get auto-bias fx=0.25"
        assert fy == 0.5, "fy should remain at center"

    def test_wide_element_with_explicit_fx_uses_explicit_value(self):
        """Wide element with explicit fx should use the explicit value, not auto-bias."""
        command = {"prompt": "search box", "fx": 0.8}  # Explicit fx
        coords = {"success": True, "width": 1074, "height": 38}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.8, "Explicit fx should be used, not auto-bias"
        assert fy == 0.5

    def test_narrow_element_without_explicit_fx_uses_center(self):
        """Narrow element (aspect ratio <= 10) should use center (fx=0.5)."""
        # Button: 100px wide, 40px tall = aspect ratio 2.5
        command = {"prompt": "submit button"}  # No fx/fy
        coords = {"success": True, "width": 100, "height": 40}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.5, "Narrow element should use center (fx=0.5)"
        assert fy == 0.5

    def test_aspect_ratio_exactly_10_uses_center(self):
        """Element with aspect ratio exactly 10 should use center (threshold is > 10)."""
        command = {"prompt": "element"}
        coords = {"success": True, "width": 400, "height": 40}  # ratio = 10.0

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.5, "Aspect ratio exactly 10 should use center"

    def test_aspect_ratio_just_over_10_gets_auto_bias(self):
        """Element with aspect ratio just over 10 should get auto-bias."""
        command = {"prompt": "element"}
        coords = {"success": True, "width": 401, "height": 40}  # ratio = 10.025

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.25, "Aspect ratio > 10 should get auto-bias"

    def test_failed_detection_returns_defaults(self):
        """Failed detection should return default values."""
        command = {"prompt": "element"}
        coords = {"success": False, "error": "Not found"}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.5, "Failed detection should use default center"
        assert fy == 0.5

    def test_explicit_fx_zero_is_honored(self):
        """Explicit fx=0.0 should be honored, not treated as 'not set'."""
        command = {"prompt": "element", "fx": 0.0}
        coords = {"success": True, "width": 1074, "height": 38}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.0, "Explicit fx=0.0 should be honored"

    def test_explicit_fy_is_honored(self):
        """Explicit fy should be honored."""
        command = {"prompt": "element", "fy": 0.2}
        coords = {"success": True, "width": 1074, "height": 38}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.25, "Auto-bias should still apply to fx"
        assert fy == 0.2, "Explicit fy should be honored"

    def test_fx_clamped_to_valid_range(self):
        """fx values outside 0-1 range should be clamped."""
        command = {"prompt": "element", "fx": 1.5}
        coords = {"success": True, "width": 100, "height": 40}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 1.0, "fx > 1.0 should be clamped to 1.0"

    def test_negative_fx_clamped_to_zero(self):
        """Negative fx should be clamped to 0."""
        command = {"prompt": "element", "fx": -0.5}
        coords = {"success": True, "width": 100, "height": 40}

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.0, "Negative fx should be clamped to 0.0"

    def test_zero_height_element_no_crash(self):
        """Element with zero height should not cause division by zero."""
        command = {"prompt": "element"}
        coords = {"success": True, "width": 100, "height": 0}

        fx, fy = _apply_auto_bias(command, coords)

        # Should not crash, and should use default center
        assert fx == 0.5
        assert fy == 0.5

    def test_google_search_box_real_dimensions(self):
        """Test with actual Google search box dimensions from production logs."""
        # From actual failed click that hit Google Lens icon
        command = {"prompt": "the text input area of the search box"}
        coords = {
            "success": True,
            "x": 659,
            "y": 555,
            "width": 1074,  # Very wide
            "height": 38,
            # Aspect ratio = 1074/38 = 28.3
        }

        fx, fy = _apply_auto_bias(command, coords)

        assert fx == 0.25, "Google search box should get auto-bias"
        # With fx=0.25: click_x = 659 + 1074*0.25 = 659 + 268 = 927 (text input area)
        # With fx=0.5:  click_x = 659 + 1074*0.5 = 659 + 537 = 1196 (Google Lens icon!)
        expected_click_x_with_auto_bias = 659 + int(1074 * 0.25)
        expected_click_x_without_auto_bias = 659 + int(1074 * 0.5)
        assert (
            expected_click_x_with_auto_bias < expected_click_x_without_auto_bias - 200
        ), "Auto-bias should click significantly left of center"
