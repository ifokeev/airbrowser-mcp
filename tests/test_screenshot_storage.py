import errno
import os
import shutil
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import airbrowser.server.ipc.service as ipc_service_module
import airbrowser.server.utils.screenshots as screenshots


class FakeDriver:
    def __init__(self, png_bytes: bytes = b"png"):
        self.png_bytes = png_bytes
        self.png_calls = 0
        self.save_calls = []

    def get_screenshot_as_png(self) -> bytes:
        self.png_calls += 1
        return self.png_bytes

    def save_screenshot(self, path: str) -> bool:
        self.save_calls.append(path)
        raise AssertionError("save_screenshot should not be used")


class RecordingDriver:
    def __init__(self):
        self.png_bytes = b"png"
        self.png_calls = 0
        self.save_calls = []

    def get_screenshot_as_png(self) -> bytes:
        self.png_calls += 1
        return self.png_bytes

    def save_screenshot(self, path: str) -> bool:
        self.save_calls.append(path)
        raise AssertionError("save_screenshot should not be used")


def test_take_screenshot_uses_configured_directory(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("API_BASE_URL", "http://localhost:18080")
    driver = FakeDriver()

    result = screenshots.take_screenshot(driver, "browser-1")

    assert result["filename"] == Path(result["path"]).name
    assert result["path"] == str(tmp_path / result["filename"])
    assert result["url"] == f"http://localhost:18080/screenshots/{result['filename']}"
    assert Path(result["path"]).exists()
    assert driver.png_calls == 1
    assert driver.save_calls == []


def test_get_screenshot_dir_defaults_to_app_screenshots(monkeypatch):
    monkeypatch.delenv("SCREENSHOTS_DIR", raising=False)

    assert screenshots.get_screenshot_dir() == Path("/app/screenshots")


def test_get_screenshot_url_strips_api_v1_from_api_base_url(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "http://localhost:8000/api/v1")
    monkeypatch.delenv("BASE_PATH", raising=False)

    assert screenshots.get_screenshot_url("shot.png") == "http://localhost:8000/screenshots/shot.png"


@pytest.mark.parametrize(
    ("api_base_url", "base_path", "expected_url"),
    [
        (
            "https://api.example.com",
            "/airbrowser",
            "https://api.example.com/airbrowser/screenshots/shot.png",
        ),
        (
            "https://api.example.com/airbrowser/api/v1",
            "/airbrowser",
            "https://api.example.com/airbrowser/screenshots/shot.png",
        ),
    ],
)
def test_get_screenshot_url_uses_base_path_once(monkeypatch, api_base_url, base_path, expected_url):
    monkeypatch.setenv("API_BASE_URL", api_base_url)
    monkeypatch.setenv("BASE_PATH", base_path)

    assert screenshots.get_screenshot_url("shot.png") == expected_url


def test_prune_screenshots_removes_expired_then_oldest(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "60")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "100")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "0")

    old_file = tmp_path / "old.png"
    keep_a = tmp_path / "keep-a.png"
    keep_b = tmp_path / "keep-b.png"
    old_file.write_bytes(b"123456")
    keep_a.write_bytes(b"1234567")
    keep_b.write_bytes(b"1234567")

    now = time.time()
    os.utime(old_file, (now - 120, now - 120))
    os.utime(keep_a, (now - 10, now - 10))
    os.utime(keep_b, (now - 5, now - 5))

    screenshots.prune_screenshots(now=now)

    assert not old_file.exists()
    assert keep_a.exists()
    assert keep_b.exists()
    assert sum(path.stat().st_size for path in tmp_path.glob("*.png")) == 14

    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "12")

    screenshots.prune_screenshots(now=now)

    assert not keep_a.exists()
    assert keep_b.exists()
    assert sum(path.stat().st_size for path in tmp_path.glob("*.png")) <= 12


def test_prune_screenshots_trims_oldest_non_expired_files_to_budget(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "3600")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "12")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "0")

    oldest = tmp_path / "oldest.png"
    middle = tmp_path / "middle.png"
    newest = tmp_path / "newest.png"
    oldest.write_bytes(b"123456")
    middle.write_bytes(b"123456")
    newest.write_bytes(b"123456")
    now = time.time()
    os.utime(oldest, (now - 30, now - 30))
    os.utime(middle, (now - 20, now - 20))
    os.utime(newest, (now - 10, now - 10))

    screenshots.prune_screenshots(now=now)

    assert not oldest.exists()
    assert middle.exists()
    assert newest.exists()
    assert sum(path.stat().st_size for path in tmp_path.glob("*.png")) <= 12


