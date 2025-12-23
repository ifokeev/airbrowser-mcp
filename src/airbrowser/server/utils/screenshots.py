"""Screenshot utilities."""

import os
import time

SCREENSHOT_DIR = "/tmp/screenshots"
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_screenshot_url(filename: str) -> str:
    """Get public URL for a screenshot filename."""
    return f"{BASE_URL}/screenshots/{filename}"


def take_screenshot(driver, browser_id: str) -> dict:
    """Take screenshot and return path and URL."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    filename = f"{browser_id}_{int(time.time())}.png"
    path = f"{SCREENSHOT_DIR}/{filename}"
    driver.save_screenshot(path)
    return {
        "path": path,
        "filename": filename,
        "url": get_screenshot_url(filename),
    }
