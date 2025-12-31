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


def handle_get_cdp_endpoint(driver, command: dict) -> dict:
    """Get CDP WebSocket endpoint URL for direct Chrome DevTools Protocol access."""
    import requests

    from ..utils import get_webdriver

    try:
        wd = get_webdriver(driver)
        caps = wd.capabilities

        # Get debugger address from Chrome capabilities
        debugger_address = caps.get("goog:chromeOptions", {}).get("debuggerAddress")

        if not debugger_address:
            # Try alternate: extract from se:cdp capability
            se_cdp = caps.get("se:cdp", "")
            if se_cdp:
                # Format: ws://127.0.0.1:PORT/devtools/...
                debugger_address = se_cdp.replace("ws://", "").split("/devtools")[0]

        if not debugger_address:
            return {
                "status": "error",
                "message": "Could not determine CDP debugger address from browser capabilities",
            }

        # Query Chrome's /json/version endpoint to get WebSocket URL
        json_url = f"http://{debugger_address}/json/version"
        response = requests.get(json_url, timeout=5)
        response.raise_for_status()
        version_info = response.json()

        ws_url = version_info.get("webSocketDebuggerUrl")
        if not ws_url:
            return {
                "status": "error",
                "message": "webSocketDebuggerUrl not found in Chrome /json/version response",
            }

        return {
            "status": "success",
            "data": {
                "websocket_url": ws_url,
                "debugger_address": debugger_address,
                "browser_version": version_info.get("Browser"),
                "protocol_version": version_info.get("Protocol-Version"),
                "v8_version": version_info.get("V8-Version"),
                "webkit_version": version_info.get("WebKit-Version"),
            },
        }

    except requests.RequestException as e:
        return {"status": "error", "message": f"Failed to query CDP endpoint: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get CDP endpoint: {str(e)}"}
