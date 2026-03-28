#!/usr/bin/env python3
"""Cross-platform local launcher for airbrowser (no Docker required).

Works on Linux, macOS, and Windows. Starts the browser service and Flask API
as native processes using the host's Chrome installation.

Usage:
    python run_local.py              # Start all services
    python run_local.py --headless   # Linux: skip Xvfb (use Chrome --headless)
    python run_local.py --port 9000  # Custom API port
"""

import argparse
import os
import platform
import signal
import subprocess
import sys
import time
from pathlib import Path

# Ensure src/ is importable
SRC_DIR = str(Path(__file__).resolve().parent / "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def ensure_data_dirs():
    """Create local data directories."""
    data_dir = Path(__file__).resolve().parent / ".data"
    for subdir in ["browser-profiles", "screenshots", "downloads", "state"]:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)
    return data_dir


def check_chrome():
    """Verify Chrome is installed."""
    system = platform.system()
    chrome_paths = {
        "Linux": [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ],
        "Darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ],
        "Windows": [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ],
    }

    for path in chrome_paths.get(system, []):
        if os.path.exists(path):
            print(f"  Chrome found: {path}")
            return True

    print("  WARNING: Chrome not found in standard locations.")
    print("  SeleniumBase will attempt to download it automatically.")
    return False


def start_xvfb():
    """Start Xvfb on Linux if no display is available. Returns process or None."""
    if platform.system() != "Linux":
        return None

    if os.environ.get("DISPLAY"):
        print(f"  Using existing display: {os.environ['DISPLAY']}")
        return None

    # No display — start Xvfb
    display = ":49"
    try:
        proc = subprocess.Popen(
            ["Xvfb", display, "-screen", "0", "1600x900x24", "-ac", "+extension", "GLX", "-noreset"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        if proc.poll() is not None:
            print("  WARNING: Xvfb failed to start. Install with: sudo apt install xvfb")
            print("  Continuing without virtual display (Chrome may fail).")
            return None
        os.environ["DISPLAY"] = display
        print(f"  Xvfb started on {display}")
        return proc
    except FileNotFoundError:
        print("  WARNING: Xvfb not found. Install with: sudo apt install xvfb")
        print("  On a headless server, Chrome will not work without Xvfb or --headless flag.")
        return None


def main():
    parser = argparse.ArgumentParser(description="Run airbrowser locally without Docker")
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    parser.add_argument("--max-browsers", type=int, default=5, help="Max concurrent browsers (default: 5)")
    parser.add_argument("--headless", action="store_true", help="Linux: skip Xvfb, rely on Chrome headless")
    parser.add_argument("--no-mcp", action="store_true", help="Disable MCP server")
    args = parser.parse_args()

    print("=" * 50)
    print("  airbrowser - Local Mode (no Docker)")
    print("=" * 50)
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Python:   {sys.executable}")

    # Check Chrome
    check_chrome()

    # Set up data directories
    data_dir = ensure_data_dirs()
    print(f"  Data dir: {data_dir}")

    # Environment
    env = {
        **os.environ,
        "PYTHONPATH": SRC_DIR,
        "AIRBROWSER_DATA_DIR": str(data_dir),
        "MAX_BROWSERS": str(args.max_browsers),
        "BROWSER_POOL_HOST": "127.0.0.1",
        "BROWSER_POOL_PORT": str(args.port),
        "ENABLE_MCP": "false" if args.no_mcp else "true",
    }

    # Start Xvfb if needed (Linux headless)
    xvfb_proc = None
    if not args.headless:
        xvfb_proc = start_xvfb()
        if xvfb_proc:
            env["DISPLAY"] = os.environ["DISPLAY"]

    processes = []

    def cleanup(signum=None, frame=None):
        print("\n  Shutting down...")
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(f"  Stopped {name}")
            except Exception:
                proc.kill()
                print(f"  Killed {name}")
        if xvfb_proc:
            xvfb_proc.terminate()
            print("  Stopped Xvfb")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    if platform.system() != "Windows":
        signal.signal(signal.SIGHUP, cleanup)

    # Start browser service
    print("\n  Starting browser service...")
    browser_service = subprocess.Popen(
        [sys.executable, "-m", "airbrowser.server.ipc.service"],
        env=env,
        cwd=Path(__file__).resolve().parent,
    )
    processes.append(("browser-service", browser_service))
    time.sleep(1)

    if browser_service.poll() is not None:
        print("  ERROR: Browser service failed to start!")
        cleanup()
        return

    # Start Flask API
    print("  Starting Flask API...")
    flask_env = {**env}
    flask_api = subprocess.Popen(
        [sys.executable, "-m", "airbrowser.server.app"],
        env=flask_env,
        cwd=Path(__file__).resolve().parent,
    )
    processes.append(("flask-api", flask_api))
    time.sleep(2)

    if flask_api.poll() is not None:
        print("  ERROR: Flask API failed to start!")
        cleanup()
        return

    mcp_info = "" if args.no_mcp else " | MCP: http://127.0.0.1:3099"
    print(f"""
  ============================================
  airbrowser is running locally!

  API:       http://127.0.0.1:{args.port}
  Dashboard: http://127.0.0.1:{args.port}/dashboard
  Docs:      http://127.0.0.1:{args.port}/docs/{mcp_info}

  Press Ctrl+C to stop
  ============================================
""")

    # Monitor processes
    try:
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"  WARNING: {name} exited with code {proc.returncode}")
                    cleanup()
                    return
            time.sleep(2)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
