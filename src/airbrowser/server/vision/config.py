"""Shared vision runtime configuration."""

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VisionSettings:
    base_url: str
    api_key: str
    model: str
    stream_default: bool


def _parse_env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False

    logger.warning("Invalid %s=%r; falling back to %s", name, raw, default)
    return default


def resolve_vision_stream(request_stream: bool | None, settings: VisionSettings) -> bool:
    if request_stream is not None:
        return request_stream
    return settings.stream_default


def load_vision_settings() -> VisionSettings | None:
    base_url = os.getenv("VISION_API_BASE_URL", "").strip()
    api_key = os.getenv("VISION_API_KEY", "").strip()
    model = os.getenv("VISION_MODEL", "").strip()
    if not (base_url and api_key and model):
        return None

    return VisionSettings(
        base_url=base_url,
        api_key=api_key,
        model=model,
        stream_default=_parse_env_bool("VISION_STREAM_DEFAULT"),
    )


def vision_is_enabled() -> bool:
    return load_vision_settings() is not None
