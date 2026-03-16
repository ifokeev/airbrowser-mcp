"""Minimal OpenAI-compatible vision client."""

import base64
import mimetypes
from pathlib import Path
from typing import Any

from openai import OpenAI


def _image_to_data_url(image_path: Path) -> str:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


class OpenAICompatibleVisionClient:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.model = model
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def explain_screenshot(self, image_path: str, prompt: str) -> dict[str, Any]:
        image = Path(image_path)
        if not image.exists():
            return {"success": False, "error": f"Screenshot file not found: {image_path}"}

        try:
            image_url = _image_to_data_url(image)
        except OSError as exc:
            return {"success": False, "error": f"Failed to read screenshot: {exc}"}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                max_tokens=1000,
                temperature=0.1,
                timeout=120.0,
            )
        except Exception as exc:
            return {"success": False, "error": f"API request failed: {exc}"}

        try:
            explanation = response.choices[0].message.content
            if explanation is None:
                raise ValueError("missing message content")
        except (AttributeError, IndexError, TypeError, ValueError) as exc:
            return {"success": False, "error": f"Malformed API response: {exc}"}

        return {"success": True, "explanation": explanation, "model": self.model}
