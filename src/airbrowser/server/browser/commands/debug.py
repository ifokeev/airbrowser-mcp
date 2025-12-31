"""Debug and logging browser commands."""

import json
import logging
import threading
import time

from ..utils import drain_driver_logs, get_webdriver

# Use the browser_launcher logger to ensure logs appear in browser log files
logger = logging.getLogger("browser_launcher")

# Best-effort debug buffers (kept in-memory per browser process)
CONSOLE_LOG_BUFFER = []
PERFORMANCE_LOG_BUFFER = []

# CDP Network logging state
NETWORK_LOG_BUFFER = []
NETWORK_LOGGING_ENABLED = False
NETWORK_LOGGING_THREAD = None
NETWORK_LOGGING_STOP_EVENT = None


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


def _get_cdp_ws_url(driver) -> str | None:
    """Get CDP WebSocket URL for the current page (not browser level).

    Network.enable only works on page-level targets, not the browser target.
    We query /json to get the list of pages and return the first page's WebSocket URL.
    """
    import requests

    try:
        wd = get_webdriver(driver)
        caps = wd.capabilities
        debugger_address = caps.get("goog:chromeOptions", {}).get("debuggerAddress")

        if not debugger_address:
            se_cdp = caps.get("se:cdp", "")
            if se_cdp:
                debugger_address = se_cdp.replace("ws://", "").split("/devtools")[0]

        if not debugger_address:
            return None

        # Query /json to get page targets (Network.enable requires page-level, not browser-level)
        json_url = f"http://{debugger_address}/json"
        response = requests.get(json_url, timeout=5)
        response.raise_for_status()
        targets = response.json()

        # Find a page target (type="page")
        for target in targets:
            if target.get("type") == "page":
                ws_url = target.get("webSocketDebuggerUrl")
                if ws_url:
                    return ws_url

        # Fallback: return first target with a webSocketDebuggerUrl
        for target in targets:
            ws_url = target.get("webSocketDebuggerUrl")
            if ws_url:
                return ws_url

        return None
    except Exception:
        return None


def _cdp_network_listener(ws_url: str, stop_event: threading.Event):
    """Background thread that listens for CDP Network events."""
    global NETWORK_LOG_BUFFER

    import websocket

    try:
        ws = websocket.create_connection(ws_url, timeout=5)

        # Enable Network domain
        ws.send(json.dumps({"id": 1, "method": "Network.enable", "params": {}}))
        response = ws.recv()  # Consume the response

        # Check for errors in the response
        try:
            resp_data = json.loads(response)
            if "error" in resp_data:
                logger.error(f"Network.enable failed: {resp_data['error']}")
                ws.close()
                return
        except json.JSONDecodeError:
            pass

        logger.info(f"CDP Network logging started on {ws_url}")

        while not stop_event.is_set():
            try:
                ws.settimeout(0.5)
                message = ws.recv()
                if message:
                    data = json.loads(message)
                    method = data.get("method", "")
                    if method.startswith("Network."):
                        NETWORK_LOG_BUFFER.append(
                            {
                                "method": method,
                                "params": data.get("params", {}),
                                "timestamp": time.time(),
                            }
                        )
            except websocket.WebSocketTimeoutException:
                continue
            except Exception as e:
                if not stop_event.is_set():
                    logger.warning(f"CDP listener error: {e}")
                break

        ws.close()
    except Exception as e:
        logger.error(f"CDP Network listener failed: {e}")


def handle_enable_network_logging(driver, command: dict) -> dict:
    """Enable CDP Network logging to capture network events."""
    global NETWORK_LOGGING_ENABLED, NETWORK_LOGGING_THREAD, NETWORK_LOGGING_STOP_EVENT, NETWORK_LOG_BUFFER

    if NETWORK_LOGGING_ENABLED:
        return {
            "status": "success",
            "message": "Network logging already enabled",
            "events_buffered": len(NETWORK_LOG_BUFFER),
        }

    try:
        ws_url = _get_cdp_ws_url(driver)
        if not ws_url:
            return {"status": "error", "message": "Could not get CDP WebSocket URL"}

        # Clear buffer and start listener thread
        NETWORK_LOG_BUFFER = []
        NETWORK_LOGGING_STOP_EVENT = threading.Event()
        NETWORK_LOGGING_THREAD = threading.Thread(
            target=_cdp_network_listener,
            args=(ws_url, NETWORK_LOGGING_STOP_EVENT),
            daemon=True,
        )
        NETWORK_LOGGING_THREAD.start()
        NETWORK_LOGGING_ENABLED = True

        return {"status": "success", "message": "Network logging enabled"}

    except Exception as e:
        return {"status": "error", "message": f"Failed to enable network logging: {str(e)}"}


def handle_disable_network_logging(driver, command: dict) -> dict:
    """Disable CDP Network logging."""
    global NETWORK_LOGGING_ENABLED, NETWORK_LOGGING_THREAD, NETWORK_LOGGING_STOP_EVENT

    if not NETWORK_LOGGING_ENABLED:
        return {"status": "success", "message": "Network logging already disabled"}

    try:
        if NETWORK_LOGGING_STOP_EVENT:
            NETWORK_LOGGING_STOP_EVENT.set()

        if NETWORK_LOGGING_THREAD and NETWORK_LOGGING_THREAD.is_alive():
            NETWORK_LOGGING_THREAD.join(timeout=2)

        NETWORK_LOGGING_ENABLED = False
        NETWORK_LOGGING_THREAD = None
        NETWORK_LOGGING_STOP_EVENT = None

        return {"status": "success", "message": "Network logging disabled", "events_buffered": len(NETWORK_LOG_BUFFER)}

    except Exception as e:
        return {"status": "error", "message": f"Failed to disable network logging: {str(e)}"}


def handle_get_network_logs(driver, command: dict) -> dict:
    """Get buffered CDP Network events."""
    global NETWORK_LOG_BUFFER

    try:
        limit = command.get("limit", 500)
        view = NETWORK_LOG_BUFFER[-limit:] if isinstance(limit, int) and limit > 0 else NETWORK_LOG_BUFFER

        return {
            "status": "success",
            "enabled": NETWORK_LOGGING_ENABLED,
            "events": view,
            "total_events": len(NETWORK_LOG_BUFFER),
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to get network logs: {str(e)}"}


def handle_clear_network_logs(driver, command: dict) -> dict:
    """Clear buffered CDP Network events."""
    global NETWORK_LOG_BUFFER

    try:
        count = len(NETWORK_LOG_BUFFER)
        NETWORK_LOG_BUFFER = []
        return {"status": "success", "message": f"Cleared {count} network events"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear network logs: {str(e)}"}
