#!/usr/bin/env python3
"""Cross-platform local launcher for airbrowser (no Docker required).

Works on Linux, macOS, and Windows. Starts the browser service and Flask API
as native processes using the host's Chrome installation.

Usage:
    python run_local.py              # Start all services
    python run_local.py --vnc        # Enable VNC viewer (Linux, requires x11vnc)
    python run_local.py --port 9000  # Custom API port
"""

import argparse
import os
import platform
import shutil
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


def check_system_deps():
    """Check and install missing system dependencies (Linux only)."""
    if platform.system() != "Linux":
        return

    # All packages needed for browser automation + GUI interaction
    required = {
        "python3-tk": None,  # PyAutoGUI / MouseInfo
        "python3-dev": None,  # Python headers
        "scrot": "scrot",  # PyAutoGUI screenshot backend
        "xdotool": "xdotool",  # PyAutoGUI mouse/keyboard
        "xsel": "xsel",  # Clipboard (PyAutoGUI)
        "xclip": "xclip",  # Clipboard fallback
        "xvfb": "Xvfb",  # Virtual display
    }

    missing = []
    for pkg, binary in required.items():
        if binary is None:
            # Python package — check import
            if pkg == "python3-tk":
                try:
                    import tkinter  # noqa: F401
                except ImportError:
                    missing.append(pkg)
            else:
                missing.append(pkg)  # Always install python3-dev
        elif not shutil.which(binary):
            missing.append(pkg)

    # Optional: x11vnc for --vnc flag
    if not shutil.which("x11vnc"):
        print("  NOTE: x11vnc not installed (needed for --vnc). Install: sudo apt install x11vnc")

    if missing:
        print(f"  Installing missing packages: {' '.join(missing)}")
        try:
            subprocess.run(
                ["sudo", "apt-get", "install", "-y"] + missing,
                check=True,
            )
            print(f"  Installed: {' '.join(missing)}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  WARNING: Could not auto-install: {' '.join(missing)}")
            print(f"  Run manually: sudo apt-get install -y {' '.join(missing)}")
    else:
        print("  System dependencies: OK")


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


def start_vnc(display: str, vnc_port: int = 5900):
    """Start x11vnc on the given display. Returns process or None."""
    if platform.system() != "Linux":
        print("  VNC not needed on Mac/Windows (Chrome opens natively)")
        return None

    try:
        proc = subprocess.Popen(
            [
                "x11vnc",
                "-display",
                display,
                "-forever",
                "-shared",
                "-nopw",
                "-noxdamage",
                "-noxfixes",
                "-noxrandr",
                "-wait",
                "10",
                "-xkb",
                "-noxrecord",
                "-rfbport",
                str(vnc_port),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        if proc.poll() is not None:
            print("  WARNING: x11vnc failed to start. Install with: sudo apt install x11vnc")
            return None
        print(f"  x11vnc started on port {vnc_port}")
        return proc
    except FileNotFoundError:
        print("  WARNING: x11vnc not found. Install with: sudo apt install x11vnc")
        return None


def start_novnc(vnc_port: int = 5900, novnc_port: int = 6080):
    """Start websockify for noVNC web access. Returns process or None."""
    # Look for noVNC in common locations
    novnc_paths = [
        "/opt/noVNC",
        "/usr/share/novnc",
        "/usr/share/noVNC",
        str(Path.home() / ".local" / "share" / "noVNC"),
    ]
    novnc_web = None
    for p in novnc_paths:
        if Path(p).is_dir():
            novnc_web = p
            break

    try:
        cmd = ["websockify"]
        if novnc_web:
            cmd.extend(["--web", novnc_web])
        cmd.extend([str(novnc_port), f"localhost:{vnc_port}"])

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        if proc.poll() is not None:
            print("  WARNING: websockify failed to start. Install with: pip install websockify")
            return None
        if novnc_web:
            print(f"  noVNC web viewer at http://127.0.0.1:{novnc_port}/vnc.html")
        else:
            print(f"  websockify started on port {novnc_port} (noVNC files not found, use a VNC client)")
        return proc
    except FileNotFoundError:
        print("  WARNING: websockify not found. Install with: pip install websockify")
        return None


def main():
    parser = argparse.ArgumentParser(description="Run airbrowser locally without Docker")
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    parser.add_argument("--max-browsers", type=int, default=5, help="Max concurrent browsers (default: 5)")
    parser.add_argument("--vnc", action="store_true", help="Enable VNC + noVNC web viewer (Linux)")
    parser.add_argument("--vnc-port", type=int, default=5900, help="VNC port (default: 5900)")
    parser.add_argument("--novnc-port", type=int, default=6080, help="noVNC web port (default: 6080)")
    parser.add_argument("--no-mcp", action="store_true", help="Disable MCP server")
    args = parser.parse_args()

    print("=" * 50)
    print("  airbrowser - Local Mode (no Docker)")
    print("=" * 50)
    print(f"  Platform: {platform.system()} {platform.machine()}")
    print(f"  Python:   {sys.executable}")

    # Check system deps and Chrome
    check_system_deps()
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

    # Start Xvfb if needed (Linux without a display)
    xvfb_proc = start_xvfb()
    if xvfb_proc:
        env["DISPLAY"] = os.environ["DISPLAY"]

    # Start VNC if requested
    vnc_proc = None
    novnc_proc = None
    if args.vnc:
        display = os.environ.get("DISPLAY", ":49")
        vnc_proc = start_vnc(display, args.vnc_port)
        if vnc_proc:
            novnc_proc = start_novnc(args.vnc_port, args.novnc_port)

    bg_processes = []  # (name, proc) for Xvfb/VNC — cleaned up at end

    if xvfb_proc:
        bg_processes.append(("Xvfb", xvfb_proc))
    if vnc_proc:
        bg_processes.append(("x11vnc", vnc_proc))
    if novnc_proc:
        bg_processes.append(("websockify", novnc_proc))

    processes = []

    def cleanup(signum=None, frame=None):
        print("\n  Shutting down...")
        for name, proc in processes + bg_processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(f"  Stopped {name}")
            except Exception:
                proc.kill()
                print(f"  Killed {name}")
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

    lines = [
        "",
        "  ============================================",
        "  airbrowser is running locally!",
        "",
        f"  API:       http://127.0.0.1:{args.port}",
        f"  Dashboard: http://127.0.0.1:{args.port}/dashboard",
        f"  Docs:      http://127.0.0.1:{args.port}/docs/",
    ]
    if not args.no_mcp:
        lines.append("  MCP:       http://127.0.0.1:3099")
    if vnc_proc:
        lines.append(f"  VNC:       vnc://127.0.0.1:{args.vnc_port}")
    if novnc_proc:
        lines.append(f"  noVNC:     http://127.0.0.1:{args.novnc_port}/vnc.html")
    if platform.system() != "Linux":
        lines.append("  (Chrome opens natively — no VNC needed)")
    lines.extend(
        [
            "",
            "  Press Ctrl+C to stop",
            "  ============================================",
            "",
        ]
    )
    print("\n".join(lines))

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
