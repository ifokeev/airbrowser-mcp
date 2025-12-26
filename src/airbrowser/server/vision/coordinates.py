"""Vision-based coordinate detection for UI elements."""

import json
import logging
import re
from typing import Any

from .openrouter import OpenRouterClient

logger = logging.getLogger(__name__)


class VisionCoordinateDetector:
    """Detects UI element coordinates using vision models."""

    def __init__(self, model: str):
        self.model = model

    def _create_prompt(self, element_description: str) -> str:
        """Create coordinate detection prompt."""
        return f"""Find the EXACT clickable element for: {element_description}

IMPORTANT: Return the precise bounding box of the clickable element itself, NOT its container.
- For links: return ONLY the link text bounds, not the surrounding row or card
- For buttons: return ONLY the button bounds
- For inputs: return ONLY the input field bounds

Return JSON only:
{{"found": true, "element": "description", "x": 123, "y": 456, "width": 78, "height": 90, "confidence": 0.95}}

Where x,y = top-left corner of the clickable element, coordinates in pixels, confidence 0.0-1.0.

If not found: {{"found": false, "error": "reason"}}"""

    def _parse_response(self, response: str) -> dict[str, Any]:
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
            logger.error(f"Failed to parse response: {e}")

        return {"success": False, "error": f"Could not parse: {response[:200]}..."}

    def _normalize_gemini_coords(self, coords: dict[str, Any], img_w: int, img_h: int) -> dict[str, Any]:
        """Convert Gemini's 0-1000 normalized coordinates to pixels."""
        if not coords.get("success"):
            return coords
        try:
            coords["x"] = int(coords["x"] / 1000.0 * img_w)
            coords["y"] = int(coords["y"] / 1000.0 * img_h)
            coords["width"] = int(coords["width"] / 1000.0 * img_w)
            coords["height"] = int(coords["height"] / 1000.0 * img_h)
        except Exception as e:
            logger.warning(f"Failed to normalize Gemini coordinates: {e}")
        return coords

    def _clamp_to_image_bounds(self, coords: dict[str, Any], img_w: int, img_h: int) -> dict[str, Any]:
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

    def _get_image_size(self, image_path: str) -> tuple[int, int]:
        """Get image dimensions, defaults to 1920x1080."""
        try:
            from PIL import Image

            with Image.open(image_path) as img:
                return img.size
        except Exception:
            return (1920, 1080)

    def detect(self, image_path: str, prompt: str) -> dict[str, Any]:
        """Detect UI element coordinates."""
        import os

        if not os.path.exists(image_path):
            return {"success": False, "error": f"Image not found: {image_path}"}

        img_w, img_h = self._get_image_size(image_path)

        try:
            client = OpenRouterClient(model=self.model)
            if not client.is_available():
                return {"success": False, "error": f"OpenRouter not available for {self.model}"}

            result = client.explain_screenshot(image_path, self._create_prompt(prompt))
            if not result.get("success"):
                return {"success": False, "error": result.get("error", "Vision model failed")}

            coords = self._parse_response(result.get("explanation", ""))
            if not coords.get("success"):
                return coords

            if "gemini" in self.model.lower():
                coords = self._normalize_gemini_coords(coords, img_w, img_h)

            # Clamp coordinates to image bounds to prevent clicking outside viewport
            coords = self._clamp_to_image_bounds(coords, img_w, img_h)

            coords["model"] = self.model
            coords["image_path"] = image_path
            coords["prompt"] = prompt
            coords["image_size"] = {"width": img_w, "height": img_h}
            return coords

        except Exception as e:
            logger.error(f"Coordinate detection failed: {e}")
            return {"success": False, "error": str(e)}


def detect_element_coordinates(image_path: str, prompt: str, model: str) -> dict[str, Any]:
    """Detect element coordinates using specified model."""
    return VisionCoordinateDetector(model).detect(image_path, prompt)
