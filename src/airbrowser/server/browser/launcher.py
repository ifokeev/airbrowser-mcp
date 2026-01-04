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
import subprocess
import sys
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


def start_local_proxy_forwarder(
    upstream_host: str, upstream_port: int, upstream_user: str, upstream_pass: str
) -> tuple[int, "subprocess.Popen"]:
    """Start a local proxy that forwards to an authenticated upstream proxy.

    Uses a simple Python proxy forwarder script to handle authenticated proxy forwarding.
    This is more reliable than pproxy which has issues parsing certain credential formats.

    Args:
        upstream_host: Upstream proxy hostname
        upstream_port: Upstream proxy port
        upstream_user: Upstream proxy username
        upstream_pass: Upstream proxy password

    Returns:
        Tuple of (local_port, process)
    """
    import socket

    # Find a free port for local proxy
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        local_port = s.getsockname()[1]

    # Path to our proxy forwarder script
    forwarder_script = Path(__file__).parent / "proxy_forwarder.py"

    cmd = [
        sys.executable,
        str(forwarder_script),
        str(local_port),
        upstream_host,
        str(upstream_port),
        upstream_user,
        upstream_pass,
    ]

    logger.info(f"Starting proxy forwarder on port {local_port} -> {upstream_host}:{upstream_port}")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,  # Detach from parent
    )

    # Wait for the proxy to signal it's ready
    try:
        # Read stdout until we get the PROXY_READY signal
        ready_line = proc.stdout.readline().decode().strip()
        if not ready_line.startswith("PROXY_READY:"):
            stderr_output = proc.stderr.read().decode() if proc.stderr else ""
            raise RuntimeError(f"Proxy forwarder failed to start: {stderr_output}")
    except Exception as e:
        if proc.poll() is not None:
            stderr_output = proc.stderr.read().decode() if proc.stderr else ""
            raise RuntimeError(f"Proxy forwarder exited (code: {proc.returncode}): {stderr_output}")
        raise RuntimeError(f"Proxy forwarder startup error: {e}")

    logger.info(f"Proxy forwarder started: pid={proc.pid}, port={local_port}")
    return local_port, proc


def create_browser(config: dict):
    """Create and configure a SeleniumBase UC browser instance."""
    from seleniumbase import Driver

    proxy = config.get("proxy")
    user_agent = config.get("user_agent")
    profile_name = config.get("profile_name")

    # Parse proxy credentials and start local forwarder if needed
    local_proxy_proc = None
    effective_proxy = None

    if proxy:
        if "@" in proxy:
            # Has credentials - start local proxy forwarder
            proxy_user, proxy_pass, proxy_server = parse_proxy_credentials(proxy)
            logger.info(f"Proxy with authentication detected: {proxy_user}@{proxy_server}")

            # Parse host and port
            if ":" in proxy_server:
                upstream_host, upstream_port = proxy_server.rsplit(":", 1)
                upstream_port = int(upstream_port)
            else:
                upstream_host = proxy_server
                upstream_port = 80

            # Start local proxy forwarder
            local_port, local_proxy_proc = start_local_proxy_forwarder(
                upstream_host, upstream_port, proxy_user, proxy_pass
            )
            effective_proxy = f"127.0.0.1:{local_port}"
            logger.info(f"Using local proxy forwarder: {effective_proxy} -> {proxy_server}")
        else:
            effective_proxy = proxy
            logger.info(f"Using proxy without auth: {proxy}")

    # UC (undetected chrome) + CDP mode are always enabled
    opts = {
        "browser": "chrome",
        "uc": True,
        "log_cdp": False,
        "uc_cdp": True,
        # Allow CDP WebSocket connections from any origin (required for CDP proxy)
        "chromium_arg": "--remote-allow-origins=*",
    }

    if effective_proxy:
        opts["proxy"] = effective_proxy

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

    return driver, local_proxy_proc


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


def cleanup(driver, status_file: Path, cmd_dir: Path, resp_dir: Path, proxy_proc=None):
    """Clean up browser, proxy process, and IPC directories."""
    try:
        if driver:
            driver.quit()
    except Exception:
        pass

    # Kill local proxy forwarder if it exists
    if proxy_proc:
        try:
            proxy_proc.terminate()
            proxy_proc.wait(timeout=2)
        except Exception:
            try:
                proxy_proc.kill()
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
    proxy_proc = None
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

        # Create browser (and optional proxy forwarder)
        driver, proxy_proc = create_browser(config)

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
            cleanup(driver, status_file, cmd_dir, resp_dir, proxy_proc)


if __name__ == "__main__":
    main()
