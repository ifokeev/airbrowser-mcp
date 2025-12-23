"""Utility functions for browser operations."""

import logging

import psutil

logger = logging.getLogger(__name__)


def get_webdriver(driver):
    """Return the underlying Selenium WebDriver if wrapped by SeleniumBase."""
    return getattr(driver, "driver", driver)


def drain_driver_logs(driver, log_type: str):
    """
    Drain logs from the underlying driver if supported.
    Selenium get_log() is best-effort and depends on Chrome capabilities.
    """
    wd = get_webdriver(driver)
    if hasattr(wd, "get_log"):
        return wd.get_log(log_type)
    raise Exception("Driver does not support get_log(); enable browser/performance logging in the driver if needed.")


def kill_child_processes(parent_pid: int):
    """Kill all child processes of a parent process."""
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except Exception:
                pass
        # Wait for children to terminate
        psutil.wait_procs(children, timeout=3)
    except Exception:
        pass
