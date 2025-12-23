#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from collections.abc import Iterable
from pathlib import Path


def iter_files(roots: Iterable[Path], suffixes: set[str]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                path = Path(dirpath) / filename
                if path.suffix in suffixes:
                    yield path


def max_mtime(roots: list[Path], suffixes: set[str]) -> float:
    latest = 0.0
    for path in iter_files(roots, suffixes):
        try:
            latest = max(latest, path.stat().st_mtime)
        except FileNotFoundError:
            continue
    return latest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Simple polling-based reloader for Docker dev workflows.",
        epilog="Example: dev_reloader.py --watch /app/src -- python -m airbrowser.server.api",
    )
    parser.add_argument("--watch", action="append", default=[], help="Directory to watch (repeatable).")
    parser.add_argument("--ext", action="append", default=[".py"], help="File extension to watch (repeatable).")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds.")
    parser.add_argument("--", dest="cmd_sep", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run (after --).")
    args = parser.parse_args()

    if not args.cmd:
        print("ERROR: missing command. Usage: dev_reloader.py --watch DIR -- <command...>", file=sys.stderr)
        return 2

    if args.cmd[0] == "--":
        args.cmd = args.cmd[1:]

    roots = [Path(p) for p in args.watch] if args.watch else [Path(".")]
    suffixes = {e if e.startswith(".") else f".{e}" for e in args.ext}

    current: subprocess.Popen[str] | None = None
    stopping = False

    def stop_child() -> None:
        nonlocal current
        if current is None or current.poll() is not None:
            return
        try:
            current.send_signal(signal.SIGTERM)
            current.wait(timeout=10)
        except Exception:
            try:
                current.kill()
            except Exception:
                pass
        current = None

    def handle_signal(_signum: int, _frame) -> None:  # type: ignore[override]
        nonlocal stopping
        stopping = True
        stop_child()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    last = max_mtime(roots, suffixes)

    while not stopping:
        if current is None or current.poll() is not None:
            current = subprocess.Popen(args.cmd)

        time.sleep(args.interval)
        latest = max_mtime(roots, suffixes)
        if latest > last:
            print(f"[reloader] change detected; restarting: {' '.join(args.cmd)}", flush=True)
            last = latest
            stop_child()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
