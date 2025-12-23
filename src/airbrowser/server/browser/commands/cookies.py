"""Cookie management browser commands."""

import logging

logger = logging.getLogger(__name__)


def handle_get_cookies(driver, command: dict) -> dict:
    """Get all cookies."""
    cookies = driver.get_cookies()
    return {"status": "success", "cookies": cookies}


def handle_set_cookie(driver, command: dict) -> dict:
    """Set a cookie."""
    cookie = command.get("cookie")
    if not cookie:
        return {"status": "error", "message": "Cookie data is required"}

    driver.add_cookie(cookie)
    return {"status": "success"}


def handle_delete_cookies(driver, command: dict) -> dict:
    """Delete all cookies."""
    driver.delete_all_cookies()
    return {"status": "success"}
