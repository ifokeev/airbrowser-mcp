"""Shared vision runtime configuration.

Vision settings live on the central `Settings` singleton in
``airbrowser.server.settings``. This module exposes a legacy
``VisionSettings`` dataclass and helpers for backwards compatibility.
"""

import logging
from dataclasses import dataclass

from airbrowser.server.settings import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VisionSettings:
    base_url: str
    api_key: str
    model: str
    stream_default: bool


def resolve_vision_stream(request_stream: bool | None, vision: VisionSettings) -> bool:
    if request_stream is not None:
        return request_stream
    return vision.stream_default


def load_vision_settings() -> VisionSettings | None:
    """Return a VisionSettings snapshot if vision is enabled, else None."""
    if not settings.vision_enabled:
        return None
    return VisionSettings(
        base_url=settings.vision_api_base_url,
        api_key=settings.vision_api_key,
        model=settings.vision_model,
        stream_default=settings.vision_stream_default,
    )


def vision_is_enabled() -> bool:
    return settings.vision_enabled
