"""Utility functions for browser operations."""

import logging
from contextlib import contextmanager

import psutil

logger = logging.getLogger(__name__)


@contextmanager
def webdriver_connected(driver):
    """Context manager that ensures WebDriver is connected for operations that need it.

    In CDP Mode, WebDriver is disconnected for stealth. This temporarily reconnects
    it, runs the operation, then disconnects again to maintain stealth.
    If not in CDP Mode, this is a no-op.
    """
    was_disconnected = hasattr(driver, "cdp") and driver.cdp and hasattr(driver, "connect")
    if was_disconnected:
        try:
            driver.connect()
        except Exception:
            pass
    try:
        yield driver
    finally:
        if was_disconnected and hasattr(driver, "disconnect"):
            try:
                driver.disconnect()
            except Exception:
                pass


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
