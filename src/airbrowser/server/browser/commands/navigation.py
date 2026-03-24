"""Navigation-related browser commands."""

import logging
import time

from ..utils import drain_driver_logs
from .debug import PERFORMANCE_LOG_BUFFER

logger = logging.getLogger(__name__)


def _capture_performance_logs(driver):
    """Capture performance logs into buffer after navigation/actions."""
    try:
        logs = drain_driver_logs(driver, "performance")
        if isinstance(logs, list) and logs:
            PERFORMANCE_LOG_BUFFER.extend(logs)
            logger.info(f"Captured {len(logs)} performance log entries (buffer now has {len(PERFORMANCE_LOG_BUFFER)})")
        else:
            logger.debug("No performance logs available to capture")
    except Exception as e:
        logger.warning(f"Failed to capture performance logs: {e}")


def handle_navigate(driver, command: dict) -> dict:
    """Navigate to a URL."""
    url = command.get("url")
    if not url:
        return {"status": "error", "message": "URL is required"}

    try:
        # UC reconnect mode — stealthy and compatible with hCaptcha
        driver.uc_open_with_reconnect(url, reconnect_time=4)
        time.sleep(0.6)
        _capture_performance_logs(driver)
        return {
            "status": "success",
            "current_url": driver.current_url,
            "title": driver.title if hasattr(driver, "title") else "",
        }
    except Exception as e:
        # Attempt recovery on tab crash by refreshing and retrying once
        try:
            driver.refresh()
            time.sleep(0.8)
            driver.uc_open_with_reconnect(url, reconnect_time=4)
            time.sleep(1.0)
            _capture_performance_logs(driver)
            return {
                "status": "success",
                "current_url": driver.current_url,
                "title": driver.title if hasattr(driver, "title") else "",
                "recovered": True,
            }
        except Exception as e2:
            return {"status": "error", "message": f"Navigate failed: {str(e2) if str(e2) else str(e)}", "crashed": True}


def handle_get_url(driver, command: dict) -> dict:
    """Get current URL."""
    try:
        return {
            "status": "success",
            "result": driver.current_url,
            "data": {
                "status": "success",
                "result": driver.current_url,
                "request_id": str(time.time()),
                "timestamp": time.time(),
            },
        }
    except Exception as e:
        try:
            driver.refresh()
            time.sleep(1)
            current = driver.current_url
            return {
                "status": "success",
                "result": current,
                "data": {
                    "status": "success",
                    "result": current,
                    "request_id": str(time.time()),
                    "timestamp": time.time(),
                },
                "recovered": True,
            }
        except Exception as e2:
            return {
                "status": "error",
                "message": f"Failed to get URL: {str(e2) if str(e2) else str(e)}",
                "crashed": True,
            }


def handle_go_back(driver, command: dict) -> dict:
    """Navigate back in history."""
    driver.back()
    _capture_performance_logs(driver)
    return {"status": "success", "current_url": driver.current_url}


def handle_go_forward(driver, command: dict) -> dict:
    """Navigate forward in history."""
    driver.forward()
    _capture_performance_logs(driver)
    return {"status": "success", "current_url": driver.current_url}


def handle_refresh(driver, command: dict) -> dict:
    """Refresh the current page."""
    driver.refresh()
    _capture_performance_logs(driver)
    return {"status": "success", "current_url": driver.current_url}
