#!/usr/bin/env python3
"""
Test suite for session restore feature.

Unit tests for StateManager class and state persistence logic.

Run with: pytest tests/test_session_restore.py -v
"""

import importlib.util
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

# Import state_manager module directly without triggering flask-dependent __init__.py
# This allows tests to run in minimal test container without flask
_STATE_MANAGER_PATH = Path(__file__).parent.parent / "src" / "airbrowser" / "server" / "services" / "state_manager.py"


def _load_state_manager_module():
    """Load state_manager module directly from file to avoid package import chain."""
    spec = importlib.util.spec_from_file_location("state_manager", _STATE_MANAGER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestStateManager:
    """Unit tests for StateManager class."""

    @pytest.fixture
    def temp_state_dir(self):
        """Create a temporary directory for state files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def state_manager(self, temp_state_dir):
        """Create StateManager with patched paths by loading module directly."""
        sm = _load_state_manager_module()

        # Patch module-level constants
        sm.STATE_DIR = temp_state_dir
        sm.STATE_FILE = temp_state_dir / "browsers.json"

        return sm.StateManager

    def test_save_empty_browsers_succeeds(self, state_manager, temp_state_dir):
        """Test saving empty browser list succeeds without creating file."""
        result = state_manager.save_state([])
        assert result is True
        # No file should be created for empty list
        state_file = temp_state_dir / "browsers.json"
        assert not state_file.exists()

    def test_save_single_browser(self, state_manager, temp_state_dir):
        """Test saving a single browser state."""
        browsers = [
            {
                "browser_id": "test-browser-1",
                "config": {"window_size": [1920, 1080]},
                "tabs": [{"url": "https://example.com", "active": True}],
                "created_at": datetime.now(timezone.utc).timestamp(),
            }
        ]

        result = state_manager.save_state(browsers)
        assert result is True

        # Verify file was created
        state_file = temp_state_dir / "browsers.json"
        assert state_file.exists()

        # Verify contents
        with open(state_file) as f:
            saved = json.load(f)

        assert saved["version"] == 1
        assert "saved_at" in saved
        assert len(saved["browsers"]) == 1
        assert saved["browsers"][0]["browser_id"] == "test-browser-1"

    def test_save_multiple_browsers_with_tabs(self, state_manager, temp_state_dir):
        """Test saving multiple browsers with multiple tabs each."""
        browsers = [
            {
                "browser_id": "browser-1",
                "config": {"window_size": [1920, 1080], "profile_name": "user1"},
                "tabs": [
                    {"url": "https://example.com", "active": True},
                    {"url": "https://docs.example.com", "active": False},
                ],
                "created_at": 1700000000.0,
            },
            {
                "browser_id": "browser-2",
                "config": {"window_size": [1280, 720]},
                "tabs": [
                    {"url": "https://httpbin.org/html", "active": True},
                ],
                "created_at": 1700000100.0,
            },
        ]

        result = state_manager.save_state(browsers)
        assert result is True

        # Load and verify
        loaded = state_manager.load_state()
        assert loaded is not None
        assert len(loaded) == 2
        assert len(loaded[0]["tabs"]) == 2
        assert len(loaded[1]["tabs"]) == 1

    def test_load_nonexistent_file_returns_none(self, state_manager, temp_state_dir):
        """Test loading when no state file exists returns None."""
        result = state_manager.load_state()
        assert result is None

    def test_load_corrupted_file_returns_none(self, state_manager, temp_state_dir):
        """Test loading corrupted JSON returns None."""
        state_file = temp_state_dir / "browsers.json"
        state_file.write_text("{ invalid json }")

        result = state_manager.load_state()
        assert result is None

    def test_load_wrong_version_returns_none(self, state_manager, temp_state_dir):
        """Test loading state with wrong version returns None."""
        state_file = temp_state_dir / "browsers.json"
        state = {
            "version": 999,  # Wrong version
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "browsers": [{"browser_id": "test"}],
        }
        state_file.write_text(json.dumps(state))

        result = state_manager.load_state()
        assert result is None

    def test_clear_state_removes_file(self, state_manager, temp_state_dir):
        """Test clearing state removes the file."""
        # Create a state file
        browsers = [{"browser_id": "test", "config": {}, "tabs": [], "created_at": 0}]
        state_manager.save_state(browsers)

        state_file = temp_state_dir / "browsers.json"
        assert state_file.exists()

        # Clear it
        result = state_manager.clear_state()
        assert result is True
        assert not state_file.exists()

    def test_clear_nonexistent_file_succeeds(self, state_manager, temp_state_dir):
        """Test clearing when no file exists still succeeds."""
        result = state_manager.clear_state()
        assert result is True

    def test_save_load_roundtrip(self, state_manager, temp_state_dir):
        """Test that save and load are symmetrical."""
        original_browsers = [
            {
                "browser_id": "roundtrip-test",
                "config": {
                    "window_size": [1920, 1080],
                    "profile_name": "test-profile",
                    "proxy": "http://proxy:8080",
                },
                "tabs": [
                    {"url": "https://example.com/page1", "active": False},
                    {"url": "https://example.com/page2", "active": True},
                    {"url": "https://example.com/page3", "active": False},
                ],
                "created_at": 1700000000.123,
            }
        ]

        state_manager.save_state(original_browsers)
        loaded_browsers = state_manager.load_state()

        assert loaded_browsers == original_browsers


class TestIsRestorableUrl:
    """Test URL filtering for restore."""

    @pytest.fixture
    def state_manager(self):
        """Load StateManager class directly."""
        sm = _load_state_manager_module()
        return sm.StateManager

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://example.com", True),
            ("http://localhost:8000", True),
            ("https://www.google.com/search?q=test", True),
            ("about:blank", False),
            ("about:srcdoc", False),
            ("chrome://settings", False),
            ("chrome://newtab", False),
            ("chrome-extension://abc123/popup.html", False),
            ("data:text/html,<h1>Hello</h1>", False),
            ("javascript:void(0)", False),
            ("", False),
            (None, False),
        ],
    )
    def test_is_restorable_url(self, state_manager, url, expected):
        """Test URL filtering logic."""
        result = state_manager.is_restorable_url(url) if url is not None else state_manager.is_restorable_url("")
        # Handle None case
        if url is None:
            result = state_manager.is_restorable_url("")
        else:
            result = state_manager.is_restorable_url(url)
        assert result == expected, f"Expected {expected} for URL: {url}"


@pytest.mark.slow
@pytest.mark.integration
class TestSessionRestoreIntegration:
    """Integration tests for session restore (requires running container)."""

    def test_state_file_location_is_persistent_volume(self):
        """Verify state file is configured for persistent volume."""
        sm = _load_state_manager_module()

        # Default location should be /app/state (mounted volume)
        assert str(sm.STATE_DIR) == "/app/state" or "state" in str(sm.STATE_DIR)
        assert sm.STATE_FILE.name == "browsers.json"
