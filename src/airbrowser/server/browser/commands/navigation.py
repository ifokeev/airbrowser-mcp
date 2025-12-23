"""Navigation-related browser commands."""

import logging
import time

logger = logging.getLogger(__name__)


def handle_navigate(driver, command: dict) -> dict:
    """Navigate to a URL."""
    url = command.get("url")
    if not url:
        return {"status": "error", "message": "URL is required"}

    try:
        driver.uc_open(url)
        time.sleep(0.6)
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
            driver.uc_open(url)
            time.sleep(1.0)
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
    return {"status": "success", "current_url": driver.current_url}


def handle_go_forward(driver, command: dict) -> dict:
    """Navigate forward in history."""
    driver.forward()
    return {"status": "success", "current_url": driver.current_url}


def handle_refresh(driver, command: dict) -> dict:
    """Refresh the current page."""
    driver.refresh()
    return {"status": "success", "current_url": driver.current_url}
