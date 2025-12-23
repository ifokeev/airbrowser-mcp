"""Page content browser commands."""

import logging

from airbrowser.server.utils.screenshots import take_screenshot

logger = logging.getLogger(__name__)


def handle_screenshot(driver, command: dict, browser_id: str = "unknown") -> dict:
    """Take a screenshot of the browser."""
    screenshot = take_screenshot(driver, browser_id)
    return {
        "status": "success",
        "filename": screenshot["filename"],
        "path": screenshot["path"],
        "url": screenshot["url"],
    }


def handle_get_content(driver, command: dict) -> dict:
    """Get page HTML content."""
    return {
        "status": "success",
        "content": driver.page_source,
        "url": driver.current_url,
        "title": driver.title if hasattr(driver, "title") else "",
    }


def handle_execute_script(driver, command: dict) -> dict:
    """Execute JavaScript in the browser."""
    script = command.get("script")
    if not script:
        return {"status": "error", "message": "Script is required"}

    result = driver.execute_script(script)
    return {"status": "success", "result": result}


def handle_resize(driver, command: dict) -> dict:
    """Resize the browser viewport."""
    width = command.get("width")
    height = command.get("height")

    if not width or not height:
        return {"status": "error", "message": "Width and height are required"}

    try:
        driver.set_window_size(width, height)
        actual_size = driver.get_window_size()
        return {
            "status": "success",
            "width": actual_size["width"],
            "height": actual_size["height"],
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to resize: {str(e)}"}


def handle_snapshot(driver, command: dict) -> dict:
    """Take a DOM or accessibility tree snapshot.

    Args:
        command: {
            "type": "dom" | "accessibility" (default: "dom")
        }
    """
    snapshot_type = command.get("type", "dom")

    try:
        if snapshot_type == "accessibility":
            # Get accessibility tree via CDP
            result = driver.execute_cdp_cmd("Accessibility.getFullAXTree", {})
            return {
                "status": "success",
                "type": "accessibility",
                "nodes": result.get("nodes", []),
            }
        else:
            # DOM snapshot via CDP
            result = driver.execute_cdp_cmd(
                "DOMSnapshot.captureSnapshot",
                {"computedStyles": [], "includeDOMRects": True},
            )
            return {
                "status": "success",
                "type": "dom",
                "documents": result.get("documents", []),
                "strings": result.get("strings", []),
            }
    except Exception as e:
        # Fallback to simple HTML if CDP not available
        return {
            "status": "success",
            "type": "html_fallback",
            "content": driver.page_source,
            "warning": f"CDP snapshot failed, using HTML fallback: {str(e)}",
        }
