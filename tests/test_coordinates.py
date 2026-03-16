from unittest.mock import MagicMock

import pytest

import airbrowser.server.vision.coordinates as vision_coordinates
from airbrowser.server.browser.commands.vision import _transform_to_screen_coords
from airbrowser.server.vision.coordinates import VisionCoordinateDetector, detect_element_coordinates


def _make_mock_driver(*, win_x=0, win_y=0, win_w=1920, win_h=1080, viewport_w=1920, viewport_h=1080):
    driver = MagicMock()
    driver.get_window_rect.return_value = {"x": win_x, "y": win_y, "width": win_w, "height": win_h}
    driver.execute_script.side_effect = lambda script: {
        "return window.innerWidth;": viewport_w,
        "return window.innerHeight;": viewport_h,
    }.get(script)
    return driver


def test_parse_response_extracts_json_payload():
    detector = VisionCoordinateDetector("rightcode/gpt-5.4")

    result = detector._parse_response(
        '{"found": true, "element": "button", "x": 100, "y": 200, "width": 50, "height": 30, "confidence": 0.95}'
    )

    assert result["success"] is True
    assert result["x"] == 100
    assert result["y"] == 200
    assert result["width"] == 50
    assert result["height"] == 30
    assert result["confidence"] == 0.95


def test_parse_response_falls_back_to_numbers():
    detector = VisionCoordinateDetector("rightcode/gpt-5.4")

    result = detector._parse_response("The element is at position 100 200 with size 50 30")

    assert result["success"] is True
    assert result["x"] == 100
    assert result["y"] == 200
    assert result["width"] == 50
    assert result["height"] == 30
    assert result["confidence"] == 0.7


def test_clamp_coordinates_within_bounds():
    detector = VisionCoordinateDetector("rightcode/gpt-5.4")
    coords = {"success": True, "x": 100, "y": 100, "width": 200, "height": 50}

    result = detector._clamp_to_image_bounds(coords, 1920, 1080)

    assert result["x"] == 100
    assert result["y"] == 100
    assert result["width"] == 200
    assert result["height"] == 50
    assert "partially_visible" not in result


def test_clamp_google_search_button_case():
    detector = VisionCoordinateDetector("rightcode/gpt-5.4")
    coords = {"success": True, "x": 1222, "y": 832, "width": 87, "height": 40}

    result = detector._clamp_to_image_bounds(coords, 1912, 837)

    assert result["y"] == 832
    assert result["height"] == 5
    assert result["partially_visible"] is True


def test_transform_with_chrome_offset():
    driver = _make_mock_driver(win_w=1920, win_h=1080, viewport_w=1920, viewport_h=900)
    coords = {"x": 500, "y": 300, "width": 100, "height": 50, "image_size": {"width": 1920, "height": 900}}

    result = _transform_to_screen_coords(driver, coords)

    assert result["x"] == 500
    assert result["y"] == 480
    assert result["click_point"] == {"x": 550, "y": 505}


def test_transform_uses_fractional_offsets_in_fallback():
    driver = MagicMock()
    driver.get_window_rect.side_effect = Exception("Driver error")
    coords = {"x": 400, "y": 300, "width": 1000, "height": 50, "image_size": {"width": 1920, "height": 1080}}

    result = _transform_to_screen_coords(driver, coords, fx=0.2, fy=0.5)

    assert result["click_point"] == {"x": 600, "y": 325}


def test_transform_requires_image_size():
    driver = _make_mock_driver()

    with pytest.raises(ValueError, match="image_size is required"):
        _transform_to_screen_coords(driver, {"x": 500, "y": 300, "width": 100, "height": 50})


def test_detect_element_coordinates_uses_generic_client(monkeypatch, tmp_path):
    image_path = tmp_path / "shot.png"
    image_path.write_bytes(b"fake-image")

    monkeypatch.setenv("VISION_API_BASE_URL", "https://cliproxy.ldc-fe.org/v1")
    monkeypatch.setenv("VISION_API_KEY", "test-key")
    monkeypatch.setenv("VISION_MODEL", "default/model")

    captured = {}

    class FakeClient:
        def __init__(self, base_url, api_key, model):
            captured["base_url"] = base_url
            captured["api_key"] = api_key
            captured["model"] = model

        def explain_screenshot(self, image_path, prompt):
            return {
                "success": True,
                "explanation": '{"found": true, "x": 10, "y": 20, "width": 30, "height": 40, "confidence": 0.9}',
            }

    monkeypatch.setattr(vision_coordinates, "OpenAICompatibleVisionClient", FakeClient, raising=False)
    monkeypatch.setattr(VisionCoordinateDetector, "_get_image_size", lambda self, path: (100, 50))

    result = detect_element_coordinates(str(image_path), "the submit button", "rightcode/gpt-5.4")

    assert result["success"] is True
    assert result["model"] == "rightcode/gpt-5.4"
    assert result["image_size"] == {"width": 100, "height": 50}
    assert captured == {
        "base_url": "https://cliproxy.ldc-fe.org/v1",
        "api_key": "test-key",
        "model": "rightcode/gpt-5.4",
    }
