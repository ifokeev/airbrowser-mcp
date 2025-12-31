#!/usr/bin/env python3
"""Browser IPC Client - Used by Flask API to communicate with browser service."""

import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# IPC directories
QUEUE_DIR = Path("/tmp/browser-queue")
RESPONSE_DIR = Path("/tmp/browser-responses")


class BrowserIPCClient:
    """Client for communicating with browser service via file-based IPC"""

    def __init__(self, timeout: int = 150):  # Increase to 2.5 minutes for driver downloads
        self.timeout = timeout

        # Ensure directories exist
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        RESPONSE_DIR.mkdir(parents=True, exist_ok=True)

    def _send_request(self, request: dict[str, Any], timeout: int | None = None) -> dict[str, Any]:
        """Send request to browser service and wait for response"""
        request_id = str(uuid.uuid4())
        request["request_id"] = request_id
        request["timestamp"] = time.time()

        # Write request file
        request_file = QUEUE_DIR / f"{request_id}.json"
        with open(request_file, "w") as f:
            json.dump(request, f)

        logger.debug(f"Sent request {request_id}: {request}")

        # Wait for response
        response_file = RESPONSE_DIR / f"{request_id}.json"
        start_time = time.time()
        # Add small slack to avoid race with downstream processing
        try:
            slack = int(os.environ.get("IPC_TIMEOUT_SLACK", 5))
        except Exception:
            slack = 5
        actual_timeout = (timeout if timeout is not None else self.timeout) + slack

        while time.time() - start_time < actual_timeout:
            if response_file.exists():
                try:
                    with open(response_file) as f:
                        response = json.load(f)

                    # Clean up response file
                    response_file.unlink()

                    logger.debug(f"Received response for {request_id}: {response}")
                    return response

                except Exception as e:
                    logger.error(f"Error reading response file: {e}")
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

        # Timeout - try to clean up request file
        try:
            request_file.unlink()
        except:
            pass

        raise TimeoutError(f"Timeout waiting for response to request {request_id}")

    def create_browser(self, config: dict[str, Any] | None = None, browser_id: str | None = None) -> str:
        """Create a new browser (synchronous - waits for completion)

        Args:
            config: Browser configuration
            browser_id: Optional pre-generated browser ID (for tracking before creation completes)
        """
        if browser_id is None:
            browser_id = str(uuid.uuid4())

        request = {"type": "create_browser", "browser_id": browser_id, "config": config or {}}

        response = self._send_request(request)

        if response.get("status") != "success":
            raise Exception(f"Failed to create browser: {response.get('message')}")

        return response.get("browser_id", browser_id)

    def get_browser_status(self, browser_id: str) -> dict[str, Any]:
        """Get status of a specific browser"""
        request = {"type": "browser_status", "browser_id": browser_id}

        return self._send_request(request, timeout=5)  # Quick timeout for status checks

    def execute_command(
        self, browser_id: str, command_type: str, timeout: int | None = None, **kwargs
    ) -> dict[str, Any]:
        """Execute command on a browser"""
        request = {"type": "browser_command", "browser_id": browser_id, "command": {"type": command_type, **kwargs}}

        # Use appropriate default timeout based on command type
        if timeout is None:
            if command_type == "navigate":
                timeout = int(os.environ.get("NAVIGATE_TIMEOUT_DEFAULT", 60))
            elif command_type in ("what_is_visible", "detect_coordinates"):
                # Vision commands need longer timeout for API calls
                timeout = int(os.environ.get("VISION_TIMEOUT_DEFAULT", 60))
            else:
                timeout = int(os.environ.get("COMMAND_TIMEOUT_DEFAULT", 20))

        # Include the timeout in the command payload so the service uses it
        # (Service extracts and applies this per-command timeout.)
        request["command"]["timeout"] = timeout

        response = self._send_request(request, timeout=timeout)
        return response

    def close_browser(self, browser_id: str) -> bool:
        """Close a browser"""
        response = self.execute_command(browser_id, "close")
        return response.get("status") == "success"

    def kill_browser(self, browser_id: str) -> dict[str, Any]:
        """Kill a browser - saves state before terminating (can be restored later)."""
        request = {"type": "kill_browser", "browser_id": browser_id}
        return self._send_request(request, timeout=30)

    def kill_all(self) -> dict[str, Any]:
        """Kill all browsers - saves state before terminating (can be restored later)."""
        request = {"type": "kill_all"}
        return self._send_request(request, timeout=60)

    def close_all(self) -> dict[str, Any]:
        """Close all browsers gracefully and clear saved state (cannot be restored)."""
        request = {"type": "close_all"}
        return self._send_request(request, timeout=60)

    def restore(self) -> dict[str, Any]:
        """Restore killed browsers from saved state."""
        request = {"type": "restore"}
        return self._send_request(request, timeout=120)  # Longer timeout for restoring multiple browsers

    def get_status(self) -> dict[str, Any]:
        """Get service status"""
        request = {"type": "status"}

        try:
            response = self._send_request(request)
            return response
        except TimeoutError:
            # Service might be down
            return {
                "status": "error",
                "message": "Browser service not responding",
                "total_browsers": 0,
                "active_browsers": 0,
                "max_browsers": 0,
                "browsers": {},
            }
