"""Tab management browser commands."""

import logging
import time

logger = logging.getLogger(__name__)


def handle_list_tabs(driver, command: dict) -> dict:
    """List all tabs in the browser."""
    try:
        handles = driver.window_handles
        current_handle = driver.current_window_handle
        current_index = handles.index(current_handle) if current_handle in handles else 0

        tabs = []
        for i, handle in enumerate(handles):
            # Switch to each tab to get info
            driver.switch_to.window(handle)
            tabs.append(
                {
                    "index": i,
                    "handle": handle,
                    "url": driver.current_url,
                    "title": driver.title if hasattr(driver, "title") else "",
                    "is_active": handle == current_handle,
                }
            )

        # Switch back to original tab
        driver.switch_to.window(current_handle)

        return {
            "status": "success",
            "tabs": tabs,
            "count": len(tabs),
            "current_index": current_index,
        }
    except Exception as e:
        logger.error(f"Error listing tabs: {e}")
        return {"status": "error", "message": f"Failed to list tabs: {str(e)}"}


def handle_new_tab(driver, command: dict) -> dict:
    """Open a new tab, optionally navigating to a URL."""
    url = command.get("url")

    try:
        # Open new tab using JavaScript
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(0.3)

        # Switch to the new tab (last in the list)
        handles = driver.window_handles
        new_handle = handles[-1]
        driver.switch_to.window(new_handle)

        # Navigate to URL if provided
        if url:
            driver.uc_open(url)
            time.sleep(0.5)

        return {
            "status": "success",
            "handle": new_handle,
            "index": len(handles) - 1,
            "url": driver.current_url,
            "title": driver.title if hasattr(driver, "title") else "",
        }
    except Exception as e:
        logger.error(f"Error opening new tab: {e}")
        return {"status": "error", "message": f"Failed to open new tab: {str(e)}"}


def handle_switch_tab(driver, command: dict) -> dict:
    """Switch to a specific tab by index or handle."""
    index = command.get("index")
    handle = command.get("handle")

    try:
        handles = driver.window_handles

        if handle:
            # Switch by handle
            if handle not in handles:
                return {"status": "error", "message": f"Tab handle not found: {handle}"}
            target_handle = handle
        elif index is not None:
            # Switch by index
            if index < 0 or index >= len(handles):
                return {"status": "error", "message": f"Tab index out of range: {index} (have {len(handles)} tabs)"}
            target_handle = handles[index]
        else:
            return {"status": "error", "message": "Either 'index' or 'handle' is required"}

        driver.switch_to.window(target_handle)
        time.sleep(0.2)

        return {
            "status": "success",
            "handle": target_handle,
            "index": handles.index(target_handle),
            "url": driver.current_url,
            "title": driver.title if hasattr(driver, "title") else "",
        }
    except Exception as e:
        logger.error(f"Error switching tab: {e}")
        return {"status": "error", "message": f"Failed to switch tab: {str(e)}"}


def handle_close_tab(driver, command: dict) -> dict:
    """Close a specific tab by index or handle. If no index/handle, closes current tab."""
    index = command.get("index")
    handle = command.get("handle")

    try:
        handles = driver.window_handles
        current_handle = driver.current_window_handle

        # Determine which tab to close
        if handle:
            if handle not in handles:
                return {"status": "error", "message": f"Tab handle not found: {handle}"}
            target_handle = handle
        elif index is not None:
            if index < 0 or index >= len(handles):
                return {"status": "error", "message": f"Tab index out of range: {index}"}
            target_handle = handles[index]
        else:
            # Close current tab
            target_handle = current_handle

        # Don't close the last tab
        if len(handles) <= 1:
            return {"status": "error", "message": "Cannot close the last tab"}

        # Switch to target tab if not already there
        if target_handle != current_handle:
            driver.switch_to.window(target_handle)

        # Close the tab
        driver.close()

        # Switch to another tab
        remaining_handles = driver.window_handles
        if remaining_handles:
            # Try to switch to the next tab, or previous if at the end
            target_index = handles.index(target_handle)
            new_index = min(target_index, len(remaining_handles) - 1)
            driver.switch_to.window(remaining_handles[new_index])

        return {
            "status": "success",
            "closed_handle": target_handle,
            "remaining_tabs": len(remaining_handles),
            "current_handle": driver.current_window_handle,
            "current_url": driver.current_url,
        }
    except Exception as e:
        logger.error(f"Error closing tab: {e}")
        return {"status": "error", "message": f"Failed to close tab: {str(e)}"}


def handle_get_current_tab(driver, command: dict) -> dict:
    """Get information about the current tab."""
    try:
        handles = driver.window_handles
        current_handle = driver.current_window_handle
        current_index = handles.index(current_handle) if current_handle in handles else 0

        return {
            "status": "success",
            "handle": current_handle,
            "index": current_index,
            "url": driver.current_url,
            "title": driver.title if hasattr(driver, "title") else "",
            "total_tabs": len(handles),
        }
    except Exception as e:
        logger.error(f"Error getting current tab: {e}")
        return {"status": "error", "message": f"Failed to get current tab: {str(e)}"}
