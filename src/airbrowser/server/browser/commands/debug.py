"""Debug and logging browser commands."""

import logging

from ..utils import drain_driver_logs

logger = logging.getLogger(__name__)

# Best-effort debug buffers (kept in-memory per browser process)
CONSOLE_LOG_BUFFER = []
PERFORMANCE_LOG_BUFFER = []


def handle_get_console_logs(driver, command: dict) -> dict:
    """Get browser console logs (best-effort)."""
    try:
        logs = drain_driver_logs(driver, "browser")
        if isinstance(logs, list):
            CONSOLE_LOG_BUFFER.extend(logs)
        limit = command.get("limit")
        view = CONSOLE_LOG_BUFFER[-limit:] if isinstance(limit, int) and limit > 0 else CONSOLE_LOG_BUFFER
        return {"status": "success", "logs": view}
    except Exception as e:
        return {"status": "error", "message": f"Console logs not available: {str(e)}"}


def handle_clear_console_logs(driver, command: dict) -> dict:
    """Clear console log buffer."""
    try:
        CONSOLE_LOG_BUFFER.clear()
        try:
            drain_driver_logs(driver, "browser")
        except Exception:
            pass
        return {"status": "success", "message": "Console log buffer cleared"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear console logs: {str(e)}"}


def handle_get_performance_logs(driver, command: dict) -> dict:
    """Get performance logs (best-effort CDP events)."""
    try:
        logs = drain_driver_logs(driver, "performance")
        if isinstance(logs, list):
            PERFORMANCE_LOG_BUFFER.extend(logs)
        limit = command.get("limit")
        view = PERFORMANCE_LOG_BUFFER[-limit:] if isinstance(limit, int) and limit > 0 else PERFORMANCE_LOG_BUFFER
        return {"status": "success", "logs": view}
    except Exception as e:
        return {"status": "error", "message": f"Performance logs not available: {str(e)}"}


def handle_clear_performance_logs(driver, command: dict) -> dict:
    """Clear performance log buffer."""
    try:
        PERFORMANCE_LOG_BUFFER.clear()
        try:
            drain_driver_logs(driver, "performance")
        except Exception:
            pass
        return {"status": "success", "message": "Performance log buffer cleared"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear performance logs: {str(e)}"}
