"""Cross-platform path resolution for airbrowser.

All base directories come from `settings`; this module provides IPC
subdirectory helpers and platform-specific environment setup.
"""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from airbrowser.server.settings import settings

# --- Base directories (delegated to settings) ---


def data_dir() -> Path:
    return settings.data_dir


def ipc_dir() -> Path:
    return settings.ipc_dir


def src_dir() -> Path:
    """Return the src/ directory containing the airbrowser package."""
    return Path(__file__).resolve().parent.parent.parent


# --- IPC subdirectories ---


def queue_dir() -> Path:
    return ipc_dir() / "browser-queue"


def status_dir() -> Path:
    return ipc_dir() / "browser-status"


def response_dir() -> Path:
    return ipc_dir() / "browser-responses"


def commands_dir(browser_id: str) -> Path:
    return ipc_dir() / "browser-commands" / browser_id


def responses_dir(browser_id: str) -> Path:
    return ipc_dir() / "browser-responses" / browser_id


def status_file(browser_id: str) -> Path:
    return status_dir() / f"{browser_id}.json"


def log_dir() -> Path:
    return ipc_dir() / "browser-launcher-logs"


# --- Data subdirectories (delegate to settings properties) ---


def profiles_dir() -> Path:
    return settings.effective_profiles_dir


def screenshots_dir() -> Path:
    return settings.effective_screenshots_dir


def downloads_dir() -> Path:
    return settings.effective_downloads_dir


def state_dir_path() -> Path:
    return settings.effective_state_dir


def certs_dir() -> Path:
    return data_dir() / "certs"


# --- Platform helpers ---


def python_executable() -> str:
    """Return the current Python interpreter path."""
    return sys.executable


def launcher_script() -> str:
    """Return the path to the browser launcher module."""
    return str(src_dir() / "airbrowser" / "server" / "browser" / "launcher.py")


def setup_display_env() -> None:
    """Set DISPLAY env var if needed (Linux only, no-op on Mac/Windows)."""
    if platform.system() == "Linux" and not os.environ.get("DISPLAY"):
        os.environ["DISPLAY"] = settings.display


def setup_home_env() -> None:
    """Set HOME if inside Docker, otherwise leave the real HOME alone."""
    if settings.in_docker:
        os.environ["HOME"] = "/home/browseruser"


def get_pythonpath() -> str:
    """Return PYTHONPATH value that includes our src directory."""
    return str(src_dir())


def in_docker() -> bool:
    return settings.in_docker
