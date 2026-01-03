#!/usr/bin/env python3
"""Browser launcher with file-based IPC (SeleniumBase UC + debug tooling).

This is the entry point for individual browser processes. It:
1. Initializes a SeleniumBase UC browser instance
2. Sets up IPC directories for command/response communication
3. Runs a command processing loop using the commands dispatcher
"""

import json
import logging
import os
import re
import sys
import threading
import time
import traceback
import warnings
from datetime import datetime
from pathlib import Path

# Add src to path for absolute imports (needed when run as a script)
sys.path.insert(0, "/app/src")

# Suppress warnings
warnings.filterwarnings("ignore")

# Configure logging - use /tmp which is writable by all users
log_dir = Path("/tmp/browser-launcher-logs")
log_dir.mkdir(parents=True, exist_ok=True)

# Get browser ID early for logging
browser_id = sys.argv[1] if len(sys.argv) > 1 else "unknown"

# Create logger
logger = logging.getLogger("browser_launcher")
logger.setLevel(logging.DEBUG)

# File handler with browser ID in filename
log_file = log_dir / f"browser_{browser_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Console handler for Docker logs (stderr - captured by docker from subprocesses)
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)  # Show all logs in docker compose logs

# Formatter
formatter = logging.Formatter(
    f"[browser_{browser_id}] %(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info(f"Browser launcher starting for browser_id: {browser_id}")

# Set environment
os.environ["DISPLAY"] = ":99"
os.environ["HOME"] = "/home/browseruser"

# Import utilities (using absolute imports)
from airbrowser.server.browser.utils import kill_child_processes


def parse_proxy_credentials(proxy_url: str) -> tuple[str | None, str | None, str]:
    """Parse proxy URL and extract credentials if present.

    Args:
        proxy_url: Proxy URL in format [user:pass@]host:port or http://[user:pass@]host:port

    Returns:
        Tuple of (username, password, proxy_server_without_credentials)
    """
    if not proxy_url:
        return None, None, proxy_url

    # Remove http:// or https:// prefix
    proxy = proxy_url
    if proxy.startswith("http://"):
        proxy = proxy[7:]
    elif proxy.startswith("https://"):
        proxy = proxy[8:]

    # Check for credentials (user:pass@host:port format)
    if "@" in proxy:
        # Pattern: user:pass@host:port
        match = re.match(r"^([^:]+):([^@]+)@(.+)$", proxy)
        if match:
            username, password, server = match.groups()
            return username, password, server

    return None, None, proxy


def setup_cdp_proxy_auth(driver, username: str, password: str):
    """Set up CDP-based proxy authentication using Fetch domain.

    This handles proxy auth requests via Chrome DevTools Protocol instead of
    relying on the Chrome extension approach which can fail with Chrome 137+.
    """
    import urllib.request

    import websocket

    try:
        # Get CDP WebSocket URL from the driver
        cdp_url = None

        # Try to get the CDP endpoint from driver capabilities
        caps = driver.capabilities
        debugger_addr = None

        if "goog:chromeOptions" in caps:
            debugger_addr = caps["goog:chromeOptions"].get("debuggerAddress")

        # Fallback: try to get from se:cdp
        if not cdp_url and "se:cdp" in caps:
            cdp_url = caps["se:cdp"]

        # If we have a debugger address, get the proper WebSocket URL from /json/version
        if debugger_addr and not cdp_url:
            try:
                version_url = f"http://{debugger_addr}/json/version"
                with urllib.request.urlopen(version_url, timeout=5) as resp:
                    version_data = json.loads(resp.read().decode())
                    cdp_url = version_data.get("webSocketDebuggerUrl")
                    logger.debug(f"Got CDP URL from /json/version: {cdp_url}")
            except Exception as e:
                logger.warning(f"Failed to get CDP URL from /json/version: {e}")

        if not cdp_url:
            logger.warning("Could not get CDP WebSocket URL for proxy auth")
            return

        logger.info(f"Setting up CDP proxy auth via {cdp_url}")

        # Create WebSocket connection for CDP events
        def handle_cdp_events():
            """Background thread to handle CDP proxy auth events."""
            ws = None
            try:
                ws = websocket.WebSocket()
                ws.connect(cdp_url, timeout=5)

                # Enable Fetch domain with auth handling
                ws.send(json.dumps({"id": 1, "method": "Fetch.enable", "params": {"handleAuthRequests": True}}))
                logger.info("CDP Fetch.enable sent for proxy auth handling")

                # Process events
                msg_id = 100
                while True:
                    try:
                        msg = ws.recv()
                        if not msg:
                            continue

                        data = json.loads(msg)

                        # Handle auth required event
                        if data.get("method") == "Fetch.authRequired":
                            request_id = data["params"]["requestId"]
                            logger.info(f"Proxy auth requested, providing credentials for request {request_id}")

                            # Respond with credentials
                            auth_response = {
                                "id": msg_id,
                                "method": "Fetch.continueWithAuth",
                                "params": {
                                    "requestId": request_id,
                                    "authChallengeResponse": {
                                        "response": "ProvideCredentials",
                                        "username": username,
                                        "password": password,
                                    },
                                },
                            }
                            ws.send(json.dumps(auth_response))
                            msg_id += 1

                        # Handle paused requests (continue them)
                        elif data.get("method") == "Fetch.requestPaused":
                            request_id = data["params"]["requestId"]
                            continue_response = {
                                "id": msg_id,
                                "method": "Fetch.continueRequest",
                                "params": {"requestId": request_id},
                            }
                            ws.send(json.dumps(continue_response))
                            msg_id += 1

                    except websocket.WebSocketTimeoutException:
                        continue
                    except websocket.WebSocketConnectionClosedException:
                        logger.info("CDP WebSocket closed, stopping proxy auth handler")
                        break
                    except Exception as e:
                        logger.debug(f"CDP event handling error: {e}")

            except Exception as e:
                logger.warning(f"CDP proxy auth setup failed: {e}")
            finally:
                if ws:
                    try:
                        ws.close()
                    except Exception:
                        pass

        # Start background thread for CDP event handling
        auth_thread = threading.Thread(target=handle_cdp_events, daemon=True)
        auth_thread.start()
        logger.info("CDP proxy auth handler thread started")

        # Give the thread time to connect and enable Fetch
        time.sleep(0.5)

    except Exception as e:
        logger.warning(f"Failed to set up CDP proxy auth: {e}")


def create_browser(config: dict):
    """Create and configure a SeleniumBase UC browser instance."""
    from seleniumbase import Driver

    proxy = config.get("proxy")
    user_agent = config.get("user_agent")
    profile_name = config.get("profile_name")

    # Parse proxy credentials if present
    proxy_user, proxy_pass, proxy_server = parse_proxy_credentials(proxy)
    has_proxy_auth = proxy_user is not None and proxy_pass is not None

    if has_proxy_auth:
        logger.info(f"Proxy with authentication detected: {proxy_user}@{proxy_server}")
    elif proxy:
        logger.info(f"Proxy without authentication: {proxy_server}")

    # UC (undetected chrome) + CDP mode are always enabled
    # Pass proxy server WITHOUT credentials - we'll handle auth via CDP
    opts = {
        "browser": "chrome",
        "uc": True,
        "log_cdp": False,
        "uc_cdp": True,
        "proxy": proxy_server if proxy else None,
        # Allow CDP WebSocket connections from any origin (required for CDP proxy)
        "chromium_arg": "--remote-allow-origins=*",
    }

    # Set user_data_dir for persistent profile
    if profile_name:
        profiles_dir = os.environ.get("PROFILES_DIR", "/app/browser-profiles")
        user_data_dir = f"{profiles_dir}/{profile_name}"
        Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        opts["user_data_dir"] = user_data_dir
        logger.info(f"Using profile '{profile_name}' at {user_data_dir}")

    if user_agent:
        opts["user_agent"] = user_agent
    if config.get("disable_images"):
        opts["block_images"] = True
    if config.get("disable_gpu"):
        opts["disable_gpu"] = True

    logger.info(f"Creating browser with options: {opts}")

    try:
        driver = Driver(**opts)
    except Exception as e:
        logger.error(f"Failed to create Driver: {e}")
        raise

    logger.info(f"Browser created successfully, session_id: {getattr(driver, 'session_id', 'unknown')}")

    # Set up CDP-based proxy authentication if credentials were provided
    if has_proxy_auth:
        setup_cdp_proxy_auth(driver, proxy_user, proxy_pass)

    # Set window position and size
    try:
        driver.set_window_position(0, 0)
        window_size = config.get("window_size")
        if window_size:
            # Use specified size
            if isinstance(window_size, list | tuple) and len(window_size) >= 2:
                width, height = int(window_size[0]), int(window_size[1])
            elif isinstance(window_size, str) and "," in window_size:
                width, height = map(int, window_size.split(","))
            else:
                width, height = None, None
            if width and height:
                driver.set_window_size(width, height)
        else:
            # No size specified - maximize
            driver.maximize_window()
    except Exception as e:
        logger.warning(f"Could not set window size: {e}")

    return driver


def run_command_loop(driver, browser_id: str, status_file: Path, cmd_dir: Path, resp_dir: Path):
    """Run the main command processing loop."""
    from airbrowser.server.browser.commands import handle_command

    should_exit = False
    while status_file.exists() and not should_exit:
        # Check for command files
        cmd_files = sorted(cmd_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)

        for cmd_file in cmd_files:
            try:
                # Read command with retry loop to avoid partial reads
                command = None
                for _ in range(5):
                    try:
                        with open(cmd_file) as f:
                            command = json.load(f)
                        break
                    except json.JSONDecodeError:
                        time.sleep(0.02)

                if command is None:
                    raise Exception("Failed to read command JSON (empty or invalid)")

                request_id = command.get("request_id", cmd_file.stem)

                # Process command using dispatcher
                result = handle_command(driver, command, browser_id=browser_id)
                result["request_id"] = request_id
                result["timestamp"] = time.time()

                # Write response atomically
                resp_file = resp_dir / f"{request_id}.json"
                tmp_resp = resp_dir / f"{request_id}.json.tmp"
                with open(tmp_resp, "w") as f:
                    json.dump(result, f)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_resp, resp_file)

                # Delete command file
                cmd_file.unlink()

                # Check if browser should close
                if result.get("action") == "close":
                    should_exit = True
                    break

            except Exception as e:
                logger.error(f"Error processing command: {e}")
                try:
                    error_result = {
                        "status": "error",
                        "message": str(e),
                        "request_id": cmd_file.stem,
                        "timestamp": time.time(),
                    }
                    resp_file = resp_dir / f"{cmd_file.stem}.json"
                    with open(resp_file, "w") as f:
                        json.dump(error_result, f)
                    cmd_file.unlink()
                except Exception:
                    pass

        time.sleep(0.1)  # Small delay to prevent CPU spinning


