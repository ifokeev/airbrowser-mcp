"""Data models for Airbrowser API."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from airbrowser.server.settings import settings


def _get_default_window_size() -> tuple[int, int]:
    """Return the default window size from settings (SCREEN_WIDTH/HEIGHT or SCREEN_RESOLUTION)."""
    if settings.screen_width and settings.screen_height:
        return (settings.screen_width, max(settings.screen_height - 100, 600))

    parts = settings.screen_resolution.split("x")
    if len(parts) >= 2:
        try:
            width = int(parts[0])
            height = int(parts[1])
            return (width, max(height - 100, 600))
        except ValueError:
            pass
    return (1600, 800)


class BrowserStatus(str, Enum):
    CREATING = "creating"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    CLOSING = "closing"


class _Model(BaseModel):
    """Base model with a `to_dict` alias matching the legacy dataclass API."""

    model_config = ConfigDict(use_enum_values=False, arbitrary_types_allowed=True)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class BrowserConfig(_Model):
    """Configuration for creating a browser instance.

    Browsers are always headful (virtual display via noVNC). UC (undetected
    chrome) mode is enabled by default but can be disabled for faster startup.
    """

    uc: bool = True
    profile_name: str | None = None
    proxy: str | None = None
    user_agent: str | None = None
    window_size: tuple[int, int] = Field(default_factory=_get_default_window_size)
    disable_gpu: bool = False
    disable_images: bool = False
    disable_javascript: bool = False
    extensions: list[str] = Field(default_factory=list)
    custom_args: list[str] = Field(default_factory=list)


class BrowserInfo(_Model):
    """Information about a browser instance."""

    id: str
    status: BrowserStatus
    config: BrowserConfig
    created_at: datetime
    last_activity: datetime
    display_num: int | None = None
    profile_dir: str | None = None
    current_url: str | None = None
    error_message: str | None = None
    session_id: str | None = None


class BrowserAction(_Model):
    """Represents an action to perform on a browser."""

    action: str
    selector: str | None = None
    text: str | None = None
    url: str | None = None
    timeout: int | None = None
    by: str = "css"
    options: dict[str, Any] = Field(default_factory=dict)


class ActionResult(_Model):
    """Result of a browser action."""

    success: bool
    message: str
    data: Any | None = None
    execution_time: float = 0.0


class PoolStatus(_Model):
    """Overall status of the browser pool."""

    total_browsers: int
    active_browsers: int
    available_browsers: int
    creating_browsers: int
    error_browsers: int
    max_browsers: int
    uptime_seconds: float
    memory_usage_mb: float
    cpu_usage_percent: float
    healthy: bool = True


get_window_size_from_env = _get_default_window_size
