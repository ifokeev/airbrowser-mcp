#!/usr/bin/env python3
"""Standalone browser service (outside Flask), processing IPC commands."""

import json
import logging
import os
import signal
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any

# Add src to path (needed for StateManager import)
sys.path.insert(0, "/app/src")

from airbrowser.server.services.state_manager import StateManager

# Set display before importing SeleniumBase
os.environ["DISPLAY"] = ":99"


def _env_truthy(name: str, default: bool = True) -> bool:
    """Check if environment variable is truthy."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Directories for IPC
QUEUE_DIR = Path("/tmp/browser-queue")
STATUS_DIR = Path("/tmp/browser-status")
RESPONSE_DIR = Path("/tmp/browser-responses")


class BrowserInstance:
    """Manages a single browser instance"""

    def __init__(self, browser_id: str, config: dict | None = None):
        self.browser_id = browser_id
        self.config = config or {}  # Store config for session restore
        self.process = None
        self.launcher_pid = None
        self.session_id = None
        self.status = "creating"
        self.created_at = time.time()

    def init_browser(self, config: dict[str, Any]) -> dict[str, Any]:
        """Initialize browser using subprocess"""
        logger.info(f"Initializing browser {self.browser_id} with config: {config}")

        try:
            import json
            import subprocess
            from pathlib import Path

            # Create status file path
            status_dir = Path("/tmp/browser-status")
            status_dir.mkdir(exist_ok=True)
            status_file = status_dir / f"{self.browser_id}.json"

            # Launch browser in separate process with full command support
            cmd = ["python3", "/app/src/airbrowser/server/browser/launcher.py", self.browser_id, json.dumps(config)]

            # Start process without waiting
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                env={**os.environ, "DISPLAY": ":99", "HOME": "/home/browseruser", "PYTHONPATH": "/app/src"},
            )

            self.launcher_pid = process.pid
            self.process = process
            self.status = "creating"

            # Wait for browser to be ready (with timeout)
            start_time = time.time()
            timeout = 30

            while time.time() - start_time < timeout:
                # Check if process died
                if process.poll() is not None:
                    stderr = process.stderr.read().decode() if process.stderr else ""
                    self.status = "error"
                    error_msg = f"Browser process exited with code {process.returncode}. Stderr: {stderr}"
                    logger.error(f"Browser {self.browser_id} process died: {error_msg}")
                    return {"status": "error", "message": error_msg}

                if status_file.exists():
                    try:
                        with open(status_file) as f:
                            status_data = json.load(f)

                        if status_data.get("status") == "ready":
                            self.session_id = status_data.get("session_id")
                            self.status = "ready"
                            logger.info(f"Browser {self.browser_id} ready with PID {process.pid}")
                            return {"status": "success", "session_id": self.session_id, "pid": process.pid}
                        elif status_data.get("status") == "error":
                            self.status = "error"
                            error_msg = status_data.get("error", "Unknown error")
                            traceback = status_data.get("traceback", "")
                            logger.error(f"Browser {self.browser_id} failed: {error_msg}")
                            if traceback:
                                logger.error(f"Traceback: {traceback}")
                            return {"status": "error", "message": error_msg}
                    except:
                        pass

                time.sleep(0.5)

            # Timeout - kill the process and capture stderr
            if process.poll() is None:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()

                # Try to read any stderr
                stderr = ""
                try:
                    stderr = process.stderr.read().decode() if process.stderr else ""
                except:
                    pass

                logger.error(f"Browser {self.browser_id} creation timed out. Stderr: {stderr}")

            self.status = "error"
            return {
                "status": "error",
                "message": f"Browser creation timed out. Last stderr: {stderr if stderr else 'No stderr captured'}",
            }
        except Exception as e:
            self.status = "error"
            error_msg = str(e)
            logger.error(f"Failed to initialize browser {self.browser_id}: {error_msg}")
            return {"status": "error", "message": error_msg}

    def execute_command(self, command: dict[str, Any], timeout: int | None = None) -> dict[str, Any]:
        """Execute a browser command via file-based IPC"""
        import os
        import uuid
        from pathlib import Path

        # Use provided timeout or default from environment (default 20 seconds)
        if timeout is None:
            timeout = int(os.environ.get("COMMAND_TIMEOUT_DEFAULT", 20))

        cmd_type = command.get("type")

        # Send command to browser process via file IPC
        request_id = str(uuid.uuid4())
        command["request_id"] = request_id

        # Write command file
        cmd_dir = Path(f"/tmp/browser-commands/{self.browser_id}")
        cmd_dir.mkdir(parents=True, exist_ok=True)
        cmd_file = cmd_dir / f"{request_id}.json"
        tmp_file = cmd_dir / f"{request_id}.json.tmp"

        # Atomic write: write to temp and rename
        with open(tmp_file, "w") as f:
            json.dump(command, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file, cmd_file)

        # Wait for response (with timeout)
        resp_dir = Path(f"/tmp/browser-responses/{self.browser_id}")
        resp_dir.mkdir(parents=True, exist_ok=True)
        resp_file = resp_dir / f"{request_id}.json"

        start_time = time.time()

        while time.time() - start_time < timeout:
            if resp_file.exists():
                try:
                    with open(resp_file) as f:
                        result = json.load(f)
                    resp_file.unlink()  # Clean up response file
                    return result
                except:
                    pass
            time.sleep(0.1)

        # Timeout - try to clean up command file
        try:
            cmd_file.unlink()
        except:
            pass

        return {"status": "error", "message": f"Command '{cmd_type}' timed out after {timeout} seconds"}

    def close(self):
        """Close the browser"""
        from pathlib import Path

        # First send close command to browser to trigger graceful shutdown
        # Use a shorter timeout since browser will exit after processing
        self.execute_command({"type": "close"}, timeout=2)

        # Then remove status file to ensure cleanup
        status_file = Path(f"/tmp/browser-status/{self.browser_id}.json")
        if status_file.exists():
            try:
                status_file.unlink()
            except:
                pass

        # Kill the process if we have it (as backup)
        if hasattr(self, "process") and self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            self.process = None
        elif self.launcher_pid:
            try:
                import os
                import signal

                os.kill(self.launcher_pid, signal.SIGTERM)
                # Clean up zombie process
                os.waitpid(self.launcher_pid, os.WNOHANG)
            except:
                pass

        self.launcher_pid = None
        self.status = "closed"
        return {"status": "success"}


class BrowserService:
    """Service that manages browsers and processes commands via file-based IPC"""

    def __init__(self, max_browsers: int = 10):
        self.max_browsers = max_browsers
        self.browsers: dict[str, BrowserInstance] = {}
        self.running = True
        # Default navigation timeout (can be overridden per-command)
        try:
            self.navigate_timeout_default = int(os.environ.get("NAVIGATE_TIMEOUT_DEFAULT", 60))
        except Exception:
            self.navigate_timeout_default = 60

        # Ensure directories exist
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        STATUS_DIR.mkdir(parents=True, exist_ok=True)
        RESPONSE_DIR.mkdir(parents=True, exist_ok=True)

        # Clean up old files
        self._cleanup_old_files()

        # Session restore on startup
        self.session_restore_enabled = _env_truthy("ENABLE_SESSION_RESTORE", default=True)
        if self.session_restore_enabled:
            self._restore_state()

        logger.info(f"Browser service started with max_browsers={max_browsers}")

    def _cleanup_old_files(self):
        """Clean up old IPC files"""
        for dir_path in [QUEUE_DIR, STATUS_DIR, RESPONSE_DIR]:
            for file_path in dir_path.glob("*.json"):
                try:
                    # Remove files older than 5 minutes
                    if time.time() - file_path.stat().st_mtime > 300:
                        file_path.unlink()
                except:
                    pass

    def _restore_state(self):
        """Restore browsers from saved state on startup."""
        browsers_state = StateManager.load_state()
        if not browsers_state:
            return

        logger.info(f"Restoring {len(browsers_state)} browser(s) from saved state...")
        restored_count = 0

        for browser_state in browsers_state:
            try:
                browser_id = browser_state.get("browser_id", str(uuid.uuid4()))
                config = browser_state.get("config", {})
                tabs = browser_state.get("tabs", [])

                # Check if we're at max capacity
                if len(self.browsers) >= self.max_browsers:
                    logger.warning(f"Max browsers reached, skipping restore of {browser_id}")
                    break

                # Create browser instance
                browser = BrowserInstance(browser_id, config)
                result = browser.init_browser(config)

                if result["status"] != "success":
                    logger.warning(f"Failed to restore browser {browser_id}: {result.get('message')}")
                    continue

                self.browsers[browser_id] = browser

                # Restore tabs
                if tabs:
                    self._restore_tabs(browser, tabs)

                restored_count += 1
                logger.info(f"Restored browser {browser_id} with {len(tabs)} tab(s)")

            except Exception as e:
                logger.error(f"Error restoring browser: {e}")
                continue

        # Clear state file after restore attempt
        StateManager.clear_state()
        logger.info(f"Session restore complete: {restored_count}/{len(browsers_state)} browser(s) restored")

    def _restore_tabs(self, browser: "BrowserInstance", tabs: list[dict]):
        """Restore tabs for a browser."""
        if not tabs:
            return

        active_tab_index = 0

        for i, tab in enumerate(tabs):
            url = tab.get("url", "")
            is_active = tab.get("active", False)

            if is_active:
                active_tab_index = i

            # Skip non-restorable URLs
            if not StateManager.is_restorable_url(url):
                continue

            try:
                if i == 0:
                    # First tab - navigate existing tab
                    browser.execute_command({"type": "navigate", "url": url}, timeout=30)
                else:
                    # Additional tabs - open new tab with URL
                    browser.execute_command({"type": "new_tab", "url": url}, timeout=30)
            except Exception as e:
                logger.warning(f"Failed to restore tab {i} with URL {url}: {e}")

        # Switch to the previously active tab
        if active_tab_index > 0:
            try:
                browser.execute_command({"type": "switch_tab", "index": active_tab_index}, timeout=5)
            except Exception as e:
                logger.warning(f"Failed to switch to active tab {active_tab_index}: {e}")

    def _update_browser_state(self, browser_id: str):
        """Update saved state for a single browser (called after navigate, new tab, etc.)."""
        if not self.session_restore_enabled:
            return

        state = self._get_browser_state_for_save(browser_id)
        if not state:
            return

        # Load existing state and update entry for this browser
        existing = StateManager.load_state() or []
        existing = [b for b in existing if b.get("browser_id") != browser_id]
        existing.append(state)
        StateManager.save_state(existing)
        logger.debug(f"Updated saved state for browser {browser_id}")

    def _remove_browser_state(self, browser_id: str):
        """Remove a browser from saved state (called when browser is closed)."""
        if not self.session_restore_enabled:
            return

        existing = StateManager.load_state() or []
        updated = [b for b in existing if b.get("browser_id") != browser_id]
        if len(updated) != len(existing):
            if updated:
                StateManager.save_state(updated)
            else:
                # Empty list - clear the state file entirely
                StateManager.clear_state()
            logger.info(f"Removed browser {browser_id} from saved state")

    def _save_state(self):
        """Save browser state before shutdown."""
        if not self.browsers:
            logger.info("No browsers to save")
            return

        logger.info(f"Saving state for {len(self.browsers)} browser(s)...")
        browsers_state = []

        for browser_id, browser in self.browsers.items():
            if browser.status != "ready":
                logger.debug(f"Skipping browser {browser_id} with status {browser.status}")
                continue

            try:
                # Get all tabs (use longer timeout during shutdown)
                result = browser.execute_command({"type": "list_tabs"}, timeout=10)
                tabs = []

                if result.get("status") == "success":
                    # Response may have tabs directly or in data
                    tab_list = result.get("tabs", [])
                    if not tab_list and result.get("data"):
                        tab_list = result["data"].get("tabs", [])

                    for tab in tab_list:
                        url = tab.get("url", "")
                        if StateManager.is_restorable_url(url):
                            tabs.append(
                                {
                                    "url": url,
                                    "active": tab.get("is_active", False),
                                }
                            )
                    logger.info(f"Browser {browser_id}: found {len(tabs)} restorable tab(s)")
                else:
                    logger.warning(f"Failed to get tabs for {browser_id}: {result.get('message', 'unknown error')}")

                browser_state = {
                    "browser_id": browser_id,
                    "config": browser.config,
                    "tabs": tabs,
                    "created_at": browser.created_at,
                }
                browsers_state.append(browser_state)

            except Exception as e:
                logger.warning(f"Failed to get state for browser {browser_id}: {e}")
                continue

        if browsers_state:
            StateManager.save_state(browsers_state)
        else:
            logger.info("No browser state to save")

    def _write_response(self, request_id: str, response: dict[str, Any]):
        """Write response to file"""
        response_file = RESPONSE_DIR / f"{request_id}.json"
        response["timestamp"] = time.time()

        with open(response_file, "w") as f:
            json.dump(response, f)

        logger.debug(f"Wrote response for {request_id}: {response}")

    def _process_create_browser(self, request: dict[str, Any]):
        """Process browser creation request (synchronous)"""
        request_id = request["request_id"]
        browser_id = request.get("browser_id", str(uuid.uuid4()))
        config = request.get("config", {})

        logger.info(f"Processing create browser request {request_id} for browser {browser_id}")

        # Check if we're at max capacity
        if len(self.browsers) >= self.max_browsers:
            # Try to clean up closed browsers
            closed_browsers = [bid for bid, b in self.browsers.items() if b.status == "closed"]
            for bid in closed_browsers:
                del self.browsers[bid]

            if len(self.browsers) >= self.max_browsers:
                self._write_response(
                    request_id,
                    {"status": "error", "message": f"Maximum number of browsers ({self.max_browsers}) reached"},
                )
                return

        # Create browser instance (store config for session restore)
        browser = BrowserInstance(browser_id, config)
        result = browser.init_browser(config)

        if result["status"] == "success":
            self.browsers[browser_id] = browser
            result["browser_id"] = browser_id

        self._write_response(request_id, result)

    def _process_browser_status(self, request: dict[str, Any]):
        """Process browser status request"""
        request_id = request["request_id"]
        browser_id = request.get("browser_id")

        logger.info(f"Processing browser status request for {browser_id}")

        browser = self.browsers.get(browser_id)
        if not browser:
            self._write_response(request_id, {"status": "error", "message": f"Browser {browser_id} not found"})
            return

        response = {
            "status": "success",
            "browser_id": browser_id,
            "browser_status": browser.status,
            "session_id": browser.session_id,
            "created_at": browser.created_at,
        }

        self._write_response(request_id, response)

    def _process_browser_command(self, request: dict[str, Any]):
        """Process command for existing browser in a worker thread to allow concurrency."""
        request_id = request["request_id"]
        browser_id = request["browser_id"]
        command = request.get("command", {})

        logger.info(f"Processing command {command.get('type')} for browser {browser_id}")

        browser = self.browsers.get(browser_id)
        if not browser:
            self._write_response(request_id, {"status": "error", "message": f"Browser {browser_id} not found"})
            return

        # Extract timeout defaults
        try:
            non_nav_default = int(os.environ.get("COMMAND_TIMEOUT_DEFAULT", 20))
        except Exception:
            non_nav_default = 20
        default_timeout = self.navigate_timeout_default if command.get("type") == "navigate" else non_nav_default
        timeout = command.pop("timeout", default_timeout)

        # Commands that should trigger state save (URL/tab changes)
        STATE_SAVE_COMMANDS = {"navigate", "new_tab", "close_tab"}

        # Worker to execute the command and write the response without blocking main loop
        def worker(req_id: str, bid: str, cmd: dict[str, Any], tout: int):
            try:
                res = browser.execute_command(cmd, timeout=tout)
                cmd_type = cmd.get("type")

                if cmd_type == "close" and res.get("status") == "success":
                    # Remove from browsers dict
                    try:
                        del self.browsers[bid]
                    except KeyError:
                        pass
                    # Always remove from saved state so browser won't be restored
                    try:
                        self._remove_browser_state(bid)
                    except Exception as e:
                        logger.warning(f"Failed to remove browser state: {e}")
                elif cmd_type in STATE_SAVE_COMMANDS and res.get("status") == "success":
                    # Save state after URL/tab changes
                    self._update_browser_state(bid)

                self._write_response(req_id, res)
            except Exception as e:
                self._write_response(req_id, {"status": "error", "message": str(e)})

        t = threading.Thread(target=worker, args=(request_id, browser_id, command, timeout), daemon=True)
        t.start()

    def _process_status_request(self, request: dict[str, Any]):
        """Process status request"""
        request_id = request["request_id"]

        status = {
            "status": "success",
            "total_browsers": len(self.browsers),
            "active_browsers": sum(1 for b in self.browsers.values() if b.status == "ready"),
            "max_browsers": self.max_browsers,
            "browsers": {
                bid: {
                    "id": bid,
                    "status": browser.status,
                    "session_id": browser.session_id,
                    "created_at": browser.created_at,
                }
                for bid, browser in self.browsers.items()
            },
        }

        self._write_response(request_id, status)

    def _get_browser_state_for_save(self, browser_id: str) -> dict[str, Any] | None:
        """Get browser state for saving (used by kill operations)."""
        browser = self.browsers.get(browser_id)
        if not browser or browser.status != "ready":
            return None

        try:
            result = browser.execute_command({"type": "list_tabs"}, timeout=10)
            tabs = []

            if result.get("status") == "success":
                tab_list = result.get("tabs", [])
                if not tab_list and result.get("data"):
                    tab_list = result["data"].get("tabs", [])

                for tab in tab_list:
                    url = tab.get("url", "")
                    if StateManager.is_restorable_url(url):
                        tabs.append(
                            {
                                "url": url,
                                "active": tab.get("is_active", False),
                            }
                        )

            return {
                "browser_id": browser_id,
                "config": browser.config,
                "tabs": tabs,
                "created_at": browser.created_at,
            }
        except Exception as e:
            logger.warning(f"Failed to get state for browser {browser_id}: {e}")
            return None

    def _process_kill_browser(self, request: dict[str, Any]):
        """Process kill browser request - saves state before closing."""
        request_id = request["request_id"]
        browser_id = request.get("browser_id")

        if not browser_id or browser_id not in self.browsers:
            self._write_response(
                request_id,
                {
                    "status": "error",
                    "message": f"Browser {browser_id} not found",
                },
            )
            return

        # Get browser state before killing
        state = self._get_browser_state_for_save(browser_id)
        tabs_saved = 0

        if state:
            # Load existing saved state and append
            existing = StateManager.load_state() or []
            existing = [b for b in existing if b.get("browser_id") != browser_id]
            existing.append(state)
            StateManager.save_state(existing)
            tabs_saved = len(state.get("tabs", []))

        # Close the browser
        browser = self.browsers.pop(browser_id)
        browser.close()

        self._write_response(
            request_id,
            {
                "status": "success",
                "message": f"Browser {browser_id} killed (state saved for restore)",
                "data": {"browser_id": browser_id, "tabs_saved": tabs_saved},
            },
        )

    def _kill_all_impl(self) -> int:
        """Kill all browsers - saves state and closes them. Returns count of killed browsers."""
        if not self.browsers:
            return 0

        # Collect state for all browsers
        states = []
        for browser_id in list(self.browsers.keys()):
            state = self._get_browser_state_for_save(browser_id)
            if state:
                states.append(state)

        # Save all states
        if states:
            StateManager.save_state(states)

        # Close all browsers
        killed = len(self.browsers)
        for browser in self.browsers.values():
            browser.close()
        self.browsers.clear()

        return killed

    def _process_kill_all(self, request: dict[str, Any]):
        """Process kill all browsers request - saves state before closing."""
        request_id = request["request_id"]

        killed = self._kill_all_impl()

        self._write_response(
            request_id,
            {
                "status": "success",
                "message": f"Killed {killed} browser(s) (state saved for restore)" if killed else "No browsers to kill",
                "data": {"killed": killed},
            },
        )

    def _process_close_all(self, request: dict[str, Any]):
        """Process close all browsers request - closes gracefully and clears state."""
        request_id = request["request_id"]

        # Close all browsers without saving state
        closed = len(self.browsers)
        for browser in self.browsers.values():
            try:
                browser.close()
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
        self.browsers.clear()

        # Clear saved state so browsers don't restore on restart
        StateManager.save_state([])

        self._write_response(
            request_id,
            {
                "status": "success",
                "message": f"Closed {closed} browser(s) (state cleared)" if closed else "No browsers to close",
                "data": {"closed": closed},
            },
        )

    def _process_restore(self, request: dict[str, Any]):
        """Process restore browsers request - restores from saved state."""
        request_id = request["request_id"]

        states = StateManager.load_state()
        if not states:
            self._write_response(
                request_id,
                {
                    "status": "success",
                    "message": "No browsers to restore",
                    "data": {"restored": 0},
                },
            )
            return

        restored = []
        failed = []

        for state in states:
            try:
                old_id = state.get("browser_id", "unknown")
                config = state.get("config", {})
                tabs = state.get("tabs", [])

                # Check if we're at max capacity
                if len(self.browsers) >= self.max_browsers:
                    logger.warning(f"Max browsers reached, skipping restore of {old_id}")
                    failed.append(old_id)
                    continue

                # Create new browser
                browser_id = str(uuid.uuid4())
                browser = BrowserInstance(browser_id, config)
                result = browser.init_browser(config)

                if result["status"] != "success":
                    logger.warning(f"Failed to restore browser {old_id}: {result.get('message')}")
                    failed.append(old_id)
                    continue

                self.browsers[browser_id] = browser

                # Restore tabs
                if tabs:
                    self._restore_tabs(browser, tabs)

                restored.append(
                    {
                        "old_id": old_id,
                        "new_id": browser_id,
                        "tabs": len(tabs),
                    }
                )

            except Exception as e:
                logger.error(f"Error restoring browser: {e}")
                failed.append(state.get("browser_id", "unknown"))

        # Clear state file after restore
        StateManager.clear_state()

        self._write_response(
            request_id,
            {
                "status": "success",
                "message": f"Restored {len(restored)} browser(s)",
                "data": {
                    "restored": len(restored),
                    "failed": len(failed),
                    "browsers": restored,
                },
            },
        )

    def process_request_file(self, request_file: Path):
        """Process a single request file"""
        try:
            with open(request_file) as f:
                request = json.load(f)

            request_type = request.get("type")

            if request_type == "create_browser":
                self._process_create_browser(request)
            elif request_type == "browser_status":
                self._process_browser_status(request)
            elif request_type == "browser_command":
                self._process_browser_command(request)
            elif request_type == "status":
                self._process_status_request(request)
            elif request_type == "kill_browser":
                self._process_kill_browser(request)
            elif request_type == "kill_all":
                self._process_kill_all(request)
            elif request_type == "close_all":
                self._process_close_all(request)
            elif request_type == "restore":
                self._process_restore(request)
            else:
                logger.warning(f"Unknown request type: {request_type}")

            # Delete the request file after processing
            request_file.unlink()

        except Exception as e:
            logger.error(f"Error processing request file {request_file}: {e}")
            try:
                request_file.unlink()
            except:
                pass

    def run(self):
        """Main service loop"""
        logger.info("Browser service running, monitoring queue directory...")

        # Register signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            sig_name = signal.Signals(signum).name
            logger.info(f"Received {sig_name}, shutting down gracefully...")
            self.running = False

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        while self.running:
            try:
                # Check for request files
                request_files = sorted(QUEUE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)

                for request_file in request_files:
                    self.process_request_file(request_file)

                # Small delay to prevent CPU spinning
                time.sleep(0.1)

            except KeyboardInterrupt:
                logger.info("Received interrupt, shutting down...")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)

        # Cleanup
        self.cleanup()

    def cleanup(self):
        """Clean up all browsers, saving state first if enabled."""
        logger.info("Cleaning up browsers...")

        if self.session_restore_enabled:
            # Use kill_all to save state and close browsers
            killed = self._kill_all_impl()
            logger.info(f"Killed {killed} browser(s) with state saved")
        else:
            # Just close without saving state
            for browser in self.browsers.values():
                browser.close()
            self.browsers.clear()

        logger.info("Browser service stopped")


if __name__ == "__main__":
    # Get max browsers from environment or use default
    max_browsers = int(os.environ.get("MAX_BROWSERS", 10))

    # Create and run service
    service = BrowserService(max_browsers)
    service.run()
