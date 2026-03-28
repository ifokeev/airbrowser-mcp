"""Cross-platform path resolution for airbrowser.

Centralizes all directory paths so the codebase works on Linux, macOS, and Windows
without hardcoded /tmp or /app paths.
"""

import os
import platform
import sys
import tempfile
from pathlib import Path

# Detect if running inside Docker
_IN_DOCKER = os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")


def _get_data_dir() -> Path:
    """Application data directory (profiles, screenshots, state, downloads)."""
    env = os.environ.get("AIRBROWSER_DATA_DIR")
    if env:
        return Path(env)

    if _IN_DOCKER:
        return Path("/app")

    # Native: use project root or ~/.airbrowser
    # Check if we're in a dev checkout (pyproject.toml exists)
    src_dir = Path(__file__).resolve().parent  # server/
    project_root = src_dir.parent.parent.parent  # go up to repo root
    if (project_root / "pyproject.toml").exists():
        return project_root / ".data"

    # Installed: use ~/.airbrowser
    return Path.home() / ".airbrowser"


def _get_ipc_dir() -> Path:
    """IPC base directory for file-based inter-process communication."""
    env = os.environ.get("AIRBROWSER_IPC_DIR")
    if env:
        return Path(env)

    if _IN_DOCKER:
        return Path("/tmp")

    # Native: use a subdirectory of the system temp dir
    return Path(tempfile.gettempdir()) / "airbrowser"


def _get_src_dir() -> Path:
    """Return the src/ directory containing the airbrowser package."""
    return Path(__file__).resolve().parent.parent.parent


# --- Public path accessors ---


def data_dir() -> Path:
    return _get_data_dir()


def ipc_dir() -> Path:
    return _get_ipc_dir()


def src_dir() -> Path:
    return _get_src_dir()


# IPC subdirectories
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


# Data subdirectories (with env var overrides for Docker compat)
def profiles_dir() -> Path:
    return Path(os.environ.get("PROFILES_DIR", str(data_dir() / "browser-profiles")))


def screenshots_dir() -> Path:
    return Path(os.environ.get("SCREENSHOTS_DIR", str(data_dir() / "screenshots")))


def downloads_dir() -> Path:
    return Path(os.environ.get("DOWNLOADS_DIR", str(data_dir() / "downloads")))


def state_dir_path() -> Path:
    return Path(os.environ.get("STATE_DIR", str(data_dir() / "state")))


def certs_dir() -> Path:
    return data_dir() / "certs"


# Platform helpers
def python_executable() -> str:
    """Return the current Python interpreter path."""
    return sys.executable


def launcher_script() -> str:
    """Return the path to the browser launcher module."""
    return str(src_dir() / "airbrowser" / "server" / "browser" / "launcher.py")


def setup_display_env():
    """Set DISPLAY env var if needed (Linux only, no-op on Mac/Windows)."""
    if platform.system() == "Linux" and not os.environ.get("DISPLAY"):
        os.environ["DISPLAY"] = ":49"


def setup_home_env():
    """Set HOME if inside Docker, otherwise leave the real HOME alone."""
    if _IN_DOCKER:
        os.environ["HOME"] = "/home/browseruser"


def get_pythonpath() -> str:
    """Return PYTHONPATH value that includes our src directory."""
    return str(src_dir())


def in_docker() -> bool:
    return _IN_DOCKER
