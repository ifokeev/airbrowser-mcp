"""GUI-based click browser commands using PyAutoGUI."""

import logging
import time

logger = logging.getLogger(__name__)


def _ensure_cdp_mode(driver):
    """Ensure CDP mode is active on the driver."""
    if not hasattr(driver, "cdp"):
        try:
            current = None
            try:
                current = driver.current_url
            except Exception:
                pass
            if current and hasattr(driver, "uc_open_with_cdp_mode"):
                driver.uc_open_with_cdp_mode(current)
            elif current and hasattr(driver, "uc_activate_cdp_mode"):
                driver.uc_activate_cdp_mode(current)
        except Exception:
            pass


def _bring_window_to_front(driver):
    """Bring browser window to front via CDP if available."""
    try:
        if hasattr(driver, "cdp") and hasattr(driver.cdp, "bring_active_window_to_front"):
            driver.cdp.bring_active_window_to_front()
            time.sleep(0.05)
    except Exception:
        pass


def _gui_click_at(driver, x: float, y: float, timeframe: float = 0.25):
    """Perform GUI click at coordinates."""
    if hasattr(driver, "uc_gui_click_x_y"):
        driver.uc_gui_click_x_y(float(x), float(y), timeframe=float(timeframe))
    else:
        driver.gui_click_x_y(float(x), float(y), timeframe=float(timeframe))


def handle_gui_click_xy(driver, command: dict) -> dict:
    """Click at absolute screen coordinates using PyAutoGUI."""
    x = command.get("x")
    y = command.get("y")
    timeframe = command.get("timeframe", 0.25)

    if x is None or y is None:
        return {"status": "error", "message": "x and y coordinates are required"}

    _ensure_cdp_mode(driver)
    _bring_window_to_front(driver)

    try:
        _gui_click_at(driver, x, y, timeframe)
        return {"status": "success", "message": "Clicked at coordinates", "x": x, "y": y}
    except Exception as e:
        return {"status": "error", "message": f"Failed to click xy: {str(e)}"}


def handle_gui_click(driver, command: dict) -> dict:
    """GUI-based click on a selector using CDP to translate to screen coordinates."""
    selector = command.get("selector")
    timeframe = command.get("timeframe", 0.25)
    fx = command.get("fx")
    fy = command.get("fy")

    if not selector:
        return {"status": "error", "message": "Selector is required"}

    try:
        _ensure_cdp_mode(driver)
        _bring_window_to_front(driver)

        if hasattr(driver, "cdp") and hasattr(driver.cdp, "gui_click_element"):
            if fx is not None or fy is not None:
                # Compute element rect and click at specified fractional offset
                try:
                    rect = driver.cdp.get_gui_element_rect(selector)
                    rx = rect.get("x", 0)
                    ry = rect.get("y", 0)
                    rw = rect.get("width", 0)
                    rh = rect.get("height", 0)
                    fx_val = float(fx) if fx is not None else 0.5
                    fy_val = float(fy) if fy is not None else 0.5
                    cx = rx + rw * fx_val
                    cy = ry + rh * fy_val
                    _gui_click_at(driver, cx, cy, timeframe)
                    return {"status": "success", "message": "GUI click executed (offset)", "x": cx, "y": cy}
                except Exception as e2:
                    return {"status": "error", "message": f"GUI click offset failed: {str(e2)}"}
            else:
                rect = driver.cdp.get_gui_element_rect(selector)
                cx = rect.get("x", 0) + rect.get("width", 0) / 2
                cy = rect.get("y", 0) + rect.get("height", 0) / 2
                driver.cdp.gui_click_element(selector, timeframe=float(timeframe))
                return {"status": "success", "message": "GUI click executed", "x": cx, "y": cy}
        else:
            # Fallback path: compute screen coordinates without CDP
            return _gui_click_fallback(driver, selector, timeframe, fx, fy)

    except Exception as e:
        return {"status": "error", "message": f"GUI click failed: {str(e)}"}


def _gui_click_fallback(driver, selector: str, timeframe: float, fx, fy) -> dict:
    """Fallback GUI click when CDP is not available."""
    try:
        # Determine locator strategy
        by = "css selector"
        if isinstance(selector, str) and selector.strip().startswith("/"):
            by = "xpath"

        element = driver.find_element(by, selector)

        # Scroll element into view
        try:
            driver.execute_script(
                'arguments[0].scrollIntoView({block:"center", inline:"nearest"});',
                element,
            )
            time.sleep(0.05)
        except Exception:
            pass

        rect = element.rect or {}
        float(rect.get("width", 0))
        float(rect.get("height", 0))

        # Get window metrics
        wrect = driver.get_window_rect()
        win_x = float(wrect.get("x", 0))
        win_y = float(wrect.get("y", 0))
        win_h = float(wrect.get("height", 0))

        # Viewport metrics via JS
        viewport_h = float(driver.execute_script("return window.innerHeight;"))

        # Use viewport-relative rect for mapping to screen
        rect = driver.execute_script(
            "var r = arguments[0].getBoundingClientRect();return {x:r.left, y:r.top, width:r.width, height:r.height};",
            element,
        ) or {"x": 0, "y": 0, "width": 0, "height": 0}

        rx = float(rect.get("x", 0))
        ry = float(rect.get("y", 0))
        rw = float(rect.get("width", 0))
        rh = float(rect.get("height", 0))

        # Convert to screen-relative coordinates
        x0 = win_x + rx
        y0 = (win_y + win_h - viewport_h) + ry

        # Offset inside element
        fx_val = float(fx) if fx is not None else 0.5
        fy_val = float(fy) if fy is not None else 0.5
        cx = x0 + rw * fx_val
        cy = y0 + rh * fy_val

        # Clamp to screen bounds
        try:
            scr = driver.execute_script("return {w: window.screen.width, h: window.screen.height};") or {
                "w": 1920,
                "h": 1080,
            }
            sw = float(scr.get("w", 1920))
            sh = float(scr.get("h", 1080))
            cx = max(2, min(cx, sw - 2))
            cy = max(2, min(cy, sh - 2))
        except Exception:
            pass

        _gui_click_at(driver, cx, cy, timeframe)
        return {"status": "success", "message": "GUI click executed (fallback)", "x": cx, "y": cy}

    except Exception as ef:
        return {
            "status": "error",
            "message": f"CDP gui_click_element unavailable and fallback failed: {str(ef)}",
        }
