"""Shared vision runtime configuration."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class VisionSettings:
    base_url: str
    api_key: str
    model: str


def load_vision_settings() -> VisionSettings | None:
    base_url = os.getenv("VISION_API_BASE_URL", "").strip()
    api_key = os.getenv("VISION_API_KEY", "").strip()
    model = os.getenv("VISION_MODEL", "").strip()
    if not (base_url and api_key and model):
        return None

    return VisionSettings(base_url=base_url, api_key=api_key, model=model)


def vision_is_enabled() -> bool:
    return load_vision_settings() is not None
