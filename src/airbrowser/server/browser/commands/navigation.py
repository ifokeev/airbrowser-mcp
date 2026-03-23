"""Navigation-related browser commands."""

import logging
import time

from ..utils import drain_driver_logs
from .debug import PERFORMANCE_LOG_BUFFER

logger = logging.getLogger(__name__)


def _get_current_url(driver) -> str:
    """Get current URL, preferring CDP path to avoid WebDriver reconnection."""
    try:
        if hasattr(driver, "cdp") and driver.cdp:
            return driver.cdp.loop.run_until_complete(driver.cdp.page.evaluate("window.location.href"))
    except Exception:
        pass
    try:
        return driver.execute_script("return window.location.href")
    except Exception:
        return driver.current_url


def _get_title(driver) -> str:
    """Get page title, preferring CDP path to avoid WebDriver reconnection."""
    try:
        if hasattr(driver, "cdp") and driver.cdp:
            return driver.cdp.loop.run_until_complete(driver.cdp.page.evaluate("document.title"))
    except Exception:
        pass
    try:
        return driver.execute_script("return document.title")
    except Exception:
        return driver.title if hasattr(driver, "title") else ""


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
        # Use CDP Mode for navigation (stealthier than UC Mode alone)
        if hasattr(driver, "uc_open_with_cdp_mode"):
            driver.uc_open_with_cdp_mode(url)
        else:
            driver.uc_open(url)
        time.sleep(0.6)
        _capture_performance_logs(driver)
        return {
            "status": "success",
            "current_url": _get_current_url(driver),
            "title": _get_title(driver),
        }
    except Exception as e:
        # Attempt recovery on tab crash by refreshing and retrying once
        try:
            driver.refresh()
            time.sleep(0.8)
            if hasattr(driver, "uc_open_with_cdp_mode"):
                driver.uc_open_with_cdp_mode(url)
            else:
                driver.uc_open(url)
            time.sleep(1.0)
            _capture_performance_logs(driver)
            return {
                "status": "success",
                "current_url": _get_current_url(driver),
                "title": _get_title(driver),
                "recovered": True,
            }
        except Exception as e2:
            return {"status": "error", "message": f"Navigate failed: {str(e2) if str(e2) else str(e)}", "crashed": True}


def handle_get_url(driver, command: dict) -> dict:
    """Get current URL."""
    try:
        current = None
        # Prefer CDP/evaluate path
        try:
            if hasattr(driver, "cdp") and driver.cdp:
                current = driver.cdp.loop.run_until_complete(driver.cdp.page.evaluate("window.location.href"))
        except Exception:
            current = None

        if not current:
            # Fallback to standard execute_script
            try:
                current = driver.execute_script("return window.location.href")
            except Exception:
                current = None

        if not current:
            # Last resort: use driver.current_url
            current = driver.current_url

        return {
            "status": "success",
            "result": current,
            "data": {"status": "success", "result": current, "request_id": str(time.time()), "timestamp": time.time()},
        }
    except Exception as e:
        # Attempt to recover from a tab crash
        try:
            driver.refresh()
            time.sleep(1)
            try:
                if hasattr(driver, "cdp") and driver.cdp:
                    current = driver.cdp.loop.run_until_complete(driver.cdp.page.evaluate("window.location.href"))
                else:
                    current = driver.execute_script("return window.location.href")
            except Exception:
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
    return {"status": "success", "current_url": _get_current_url(driver)}


def handle_go_forward(driver, command: dict) -> dict:
    """Navigate forward in history."""
    driver.forward()
    _capture_performance_logs(driver)
    return {"status": "success", "current_url": _get_current_url(driver)}


def handle_refresh(driver, command: dict) -> dict:
    """Refresh the current page."""
    driver.refresh()
    _capture_performance_logs(driver)
    return {"status": "success", "current_url": _get_current_url(driver)}
