"""Cookie management browser commands."""

import logging

from ..utils import get_webdriver

logger = logging.getLogger(__name__)


def handle_get_cookies(driver, command: dict) -> dict:
    """Get all cookies using CDP (includes HttpOnly cookies)."""
    try:
        wd = get_webdriver(driver)
        # Use CDP to get ALL cookies including HttpOnly
        result = wd.execute_cdp_cmd("Network.getAllCookies", {})
        cookies = result.get("cookies", [])
        return {"status": "success", "cookies": cookies}
    except Exception as e:
        # Fallback to Selenium method (doesn't include HttpOnly)
        logger.warning(f"CDP cookie fetch failed, using Selenium fallback: {e}")
        cookies = driver.get_cookies()
        return {"status": "success", "cookies": cookies, "note": "HttpOnly cookies may be missing"}


def handle_set_cookie(driver, command: dict) -> dict:
    """Set a cookie using CDP for full control."""
    cookie = command.get("cookie")
    if not cookie:
        return {"status": "error", "message": "Cookie data is required"}

    try:
        wd = get_webdriver(driver)
        # Use CDP for full cookie control (supports all attributes)
        result = wd.execute_cdp_cmd("Network.setCookie", cookie)
        if result.get("success", True):
            return {"status": "success", "message": "Cookie set successfully"}
        return {"status": "error", "message": "Failed to set cookie"}
    except Exception as e:
        # Fallback to Selenium method
        logger.warning(f"CDP cookie set failed, using Selenium fallback: {e}")
        driver.add_cookie(cookie)
        return {"status": "success", "message": "Cookie set (Selenium fallback)"}


def handle_delete_cookie(driver, command: dict) -> dict:
    """Delete a specific cookie by name and domain."""
    name = command.get("name")
    domain = command.get("domain")

    if not name:
        return {"status": "error", "message": "Cookie name is required"}

    try:
        wd = get_webdriver(driver)
        params = {"name": name}
        if domain:
            params["domain"] = domain
        wd.execute_cdp_cmd("Network.deleteCookies", params)
        return {"status": "success", "message": f"Cookie '{name}' deleted"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete cookie: {str(e)}"}


def handle_delete_cookies(driver, command: dict) -> dict:
    """Delete all cookies."""
    driver.delete_all_cookies()
    return {"status": "success", "message": "All cookies cleared"}
