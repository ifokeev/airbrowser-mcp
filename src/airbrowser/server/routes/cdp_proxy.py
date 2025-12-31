"""CDP WebSocket proxy - proxies CDP connections to Chrome's dynamic port."""

import logging
import threading

from flask import Blueprint, current_app
from flask_sock import Sock
from websocket import WebSocketException
from websocket import create_connection as ws_create_connection

logger = logging.getLogger(__name__)

cdp_bp = Blueprint("cdp", __name__)
sock = Sock()


def get_chrome_cdp_info(browser_id: str) -> dict | None:
    """Get the CDP connection info for a browser.

    Uses the IPC client to execute get_cdp_endpoint command.
    Returns dict with websocket_url and debugger_address.
    """
    from ..models import BrowserAction

    browser_pool = current_app.browser_pool

    # Check if browser exists
    browser = browser_pool.get_browser(browser_id)
    if not browser:
        return None

    # Execute get_cdp_endpoint via IPC
    action = BrowserAction(action="get_cdp_endpoint")
    result = browser_pool.execute_action(browser_id, action)

    if not result.success:
        logger.error(f"Failed to get CDP endpoint for {browser_id}: {result.message}")
        return None

    # Extract CDP info from response
    data = result.data.get("data", {}) if isinstance(result.data, dict) else {}
    return {
        "websocket_url": data.get("websocket_url"),
        "debugger_address": data.get("debugger_address"),
    }


@sock.route("/browser/<browser_id>/cdp")
def cdp_websocket_proxy(ws, browser_id: str):
    """WebSocket proxy handler for CDP connections.

    Proxies WebSocket messages between the external client and Chrome's CDP.
    """
    # Get the Chrome CDP info
    cdp_info = get_chrome_cdp_info(browser_id)
    if not cdp_info or not cdp_info.get("websocket_url"):
        logger.warning(f"CDP proxy: Browser {browser_id} not found or CDP not available")
        ws.close(1008, f"Browser {browser_id} not found or CDP not available")
        return

    chrome_ws_url = cdp_info["websocket_url"]
    debugger_address = cdp_info.get("debugger_address", "")

    logger.info(f"CDP proxy: Connecting browser {browser_id} to {chrome_ws_url}")

    # Connect to Chrome's CDP with correct Origin header
    # Chrome validates the Origin header - it must match the debugger address
    origin = f"http://{debugger_address}" if debugger_address else None
    try:
        chrome_ws = ws_create_connection(
            chrome_ws_url,
            timeout=30,
            origin=origin,
        )
    except Exception as e:
        logger.error(f"CDP proxy: Failed to connect to Chrome CDP: {e}")
        ws.close(1011, f"Failed to connect to Chrome: {str(e)}")
        return

    # Bidirectional proxy
    stop_event = threading.Event()
    error_holder = {"error": None}

    def forward_to_chrome():
        """Forward messages from external client to Chrome."""
        try:
            while not stop_event.is_set():
                try:
                    message = ws.receive(timeout=0.1)
                    if message is None:
                        # Client disconnected
                        break
                    chrome_ws.send(message)
                except TimeoutError:
                    continue
                except Exception as e:
                    if not stop_event.is_set():
                        error_holder["error"] = f"Client->Chrome error: {e}"
                    break
        finally:
            stop_event.set()

    def forward_to_client():
        """Forward messages from Chrome to external client."""
        try:
            while not stop_event.is_set():
                try:
                    chrome_ws.settimeout(0.1)
                    message = chrome_ws.recv()
                    if message:
                        ws.send(message)
                except TimeoutError:
                    continue
                except WebSocketException as e:
                    if not stop_event.is_set():
                        error_holder["error"] = f"Chrome->Client error: {e}"
                    break
                except Exception as e:
                    if not stop_event.is_set():
                        error_holder["error"] = f"Chrome->Client error: {e}"
                    break
        finally:
            stop_event.set()

    # Start forwarding threads
    client_thread = threading.Thread(target=forward_to_chrome, daemon=True)
    chrome_thread = threading.Thread(target=forward_to_client, daemon=True)

    client_thread.start()
    chrome_thread.start()

    # Wait for either thread to finish
    while not stop_event.is_set():
        client_thread.join(timeout=0.5)
        chrome_thread.join(timeout=0.5)
        if not client_thread.is_alive() or not chrome_thread.is_alive():
            stop_event.set()

    # Cleanup
    try:
        chrome_ws.close()
    except Exception:
        pass

    if error_holder["error"]:
        logger.warning(f"CDP proxy closed for browser {browser_id}: {error_holder['error']}")
    else:
        logger.info(f"CDP proxy closed for browser {browser_id}")


def init_cdp_proxy(app):
    """Initialize CDP proxy with the Flask app."""
    sock.init_app(app)
    app.register_blueprint(cdp_bp)
    logger.info("CDP WebSocket proxy initialized at /browser/<browser_id>/cdp")
