"""Session state manager for browser persistence across restarts."""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# State file location (must be on a persistent volume)
STATE_DIR = Path(os.environ.get("STATE_DIR", "/app/state"))
STATE_FILE = STATE_DIR / "browsers.json"
STATE_VERSION = 1


class StateManager:
    """Manages browser state persistence for session restore."""

    @staticmethod
    def save_state(browsers: list[dict[str, Any]]) -> bool:
        """Save browser state to disk.

        Args:
            browsers: List of browser state dicts with keys:
                - browser_id: str
                - config: dict (window_size, profile_name, etc.)
                - tabs: list of {url: str, active: bool}
                - created_at: float (timestamp)

        Returns:
            True if saved successfully, False otherwise.
        """
        if not browsers:
            logger.info("No browsers to save, skipping state save")
            return True

        try:
            # Ensure state directory exists
            STATE_DIR.mkdir(parents=True, exist_ok=True)

            state = {
                "version": STATE_VERSION,
                "saved_at": datetime.now(timezone.utc).isoformat(),
                "browsers": browsers,
            }

            # Atomic write: write to temp file then rename
            tmp_file = STATE_FILE.with_suffix(".json.tmp")
            with open(tmp_file, "w") as f:
                json.dump(state, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            os.replace(tmp_file, STATE_FILE)
            logger.info(f"Saved state for {len(browsers)} browser(s) to {STATE_FILE}")
            return True

        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            return False

    @staticmethod
    def load_state() -> list[dict[str, Any]] | None:
        """Load browser state from disk.

        Returns:
            List of browser state dicts, or None if no state file or error.
        """
        if not STATE_FILE.exists():
            logger.info("No state file found, nothing to restore")
            return None

        try:
            with open(STATE_FILE) as f:
                state = json.load(f)

            version = state.get("version", 0)
            if version != STATE_VERSION:
                logger.warning(f"State version mismatch: {version} != {STATE_VERSION}, skipping restore")
                return None

            browsers = state.get("browsers", [])
            saved_at = state.get("saved_at", "unknown")
            logger.info(f"Loaded state with {len(browsers)} browser(s) from {saved_at}")
            return browsers

        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return None

    @staticmethod
    def clear_state() -> bool:
        """Delete the state file after successful restore.

        Returns:
            True if cleared or didn't exist, False on error.
        """
        try:
            if STATE_FILE.exists():
                STATE_FILE.unlink()
                logger.info(f"Cleared state file: {STATE_FILE}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear state file: {e}")
            return False

    @staticmethod
    def is_restorable_url(url: str) -> bool:
        """Check if a URL should be restored.

        Skips blank pages and internal Chrome URLs.
        """
        if not url:
            return False

        skip_prefixes = (
            "about:",
            "chrome:",
            "chrome-extension:",
            "data:",
            "javascript:",
        )
        return not url.startswith(skip_prefixes)