def test_prune_screenshots_frees_space_by_deleting_oldest_even_under_byte_budget(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "3600")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "100")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "50")

    oldest = tmp_path / "oldest.png"
    newer = tmp_path / "newer.png"
    oldest.write_bytes(b"1234567890")
    newer.write_bytes(b"1234567890")
    now = time.time()
    os.utime(oldest, (now - 10, now - 10))
    os.utime(newer, (now - 5, now - 5))

    def fake_disk_usage(_):
        used = 60
        if not oldest.exists():
            used -= 10
        if not newer.exists():
            used -= 10
        return SimpleNamespace(total=100, used=used, free=100 - used)

    monkeypatch.setattr(shutil, "disk_usage", fake_disk_usage)

    screenshots.prune_screenshots(now=now)

    assert not oldest.exists()
    assert newer.exists()


def test_take_screenshot_raises_enospc_when_budget_cannot_be_recovered(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "0")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "1")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", str(10**15))
    driver = RecordingDriver()
    write_calls = []

    def unexpected_write(self, data):
        write_calls.append((self, data))
        raise AssertionError("canonical write should not happen before ENOSPC")

    monkeypatch.setattr(screenshots.Path, "write_bytes", unexpected_write)

    with pytest.raises(OSError) as exc:
        screenshots.take_screenshot(driver, "browser-1")

    assert exc.value.errno == 28
    assert driver.png_calls == 1
    assert driver.save_calls == []
    assert write_calls == []
    assert list(tmp_path.glob("*.png")) == []


def test_take_screenshot_keeps_store_within_budget_across_repeated_writes(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "3600")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "5")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "0")
    first_driver = FakeDriver(b"png")
    second_driver = FakeDriver(b"png")

    first = screenshots.take_screenshot(first_driver, "browser-1")
    older = time.time() - 10
    os.utime(first["path"], (older, older))
    second = screenshots.take_screenshot(second_driver, "browser-1")

    remaining = list(tmp_path.glob("*.png"))

    assert Path(first["path"]).exists() is False
    assert Path(second["path"]).exists() is True
    assert remaining == [Path(second["path"])]
    assert sum(path.stat().st_size for path in remaining) <= 5
    assert first_driver.save_calls == []
    assert second_driver.save_calls == []


def test_take_screenshot_serializes_concurrent_writers_to_stay_within_budget(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "3600")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "5")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "0")
    original_write_bytes = Path.write_bytes
    barrier = threading.Barrier(3)
    errors = []
    results = []

    def slow_write_bytes(self, data):
        time.sleep(0.1)
        return original_write_bytes(self, data)

    def worker(driver):
        barrier.wait()
        try:
            results.append(screenshots.take_screenshot(driver, "browser-1"))
        except Exception as exc:  # pragma: no cover - assertion captures unexpected path
            errors.append(exc)

    monkeypatch.setattr(screenshots.Path, "write_bytes", slow_write_bytes)
    threads = [
        threading.Thread(target=worker, args=(FakeDriver(b"1234"),)),
        threading.Thread(target=worker, args=(FakeDriver(b"5678"),)),
    ]

    for thread in threads:
        thread.start()

    barrier.wait()

    for thread in threads:
        thread.join()

    assert errors == []
    assert len(results) == 2
    remaining = list(tmp_path.glob("*.png"))
    assert len(remaining) == 1
    assert sum(path.stat().st_size for path in remaining) <= 5


def test_take_screenshot_raises_when_canonical_write_does_not_persist(monkeypatch, tmp_path):
    monkeypatch.setenv("SCREENSHOTS_DIR", str(tmp_path))
    monkeypatch.setenv("SCREENSHOTS_TTL_SECONDS", "3600")
    monkeypatch.setenv("SCREENSHOTS_MAX_BYTES", "100")
    monkeypatch.setenv("SCREENSHOTS_MIN_FREE_BYTES", "0")
    driver = FakeDriver()
    write_calls = []

    def fake_write_bytes(self, data):
        write_calls.append((self, data))
        return 0

    monkeypatch.setattr(screenshots.Path, "write_bytes", fake_write_bytes)

    with pytest.raises(OSError) as exc:
        screenshots.take_screenshot(driver, "browser-1")

    assert exc.value.errno == errno.EIO
    assert driver.png_calls == 1
    assert driver.save_calls == []
    assert len(write_calls) == 1
    assert list(tmp_path.glob("*.png")) == []


def test_browser_service_prunes_screenshots_on_startup(monkeypatch):
    calls = []
    monkeypatch.setenv("ENABLE_SESSION_RESTORE", "false")

    def fake_prune():
        calls.append("called")

    monkeypatch.setattr(ipc_service_module, "prune_screenshots", fake_prune, raising=False)
    monkeypatch.setattr(screenshots, "prune_screenshots", fake_prune, raising=False)

    ipc_service_module.BrowserService(max_browsers=1)

    assert calls == ["called"]
