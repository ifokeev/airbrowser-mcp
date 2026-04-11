"""Centralized application settings via Pydantic BaseSettings.

All runtime configuration is declared here with typed defaults. Environment
variables are read once at import time and exposed via the `settings` singleton.

Usage:
    from airbrowser.server.settings import settings

    if settings.enable_mcp:
        ...
    max = settings.max_browsers
"""

from __future__ import annotations

import logging
import os
import platform
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


def _in_docker() -> bool:
    """Detect if running inside a Docker container."""
    return os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")


def _default_data_dir() -> Path:
    """Default data directory when AIRBROWSER_DATA_DIR is unset."""
    if _in_docker():
        return Path("/app")

    # Dev checkout: use <repo>/.data
    src_dir = Path(__file__).resolve().parent  # server/
    project_root = src_dir.parent.parent.parent  # repo root
    if (project_root / "pyproject.toml").exists():
        return project_root / ".data"

    # Installed: user home
    return Path.home() / ".airbrowser"


def _default_ipc_dir() -> Path:
    """Default IPC directory when AIRBROWSER_IPC_DIR is unset."""
    import tempfile

    if _in_docker():
        return Path("/tmp")
    return Path(tempfile.gettempdir()) / "airbrowser"


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and .env files."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Browser pool ---
    max_browsers: int = Field(default=10, description="Max concurrent browsers")
    browser_timeout: int = Field(default=300, description="Browser idle timeout seconds")
    cleanup_interval: int = Field(default=60, description="Cleanup poll interval seconds")
    enable_session_restore: bool = Field(default=True)

    # --- Command timeouts ---
    command_timeout_default: int = Field(default=20)
    navigate_timeout_default: int = Field(default=60)
    vision_timeout_default: int = Field(default=60)
    ipc_timeout_slack: int = Field(default=5)

    # --- Paths ---
    airbrowser_data_dir: Path | None = Field(default=None)
    airbrowser_ipc_dir: Path | None = Field(default=None)
    profiles_dir: Path | None = Field(default=None)
    screenshots_dir: Path | None = Field(default=None)
    downloads_dir: Path | None = Field(default=None)
    state_dir: Path | None = Field(default=None)

    # --- Screenshot lifecycle ---
    screenshots_ttl_seconds: int = Field(default=3600)
    screenshots_max_bytes: int = Field(default=256 * 1024 * 1024)
    screenshots_min_free_bytes: int = Field(default=64 * 1024 * 1024)

    # --- Display (Linux only) ---
    display: str = Field(default=":49")
    screen_width: int | None = Field(default=None)
    screen_height: int | None = Field(default=None)
    screen_resolution: str = Field(default="1600x900x24")

    # --- HTTP server ---
    port: int = Field(default=8000)
    host: str = Field(default="0.0.0.0")
    base_path: str = Field(default="")
    api_base_url: str = Field(default="http://localhost:8000")
    debug: bool = Field(default=False)
    werkzeug_run_main: bool = Field(default=False)

    # --- MCP ---
    enable_mcp: bool = Field(default=True)
    mcp_port: int = Field(default=3099)
    mcp_include_all_tools: bool = Field(default=False)

    # --- VNC ---
    vnc_base_url: str = Field(default="")

    # --- Vision (optional) ---
    vision_api_base_url: str = Field(default="")
    vision_api_key: str = Field(default="")
    vision_model: str = Field(default="")
    vision_stream_default: bool = Field(default=False)

    @field_validator("airbrowser_data_dir", mode="before")
    @classmethod
    def _default_data(cls, v: Path | str | None) -> Path:
        if v:
            return Path(v)
        return _default_data_dir()

    @field_validator("airbrowser_ipc_dir", mode="before")
    @classmethod
    def _default_ipc(cls, v: Path | str | None) -> Path:
        if v:
            return Path(v)
        return _default_ipc_dir()

    @property
    def effective_profiles_dir(self) -> Path:
        return self.profiles_dir or (self.data_dir / "browser-profiles")

    @property
    def effective_screenshots_dir(self) -> Path:
        return self.screenshots_dir or (self.data_dir / "screenshots")

    @property
    def effective_downloads_dir(self) -> Path:
        return self.downloads_dir or (self.data_dir / "downloads")

    @property
    def effective_state_dir(self) -> Path:
        return self.state_dir or (self.data_dir / "state")

    @property
    def data_dir(self) -> Path:
        assert self.airbrowser_data_dir is not None  # validator ensures non-None
        return self.airbrowser_data_dir

    @property
    def ipc_dir(self) -> Path:
        assert self.airbrowser_ipc_dir is not None  # validator ensures non-None
        return self.airbrowser_ipc_dir

    @property
    def in_docker(self) -> bool:
        return _in_docker()

    @property
    def is_linux(self) -> bool:
        return platform.system() == "Linux"

    @property
    def vision_enabled(self) -> bool:
        """Vision is enabled only when all three required fields are set."""
        return bool(self.vision_api_base_url and self.vision_api_key and self.vision_model)

    def resolved_screen_resolution(self) -> str:
        """Return SCREEN_RESOLUTION, composing from SCREEN_WIDTH/HEIGHT if provided."""
        if self.screen_width and self.screen_height:
            return f"{self.screen_width}x{self.screen_height}x24"
        return self.screen_resolution


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the Settings singleton. Cached on first call."""
    return Settings()


# Convenience singleton — import as `from airbrowser.server.settings import settings`
settings: Settings = get_settings()
