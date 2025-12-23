"""OpenRouter API client for vision model integration."""

import base64
import logging
import os
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Client for interacting with OpenRouter's vision models."""

    def __init__(self, api_key: str | None = None, model: str = "google/gemini-3-flash-preview"):
        """
        Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            model: Model to use for vision tasks (default: google/gemini-3-flash-preview)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.client = None

        if not self.api_key:
            logger.warning("OpenRouter API key not provided. Screenshot explanation will be disabled.")
            return

        if OpenAI is None:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            return

        try:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                default_headers={"HTTP-Referer": "http://localhost:8000", "X-Title": "Airbrowser"},
            )
            logger.info(f"OpenRouter client initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {e}")
            self.client = None

    def is_available(self) -> bool:
        """Check if OpenRouter client is available for use."""
        return self.client is not None and self.api_key is not None

    def encode_image_to_base64(self, image_path: str) -> str | None:
        """
        Encode an image file to base64.

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded image string or None if failed
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to encode image {image_path}: {e}")
            return None

    def get_mime_type(self, image_path: str) -> str:
        """
        Determine MIME type based on file extension.

        Args:
            image_path: Path to the image file

        Returns:
            MIME type string
        """
        ext = Path(image_path).suffix.lower()
        if ext == ".png":
            return "image/png"
        elif ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".gif":
            return "image/gif"
        elif ext == ".webp":
            return "image/webp"
        else:
            return "image/png"  # Default fallback

    def explain_screenshot(
        self, image_path: str, prompt: str = "What's in this screenshot? Describe what you see in detail."
    ) -> dict[str, Any]:
        """
        Explain a screenshot using OpenRouter's vision model.

        Args:
            image_path: Path to the screenshot file
            prompt: Custom prompt for the explanation

        Returns:
            Dictionary with success status and explanation or error message
        """
        if not self.is_available():
            return {"success": False, "error": "OpenRouter client not available (check API key and dependencies)"}

        if not os.path.exists(image_path):
            return {"success": False, "error": f"Screenshot file not found: {image_path}"}

        try:
            # Encode image to base64
            base64_image = self.encode_image_to_base64(image_path)
            if not base64_image:
                return {"success": False, "error": "Failed to encode image to base64"}

            # Get MIME type
            mime_type = self.get_mime_type(image_path)

            # Create the vision request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}},
                        ],
                    }
                ],
                max_tokens=1000,
                temperature=0.1,
                timeout=120.0,  # 2 minute timeout
            )

            explanation = response.choices[0].message.content

            return {
                "success": True,
                "explanation": explanation,
                "model": self.model,
                "prompt": prompt,
                "image_path": image_path,
            }

        except Exception as e:
            logger.error(f"OpenRouter API request failed: {e}")
            return {"success": False, "error": f"API request failed: {str(e)}"}

    def explain_multiple_screenshots(
        self, image_paths: list, prompt: str = "Compare and describe these screenshots. What's different between them?"
    ) -> dict[str, Any]:
        """
        Explain multiple screenshots together using OpenRouter's vision model.

        Args:
            image_paths: List of paths to screenshot files
            prompt: Custom prompt for the comparison

        Returns:
            Dictionary with success status and explanation or error message
        """
        if not self.is_available():
            return {"success": False, "error": "OpenRouter client not available (check API key and dependencies)"}

        if not image_paths or len(image_paths) == 0:
            return {"success": False, "error": "No image paths provided"}

        try:
            # Build content array with text prompt first
            content = [{"type": "text", "text": prompt}]

            # Add all images
            for image_path in image_paths:
                if not os.path.exists(image_path):
                    logger.warning(f"Skipping missing screenshot: {image_path}")
                    continue

                base64_image = self.encode_image_to_base64(image_path)
                if base64_image:
                    mime_type = self.get_mime_type(image_path)
                    content.append(
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                    )

            if len(content) == 1:  # Only text, no images
                return {"success": False, "error": "No valid images found in provided paths"}

            # Create the vision request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}],
                max_tokens=1500,
                temperature=0.1,
            )

            explanation = response.choices[0].message.content

            return {
                "success": True,
                "explanation": explanation,
                "model": self.model,
                "prompt": prompt,
                "image_count": len(content) - 1,  # Subtract 1 for text prompt
                "image_paths": image_paths,
            }

        except Exception as e:
            logger.error(f"OpenRouter API request for multiple images failed: {e}")
            return {"success": False, "error": f"API request failed: {str(e)}"}


# Global instance for reuse
_openrouter_client = None


def get_openrouter_client() -> OpenRouterClient:
    """Get the global OpenRouter client instance."""
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenRouterClient()
    return _openrouter_client