def cleanup(driver, status_file: Path, cmd_dir: Path, resp_dir: Path):
    """Clean up browser and IPC directories."""
    try:
        if driver:
            driver.quit()
    except Exception:
        pass

    kill_child_processes(os.getpid())

    if status_file.exists():
        try:
            status_file.unlink()
        except Exception:
            pass

    for f in cmd_dir.glob("*.json"):
        try:
            f.unlink()
        except Exception:
            pass
    for f in resp_dir.glob("*.json"):
        try:
            f.unlink()
        except Exception:
            pass
    try:
        cmd_dir.rmdir()
        resp_dir.rmdir()
    except Exception:
        pass


def main():
    """Main entry point for browser launcher."""
    driver = None
    status_file = None
    cmd_dir = None
    resp_dir = None

    try:
        browser_id = sys.argv[1]
        config = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

        logger.info(f"Starting browser {browser_id} with config: {config}")

        # Set up IPC paths
        status_file = Path(f"/tmp/browser-status/{browser_id}.json")
        cmd_dir = Path(f"/tmp/browser-commands/{browser_id}")
        cmd_dir.mkdir(parents=True, exist_ok=True)
        resp_dir = Path(f"/tmp/browser-responses/{browser_id}")
        resp_dir.mkdir(parents=True, exist_ok=True)

        # Write initial status
        status_data = {"browser_id": browser_id, "status": "creating", "pid": os.getpid(), "timestamp": time.time()}
        with open(status_file, "w") as f:
            json.dump(status_data, f)

        # Create browser
        driver = create_browser(config)

        # Update status to ready
        status_data.update(
            {
                "status": "ready",
                "session_id": getattr(driver, "session_id", "unknown"),
                "current_url": driver.current_url,
                "timestamp": time.time(),
            }
        )
        with open(status_file, "w") as f:
            json.dump(status_data, f)

        # Run command loop
        run_command_loop(driver, browser_id, status_file, cmd_dir, resp_dir)

    except Exception as e:
        logger.critical(f"Fatal error in browser {browser_id}: {e}", exc_info=True)
        error_data = {
            "browser_id": browser_id,
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": time.time(),
        }
        try:
            with open(f"/tmp/browser-status/{browser_id}.json", "w") as f:
                json.dump(error_data, f)
        except Exception:
            pass
        sys.exit(1)

    finally:
        if status_file and cmd_dir and resp_dir:
            cleanup(driver, status_file, cmd_dir, resp_dir)


if __name__ == "__main__":
    main()
