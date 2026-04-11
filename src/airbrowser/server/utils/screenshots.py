"""Canonical screenshot lifecycle utilities."""

import errno
import platform
import shutil
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import SplitResult, urlsplit, urlunsplit
from uuid import uuid4

from werkzeug.security import safe_join

from airbrowser.server.paths import screenshots_dir as _screenshots_dir
from airbrowser.server.settings import settings

DEFAULT_SCREENSHOTS_DIR = _screenshots_dir()
SCREENSHOT_LOCK_FILENAME = ".airbrowser-screenshots.lock"
API_V1_PATH = "/api/v1"

_SCREENSHOT_STORE_MUTEX = threading.Lock()


def get_screenshot_dir() -> Path:
    """Return the configured screenshot directory."""
    return settings.effective_screenshots_dir


def _normalize_url_path(path: str) -> str:
    stripped = path.strip()
    if not stripped or stripped == "/":
        return ""
    return f"/{stripped.strip('/')}"


def _strip_api_v1_suffix(path: str) -> str:
    normalized_path = _normalize_url_path(path)
    if normalized_path == API_V1_PATH:
        return ""
    if normalized_path.endswith(API_V1_PATH):
        return normalized_path[: -len(API_V1_PATH)]
    return normalized_path


def _get_public_base_url() -> str:
    parsed = urlsplit(settings.api_base_url)
    normalized_public_path = _normalize_url_path(settings.base_path) or _strip_api_v1_suffix(parsed.path)
    public_base = SplitResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=normalized_public_path,
        query="",
        fragment="",
    )
    return urlunsplit(public_base)


def get_screenshot_url(filename: str) -> str:
    """Return the public URL for a screenshot filename."""
    base_url = _get_public_base_url().rstrip("/")
    return f"{base_url}/screenshots/{filename}"


def _get_screenshot_entries(directory: Path) -> list[tuple[Path, float, int]]:
    entries = []
    for path in directory.glob("*.png"):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
        except FileNotFoundError:
            continue
        entries.append((path, stat.st_mtime, stat.st_size))
    entries.sort(key=lambda entry: entry[1])
    return entries


def _flock(lock_file, exclusive: bool):
    """Cross-platform file locking."""
    if platform.system() == "Windows":
        import msvcrt

        if exclusive:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        else:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        if exclusive:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        else:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


@contextmanager
def _locked_screenshot_store(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    lock_path = directory / SCREENSHOT_LOCK_FILENAME

    with _SCREENSHOT_STORE_MUTEX, lock_path.open("a+b") as lock_file:
        _flock(lock_file, exclusive=True)
        try:
            yield
        finally:
            _flock(lock_file, exclusive=False)


def _prune_screenshot_store(
    directory: Path,
    now: float,
    *,
    required_bytes: int = 0,
) -> None:
    ttl_seconds = settings.screenshots_ttl_seconds
    max_bytes = settings.screenshots_max_bytes
    min_free_bytes = settings.screenshots_min_free_bytes

    entries = _get_screenshot_entries(directory)
    for path, modified_at, _size in entries:
        if ttl_seconds > 0 and now - modified_at > ttl_seconds:
            path.unlink(missing_ok=True)

    entries = _get_screenshot_entries(directory)
    total_bytes = sum(size for _path, _modified_at, size in entries)
    while entries and (
        total_bytes + required_bytes > max_bytes or shutil.disk_usage(directory).free < min_free_bytes + required_bytes
    ):
        path, _modified_at, size = entries.pop(0)
        path.unlink(missing_ok=True)
        total_bytes -= size


def prune_screenshots(now: float | None = None) -> None:
    """Prune expired and oldest screenshots until storage is healthy."""
    now = time.time() if now is None else now
    directory = get_screenshot_dir()
    with _locked_screenshot_store(directory):
        _prune_screenshot_store(directory, now)


def _ensure_screenshot_capacity(directory: Path, *, incoming_bytes: int) -> None:
    # Caller must hold the store lock so cleanup and write stay atomic.
    max_bytes = settings.screenshots_max_bytes
    min_free_bytes = settings.screenshots_min_free_bytes

    if incoming_bytes > max_bytes:
        raise OSError(errno.ENOSPC, "No space left on device")

    _prune_screenshot_store(
        directory,
        time.time(),
        required_bytes=incoming_bytes,
    )

    if shutil.disk_usage(directory).free < min_free_bytes + incoming_bytes:
        raise OSError(errno.ENOSPC, "No space left on device")


def _capture_screenshot_bytes(driver) -> bytes:
    import tempfile

    # Try CDP screenshot first (avoids WebDriver reconnection in CDP Mode)
    try:
        if hasattr(driver, "cdp") and driver.cdp:
            # save_screenshot is async, returns file path — use a temp file
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp_path = tmp.name
            tmp.close()
            try:
                driver.cdp.loop.run_until_complete(driver.cdp.page.save_screenshot(tmp_path))
                png_bytes = Path(tmp_path).read_bytes()
                if len(png_bytes) > 0:
                    return png_bytes
            finally:
                Path(tmp_path).unlink(missing_ok=True)
    except Exception:
        pass
    # Fallback: reconnect WebDriver temporarily for screenshot, then disconnect
    try:
        if hasattr(driver, "connect"):
            driver.connect()
        png_bytes = driver.get_screenshot_as_png()
        if hasattr(driver, "disconnect"):
            driver.disconnect()
        if isinstance(png_bytes, bytes | bytearray) and len(png_bytes) > 0:
            return bytes(png_bytes)
    except Exception:
        pass
    # Last resort: direct WebDriver call
    png_bytes = driver.get_screenshot_as_png()
    if not isinstance(png_bytes, bytes | bytearray) or len(png_bytes) == 0:
        raise OSError(errno.EIO, "Failed to save screenshot")
    return bytes(png_bytes)


def take_screenshot(driver, browser_id: str) -> dict:
    """Write a screenshot and return its canonical metadata."""
    directory = get_screenshot_dir()
    png_bytes = _capture_screenshot_bytes(driver)
    with _locked_screenshot_store(directory):
        _ensure_screenshot_capacity(directory, incoming_bytes=len(png_bytes))

        filename = f"{browser_id}_{int(time.time() * 1000)}_{uuid4().hex[:8]}.png"
        path = directory / filename

        try:
            written = path.write_bytes(png_bytes)
        except Exception:
            path.unlink(missing_ok=True)
            raise

        if written != len(png_bytes) or not path.is_file() or path.stat().st_size != len(png_bytes):
            path.unlink(missing_ok=True)
            raise OSError(errno.EIO, "Failed to save screenshot")

    return {
        "path": str(path),
        "filename": filename,
        "url": get_screenshot_url(filename),
    }


def touch_screenshot(filename: str) -> None:
    """Mark a screenshot as recently used when it is read."""
    joined = safe_join(str(get_screenshot_dir()), filename)
    if not joined:
        return

    path = Path(joined)
    if path.is_file():
        path.touch()
