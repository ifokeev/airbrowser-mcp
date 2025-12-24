"""Data models for Airbrowser API."""

import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


def _get_default_window_size():
    """Get default window size, preferring SCREEN_WIDTH/HEIGHT if set."""
    # Prefer explicit width/height if provided
    try:
        w_env = os.environ.get("SCREEN_WIDTH")
        h_env = os.environ.get("SCREEN_HEIGHT")
        if w_env and h_env:
            width = int(w_env)
            height = int(h_env)
            adjusted_height = max(height - 100, 600)
            return (width, adjusted_height)
    except (ValueError, TypeError):
        pass

    # Fallback to SCREEN_RESOLUTION (WIDTHxHEIGHTxDEPTH)
    resolution = os.environ.get("SCREEN_RESOLUTION", "1920x1080x24")
    try:
        parts = resolution.split("x")
        if len(parts) >= 2:
            width = int(parts[0])
            height = int(parts[1])
            adjusted_height = max(height - 100, 600)
            return (width, adjusted_height)
    except (ValueError, IndexError):
        pass
    return (1920, 980)


class BrowserStatus(Enum):
    CREATING = "creating"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    CLOSING = "closing"


@dataclass
class BrowserConfig:
    """Configuration for creating a browser instance.

    Note: Browsers are always headful (virtual display via noVNC).
    UC (undetected chrome) mode is enabled by default but can be disabled for faster startup.
    """

    uc: bool = True  # Undetected Chrome mode (slower but bypasses bot detection)
    profile_name: str | None = None  # None = fresh session, named = persistent
    proxy: str | None = None
    user_agent: str | None = None
    window_size: tuple = field(default_factory=_get_default_window_size)
    disable_gpu: bool = False
    disable_images: bool = False
    disable_javascript: bool = False
    extensions: list[str] = field(default_factory=list)
    custom_args: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "uc": self.uc,
            "profile_name": self.profile_name,
            "proxy": self.proxy,
            "user_agent": self.user_agent,
            "window_size": self.window_size,
            "disable_gpu": self.disable_gpu,
            "disable_images": self.disable_images,
            "disable_javascript": self.disable_javascript,
            "extensions": self.extensions,
            "custom_args": self.custom_args,
        }


@dataclass
class BrowserInfo:
    """Information about a browser instance"""

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status.value,
            "config": self.config.to_dict(),
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "display_num": self.display_num,
            "profile_dir": self.profile_dir,
            "current_url": self.current_url,
            "error_message": self.error_message,
            "session_id": self.session_id,
        }


@dataclass
class BrowserAction:
    """Represents an action to perform on a browser"""

    action: str
    selector: str | None = None
    text: str | None = None
    url: str | None = None
    timeout: int = 10
    by: str = "css"
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    """Result of a browser action"""

    success: bool
    message: str
    data: Any | None = None
    screenshot_path: str | None = None
    execution_time: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "screenshot_path": self.screenshot_path,
            "execution_time": self.execution_time,
        }


@dataclass
class PoolStatus:
    """Overall status of the browser pool"""

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

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_browsers": self.total_browsers,
            "active_browsers": self.active_browsers,
            "available_browsers": self.available_browsers,
            "creating_browsers": self.creating_browsers,
            "error_browsers": self.error_browsers,
            "max_browsers": self.max_browsers,
            "uptime_seconds": self.uptime_seconds,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_usage_percent": self.cpu_usage_percent,
            "healthy": self.healthy,
        }


# Alias for backwards compatibility
get_window_size_from_env = _get_default_window_size
