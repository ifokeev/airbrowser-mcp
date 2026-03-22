"""GUI-based browser commands using PyAutoGUI."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any

from selenium.webdriver.common.action_chains import ActionChains

from ..postclick_feedback import capture_postclick_snapshot, diff_postclick_snapshot
from ..smart_targeting import (
    HitTestResult,
    Point,
    Rect,
    get_window_metrics,
    hit_test_point,
    resolve_click_target,
    viewport_to_screen_point,
)
from ..utils import get_webdriver
from .elements import KEY_MAP

logger = logging.getLogger(__name__)

CLICK_CONFIRMED_POSTCHECK_STATUSES = {
    "url_changed",
    "content_changed",
    "focus_changed",
    "visible_state_changed",
}
CLICK_UNAVAILABLE_POSTCHECK_STATUSES = {"postcheck_unavailable"}
CLICK_SUCCESS_STATUSES = {"clicked_raw", "clicked_exact", "clicked_snapped"}
SELECTOR_TARGET_SCRIPT = r"""
const selector = arguments[0];
const fx = arguments[1];
const fy = arguments[2];
const elementPath = (node) => {
  const parts = [];
  for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; current = current.parentElement) {
    let index = 0;
    for (let sibling = current; (sibling = sibling.previousElementSibling); ) {
      index += 1;
    }
    parts.push(`${current.tagName}[${index}]`);
  }
  return parts.reverse().join('>');
};
const resolveSelector = (value) => {
  if (typeof value !== 'string') {
    return null;
  }
  const trimmed = value.trim();
  if (!trimmed) {
    return null;
  }
  if (trimmed.startsWith('/')) {
    return document.evaluate(trimmed, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  }
  return document.querySelector(trimmed);
};
const el = resolveSelector(selector);
if (!el) {
  return {found: false};
}
try {
  el.scrollIntoView({block: 'center', inline: 'nearest'});
} catch (error) {
  // Ignore scroll failures and use the current rect.
}
const rect = el.getBoundingClientRect();
return {
  found: true,
  tag: (el.tagName || '').toUpperCase(),
  text: (el.innerText || el.textContent || '').trim().slice(0, 200),
  element_path: elementPath(el),
  viewport_rect: {x: rect.left, y: rect.top, width: rect.width, height: rect.height},
  viewport_point: {x: rect.left + rect.width * fx, y: rect.top + rect.height * fy},
};
"""


@dataclass(frozen=True)
class ClickPlan:
    success: bool
    outcome_status: str
    reason: str | None
    reason_detail: str | None
    recommended_next_action: str
    raw_screen_point: Point | None
    raw_viewport_point: Point | None
    resolved_screen_point: Point | None
    resolved_viewport_point: Point | None
    resolved_element_path: str | None = None
    resolved_element: dict[str, Any] | None = None
    hit_test_result: HitTestResult | None = None
    snap_candidate: Any | None = None


@dataclass(frozen=True)
class SelectorTarget:
    tag: str
    text: str | None
    rect: Rect
    viewport_point: Point
    screen_point: Point
    element_path: str | None


class PageScriptUnavailable(RuntimeError):
    """Raised when GUI click pre/post-check scripts cannot run."""


class _ScriptDriverProxy:
    def __init__(self, driver: Any):
        self._driver = driver

    def get_window_rect(self) -> dict[str, Any]:
        return self._driver.get_window_rect()

    def execute_script(self, script: str, *args: Any) -> Any:
        try:
            return self._driver.execute_script(script, *args)
        except Exception as exc:
            return _execute_script_via_cdp(self._driver, script, args, fallback_error=exc)


def _clipboard_type(text: str):
    """Type text using clipboard (paste) - supports Unicode/Cyrillic.

    PyAutoGUI's write() only supports ASCII characters. For Unicode text,
    we copy to clipboard using xclip and paste with Ctrl+V.
    """
    import subprocess

    import pyautogui

    # Copy to clipboard using xclip (available in Docker container)
    proc = subprocess.Popen(
        ["xclip", "-selection", "clipboard"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    proc.communicate(input=text.encode("utf-8"))

    # Small delay to ensure clipboard is ready
    time.sleep(0.05)

    # Paste with Ctrl+V
    pyautogui.hotkey("ctrl", "v")


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
            time.sleep(0.15)
    except Exception:
        pass


def _gui_click_at(driver, x: float, y: float, timeframe: float = 0.25):
    """Perform GUI click at coordinates."""
    if hasattr(driver, "uc_gui_click_x_y"):
        driver.uc_gui_click_x_y(float(x), float(y), timeframe=float(timeframe))
    else:
        driver.gui_click_x_y(float(x), float(y), timeframe=float(timeframe))


def _execute_script_via_cdp(
    driver: Any,
    script: str,
    args: tuple[Any, ...],
    *,
    fallback_error: Exception | None = None,
) -> Any:
    wd = get_webdriver(driver)
    if not hasattr(wd, "execute_cdp_cmd"):
        raise PageScriptUnavailable(str(fallback_error or "CDP evaluation unavailable"))

    expression = f"""
(() => {{
  const __args = {json.dumps(list(args))};
  return (function() {{
{script}
  }}).apply(window, __args);
}})()
"""
    try:
        result = wd.execute_cdp_cmd(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
        )
    except Exception as exc:  # pragma: no cover - browser-only fallback path
        raise PageScriptUnavailable(str(exc)) from exc

    if result.get("exceptionDetails"):
        detail = result["exceptionDetails"].get("text") or "CDP evaluation failed"
        raise PageScriptUnavailable(detail)

    payload = result.get("result", {})
    if "value" in payload:
        return payload["value"]
    if payload.get("subtype") == "null":
        return None
    raise PageScriptUnavailable("CDP evaluation did not return a serializable value")


def _point_to_payload(point: Point | None) -> dict[str, float] | None:
    if point is None:
        return None
    return {"x": point.x, "y": point.y}


def _hit_test_element_payload(hit_test_result: HitTestResult | None) -> dict[str, Any] | None:
    if hit_test_result is None:
        return None
    return {
        "tag": hit_test_result.tag,
        "text": hit_test_result.text,
        "interactive": hit_test_result.interactive,
    }


def _selector_element_payload(target: SelectorTarget | None) -> dict[str, Any] | None:
    if target is None:
        return None
    return {"tag": target.tag, "text": target.text, "interactive": True}


def _precheck_outcome_status(outcome_status: str) -> str:
    return {
        "clicked_exact": "exact_match",
        "clicked_snapped": "snapped_match",
        "clicked_raw": "clicked_raw",
    }.get(outcome_status, outcome_status)


def _execution_mode(outcome_status: str) -> str:
    return {
        "clicked_snapped": "snapped",
        "clicked_exact": "exact",
    }.get(outcome_status, "raw")


def _build_click_message(outcome_status: str, postcheck_status: str | None, reason_detail: str | None) -> str:
    if outcome_status == "click_failed_precheck":
        return reason_detail or "Click precheck failed"
    if outcome_status == "click_failed_execution":
        return reason_detail or "Click execution failed"
    if outcome_status == "click_failed_postcheck":
        return reason_detail or "Post-click feedback failed"
    if outcome_status == "click_uncertain":
        return reason_detail or "Click executed but outcome could not be confirmed"

    base = {
        "clicked_snapped": "Clicked snapped target",
        "clicked_exact": "Clicked validated target",
        "clicked_raw": "Clicked requested target",
    }.get(outcome_status, "GUI click executed")
    if postcheck_status in CLICK_CONFIRMED_POSTCHECK_STATUSES:
        return f"{base} and detected {postcheck_status.replace('_', ' ')}"
    return base


def _build_debug_payload(mode: str, plan: ClickPlan) -> dict[str, Any]:
    debug = {
        "mode": mode,
        "raw_screen_point": _point_to_payload(plan.raw_screen_point),
        "raw_viewport_point": _point_to_payload(plan.raw_viewport_point),
        "resolved_screen_point": _point_to_payload(plan.resolved_screen_point),
        "resolved_viewport_point": _point_to_payload(plan.resolved_viewport_point),
    }
    if plan.hit_test_result is not None:
        debug["hit_test_result"] = {
            "viewport_point": _point_to_payload(plan.hit_test_result.viewport_point),
            "element": _hit_test_element_payload(plan.hit_test_result),
            "reason": plan.hit_test_result.reason,
            "reason_detail": plan.hit_test_result.reason_detail,
        }
    if plan.snap_candidate is not None:
        debug["snap_candidate"] = {
            "tag": plan.snap_candidate.tag,
            "text": plan.snap_candidate.text,
            "element_path": plan.snap_candidate.element_path,
            "point": _point_to_payload(plan.resolved_screen_point),
        }
    return debug


def _build_precheck_payload(plan: ClickPlan, attempted: bool) -> dict[str, Any] | None:
    if not attempted:
        return None
    payload = {
        "outcome_status": _precheck_outcome_status(plan.outcome_status),
        "original_point": _point_to_payload(plan.raw_screen_point),
        "resolved_point": _point_to_payload(plan.resolved_screen_point),
        "resolved_element": plan.resolved_element,
    }
    if plan.reason is not None:
        payload["reason"] = plan.reason
    if plan.reason_detail is not None:
        payload["reason_detail"] = plan.reason_detail
    return payload


def _build_response(
    *,
    command: dict[str, Any],
    mode: str,
    plan: ClickPlan,
    success: bool,
    outcome_status: str,
    execution: dict[str, Any] | None,
    postcheck: dict[str, Any] | None,
    precheck_attempted: bool,
    include_debug: bool,
    reason_detail: str | None = None,
    recommended_next_action: str | None = None,
) -> dict[str, Any]:
    raw_x = command.get("x") if mode == "coordinate" else None
    raw_y = command.get("y") if mode == "coordinate" else None
    resolved_point = plan.raw_screen_point if plan.raw_screen_point is not None else plan.resolved_screen_point
    data = {
        "status": "success",
        "success": success,
        "message": _build_click_message(
            outcome_status, postcheck.get("status") if postcheck else None, reason_detail or plan.reason_detail
        ),
        "x": raw_x if raw_x is not None else (resolved_point.x if resolved_point is not None else None),
        "y": raw_y if raw_y is not None else (resolved_point.y if resolved_point is not None else None),
        "outcome_status": outcome_status,
        "precheck": _build_precheck_payload(plan, precheck_attempted),
        "execution": execution,
        "postcheck": postcheck,
        "recommended_next_action": recommended_next_action or plan.recommended_next_action,
    }
    if plan.reason is not None:
        data["reason"] = plan.reason
    if reason_detail or plan.reason_detail:
        data["reason_detail"] = reason_detail or plan.reason_detail
    if include_debug:
        data["debug"] = _build_debug_payload(mode, plan)
    return data


def _selector_hit_matches(target: SelectorTarget, hit_test_result: HitTestResult) -> bool:
    hit_path = hit_test_result.element_path
    target_path = target.element_path
    if not target_path or not hit_path:
        return False
    return hit_path == target_path or hit_path.startswith(f"{target_path}>")


def _resolve_selector_target(
    script_driver: _ScriptDriverProxy, selector: str, fx: float | None, fy: float | None
) -> SelectorTarget:
    fx_value = max(0.0, min(1.0, float(fx) if fx is not None else 0.5))
    fy_value = max(0.0, min(1.0, float(fy) if fy is not None else 0.5))
    payload = script_driver.execute_script(SELECTOR_TARGET_SCRIPT, selector, fx_value, fy_value) or {}
    if not payload.get("found"):
        raise PageScriptUnavailable("selector could not be resolved")

    viewport_rect = Rect.from_mapping(payload.get("viewport_rect"))
    viewport_point_payload = payload.get("viewport_point") or {}
    if viewport_rect is None or "x" not in viewport_point_payload or "y" not in viewport_point_payload:
        raise PageScriptUnavailable("selector geometry was unavailable")

    viewport_point = Point(float(viewport_point_payload["x"]), float(viewport_point_payload["y"]))
    metrics = get_window_metrics(script_driver)
    screen_point = viewport_to_screen_point(metrics, viewport_point)
    return SelectorTarget(
        tag=(payload.get("tag") or "").upper(),
        text=payload.get("text"),
        rect=viewport_rect,
        viewport_point=viewport_point,
        screen_point=screen_point,
        element_path=payload.get("element_path"),
    )


def _selector_screen_point_from_cdp(driver: Any, selector: str, fx: float | None, fy: float | None) -> Point | None:
    _ensure_cdp_mode(driver)
    if not hasattr(driver, "cdp") or not hasattr(driver.cdp, "get_gui_element_rect"):
        return None
    rect = driver.cdp.get_gui_element_rect(selector)
    if not rect:
        return None
    fx_value = max(0.0, min(1.0, float(fx) if fx is not None else 0.5))
    fy_value = max(0.0, min(1.0, float(fy) if fy is not None else 0.5))
    return Point(
        float(rect.get("x", 0.0)) + float(rect.get("width", 0.0)) * fx_value,
        float(rect.get("y", 0.0)) + float(rect.get("height", 0.0)) * fy_value,
    )


def _selector_click_plan(
    target: SelectorTarget, hit_test_result: HitTestResult | None, pre_click_validate: str
) -> ClickPlan:
    resolved_element = _selector_element_payload(target)
    if hit_test_result is not None and _selector_hit_matches(target, hit_test_result):
        return ClickPlan(
            success=True,
            outcome_status="clicked_exact",
            reason="hit_interactive_element",
            reason_detail=hit_test_result.reason_detail,
            recommended_next_action="proceed",
            raw_screen_point=target.screen_point,
            raw_viewport_point=target.viewport_point,
            resolved_screen_point=target.screen_point,
            resolved_viewport_point=target.viewport_point,
            resolved_element_path=target.element_path,
            resolved_element=resolved_element,
            hit_test_result=hit_test_result,
        )

    reason = "intent_mismatch"
    reason_detail = (
        hit_test_result.reason_detail
        if hit_test_result is not None
        else "selector-derived point could not be validated"
    )
    if hit_test_result is not None and hit_test_result.reason != "hit_interactive_element":
        reason = hit_test_result.reason
    if pre_click_validate == "strict":
        return ClickPlan(
            success=False,
            outcome_status="click_failed_precheck",
            reason=reason,
            reason_detail=reason_detail,
            recommended_next_action="inspect_page",
            raw_screen_point=target.screen_point,
            raw_viewport_point=target.viewport_point,
            resolved_screen_point=target.screen_point,
            resolved_viewport_point=target.viewport_point,
            resolved_element_path=target.element_path,
            resolved_element=resolved_element,
            hit_test_result=hit_test_result,
        )

    return ClickPlan(
        success=True,
        outcome_status="clicked_raw",
        reason=reason,
        reason_detail=reason_detail,
        recommended_next_action="inspect_page",
        raw_screen_point=target.screen_point,
        raw_viewport_point=target.viewport_point,
        resolved_screen_point=target.screen_point,
        resolved_viewport_point=target.viewport_point,
        resolved_element_path=target.element_path,
        resolved_element=resolved_element,
        hit_test_result=hit_test_result,
    )


def _unavailable_selector_plan(
    raw_point: Point | None,
    reason_detail: str,
    pre_click_validate: str,
) -> ClickPlan:
    success = pre_click_validate != "strict"
    return ClickPlan(
        success=success,
        outcome_status="clicked_raw" if success else "click_failed_precheck",
        reason="hit_test_unavailable",
        reason_detail=reason_detail,
        recommended_next_action="inspect_page",
        raw_screen_point=raw_point,
        raw_viewport_point=None,
        resolved_screen_point=raw_point,
        resolved_viewport_point=None,
    )


def _plan_from_resolution(resolution: Any) -> ClickPlan:
    resolved_element = None
    resolved_element_path = None
    if resolution.snap_candidate is not None:
        resolved_element = {
            "tag": resolution.snap_candidate.tag,
            "text": resolution.snap_candidate.text,
            "interactive": True,
        }
        resolved_element_path = resolution.snap_candidate.element_path
    elif resolution.hit_test_result is not None:
        resolved_element = _hit_test_element_payload(resolution.hit_test_result)
        resolved_element_path = resolution.hit_test_result.element_path

    return ClickPlan(
        success=resolution.success,
        outcome_status=resolution.outcome_status,
        reason=resolution.reason,
        reason_detail=resolution.reason_detail,
        recommended_next_action=resolution.recommended_next_action,
        raw_screen_point=resolution.original_screen_point,
        raw_viewport_point=resolution.original_viewport_point,
        resolved_screen_point=resolution.resolved_screen_point or resolution.original_screen_point,
        resolved_viewport_point=resolution.resolved_viewport_point or resolution.original_viewport_point,
        resolved_element_path=resolved_element_path,
        resolved_element=resolved_element,
        hit_test_result=resolution.hit_test_result,
        snap_candidate=resolution.snap_candidate,
    )


def handle_gui_click_xy(driver, command: dict) -> dict:
    """Click at absolute screen coordinates using the smart GUI click pipeline."""
    return handle_gui_click(driver, command)


def handle_gui_type_xy(driver, command: dict) -> dict:
    """Click at coordinates then type text using proper focus and browser events."""
    x = command.get("x")
    y = command.get("y")
    text = command.get("text")
    timeframe = command.get("timeframe", 0.25)

    if x is None or y is None:
        return {"status": "error", "message": "x and y coordinates are required"}
    if not text:
        return {"status": "error", "message": "text is required"}

    _ensure_cdp_mode(driver)
    _bring_window_to_front(driver)

    try:
        _gui_click_at(driver, x, y, timeframe)
        time.sleep(0.2)

        try:
            focused = driver.execute_script("return document.activeElement;")
            if focused:
                tag = focused.tag_name.lower() if hasattr(focused, "tag_name") else ""
                is_editable = (
                    focused.get_attribute("contenteditable") == "true" if hasattr(focused, "get_attribute") else False
                )
                if tag in ("input", "textarea") or is_editable:
                    try:
                        focused.clear()
                    except Exception:
                        pass
                    focused.send_keys(text)
                    logger.debug(f"gui_type_xy: used send_keys on {tag} element")
                    return {
                        "status": "success",
                        "message": "Typed at coordinates",
                        "x": x,
                        "y": y,
                        "text_length": len(text),
                        "method": "send_keys",
                    }
        except Exception as e:
            logger.debug(f"gui_type_xy: send_keys failed, falling back to pyautogui: {e}")

        if hasattr(driver, "uc_gui_write"):
            driver.uc_gui_write(text)
        elif hasattr(driver, "cdp") and hasattr(driver.cdp, "gui_write"):
            driver.cdp.gui_write(text)
        else:
            # Use clipboard-based typing for Unicode support
            # (pyautogui.write() only supports ASCII characters)
            _clipboard_type(text)

        return {
            "status": "success",
            "message": "Typed at coordinates",
            "x": x,
            "y": y,
            "text_length": len(text),
            "method": "clipboard",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to type at xy: {str(e)}"}


def handle_gui_hover_xy(driver, command: dict) -> dict:
    """Hover at absolute screen coordinates using PyAutoGUI."""
    x = command.get("x")
    y = command.get("y")
    timeframe = command.get("timeframe", 0.25)

    if x is None or y is None:
        return {"status": "error", "message": "x and y coordinates are required"}

    _ensure_cdp_mode(driver)
    _bring_window_to_front(driver)

    try:
        if hasattr(driver, "cdp") and hasattr(driver.cdp, "gui_hover_x_y"):
            driver.cdp.gui_hover_x_y(float(x), float(y), timeframe=float(timeframe))
        else:
            import pyautogui

            pyautogui.moveTo(float(x), float(y), float(timeframe))

        return {"status": "success", "message": "Hovered at coordinates", "x": x, "y": y}
    except Exception as e:
        return {"status": "error", "message": f"Failed to hover at xy: {str(e)}"}


def handle_gui_click(driver, command: dict) -> dict:
    """GUI click by selector or coordinates with validation and post-click feedback."""
    selector = command.get("selector")
    x = command.get("x")
    y = command.get("y")
    timeframe = float(command.get("timeframe", 0.25))
    fx = command.get("fx")
    fy = command.get("fy")
    pre_click_validate = command.get("pre_click_validate", "off") or "off"
    auto_snap = command.get("auto_snap", "off") or "off"
    snap_radius = float(command.get("snap_radius", 96))
    post_click_feedback = command.get("post_click_feedback", "none") or "none"
    post_click_timeout_ms = int(command.get("post_click_timeout_ms", 1500))
    return_content = bool(command.get("return_content", False))
    content_limit_chars = int(command.get("content_limit_chars", 4000))
    include_debug = bool(command.get("include_debug", False))

    selector_mode = selector is not None
    coordinate_mode = x is not None or y is not None
    if selector_mode and coordinate_mode:
        return {"status": "error", "message": "Selector mode cannot be combined with x/y coordinates"}
    if not selector_mode and not coordinate_mode:
        return {"status": "error", "message": "Either selector or both x and y coordinates are required"}
    if coordinate_mode and (x is None or y is None):
        return {"status": "error", "message": "Both x and y coordinates are required"}

    x_value = float(x) if x is not None else None
    y_value = float(y) if y is not None else None

    script_driver = _ScriptDriverProxy(driver)
    mode = "selector" if selector_mode else "coordinate"
    precheck_attempted = (selector_mode and pre_click_validate != "off") or (
        not selector_mode and (pre_click_validate != "off" or auto_snap != "off")
    )

    target_element_path = None
    if selector_mode:
        selector_target = None
        try:
            selector_target = _resolve_selector_target(script_driver, selector, fx, fy)
            target_element_path = selector_target.element_path
            if pre_click_validate == "off":
                plan = ClickPlan(
                    success=True,
                    outcome_status="clicked_raw",
                    reason=None,
                    reason_detail=None,
                    recommended_next_action="proceed",
                    raw_screen_point=selector_target.screen_point,
                    raw_viewport_point=selector_target.viewport_point,
                    resolved_screen_point=selector_target.screen_point,
                    resolved_viewport_point=selector_target.viewport_point,
                    resolved_element_path=selector_target.element_path,
                    resolved_element=_selector_element_payload(selector_target),
                )
            else:
                hit_test_result = hit_test_point(script_driver, selector_target.viewport_point)
                plan = _selector_click_plan(selector_target, hit_test_result, pre_click_validate)
                target_element_path = plan.resolved_element_path or target_element_path
        except Exception as exc:
            raw_point = _selector_screen_point_from_cdp(driver, selector, fx, fy)
            plan = _unavailable_selector_plan(raw_point, str(exc), pre_click_validate)
    else:
        assert x_value is not None and y_value is not None
        resolution = resolve_click_target(
            driver=script_driver,
            raw_point=Point(x_value, y_value),
            pre_click_validate=pre_click_validate,
            auto_snap=auto_snap,
            snap_radius=snap_radius,
        )
        plan = _plan_from_resolution(resolution)
        target_element_path = plan.resolved_element_path

    before_snapshot = None
    postcheck_issue = None
    if post_click_feedback != "none":
        try:
            before_snapshot = capture_postclick_snapshot(
                script_driver,
                post_click_feedback,
                content_limit_chars,
                return_content=return_content,
                target_element_path=target_element_path,
            )
        except Exception as exc:
            postcheck_issue = str(exc)

    if not plan.success:
        return _build_response(
            command=command,
            mode=mode,
            plan=plan,
            success=False,
            outcome_status=plan.outcome_status,
            execution=None,
            postcheck=None,
            precheck_attempted=precheck_attempted,
            include_debug=include_debug,
            recommended_next_action=plan.recommended_next_action,
        )

    clicked_point = plan.resolved_screen_point or plan.raw_screen_point
    if clicked_point is None:
        failed_plan = ClickPlan(
            success=False,
            outcome_status="click_failed_precheck",
            reason="hit_test_unavailable",
            reason_detail="click target could not be resolved",
            recommended_next_action="inspect_page",
            raw_screen_point=plan.raw_screen_point,
            raw_viewport_point=plan.raw_viewport_point,
            resolved_screen_point=plan.resolved_screen_point,
            resolved_viewport_point=plan.resolved_viewport_point,
            resolved_element_path=plan.resolved_element_path,
            resolved_element=plan.resolved_element,
            hit_test_result=plan.hit_test_result,
            snap_candidate=plan.snap_candidate,
        )
        return _build_response(
            command=command,
            mode=mode,
            plan=failed_plan,
            success=False,
            outcome_status="click_failed_precheck",
            execution=None,
            postcheck=None,
            precheck_attempted=precheck_attempted,
            include_debug=include_debug,
            recommended_next_action=failed_plan.recommended_next_action,
        )

    _ensure_cdp_mode(driver)
    _bring_window_to_front(driver)

    try:
        _gui_click_at(driver, clicked_point.x, clicked_point.y, timeframe)
    except Exception as exc:
        execution = {
            "clicked_point": _point_to_payload(clicked_point),
            "mode": _execution_mode(plan.outcome_status),
            "error": str(exc),
        }
        return _build_response(
            command=command,
            mode=mode,
            plan=plan,
            success=False,
            outcome_status="click_failed_execution",
            execution=execution,
            postcheck=None,
            precheck_attempted=precheck_attempted,
            include_debug=include_debug,
            reason_detail=str(exc),
            recommended_next_action="inspect_page",
        )

    execution = {
        "clicked_point": _point_to_payload(clicked_point),
        "mode": _execution_mode(plan.outcome_status),
    }

    postcheck_payload = None
    if post_click_feedback != "none":
        if post_click_timeout_ms > 0:
            time.sleep(post_click_timeout_ms / 1000.0)
        if postcheck_issue is None and before_snapshot is not None:
            try:
                after_snapshot = capture_postclick_snapshot(
                    script_driver,
                    post_click_feedback,
                    content_limit_chars,
                    return_content=return_content,
                    target_element_path=target_element_path,
                )
                postcheck_payload = asdict(
                    diff_postclick_snapshot(before_snapshot, after_snapshot, post_click_feedback)
                )
            except Exception as exc:
                postcheck_issue = str(exc)
        if postcheck_payload is None:
            postcheck_payload = {"status": "postcheck_unavailable", "reason_detail": postcheck_issue}

    if postcheck_payload and postcheck_payload.get("status") in CLICK_UNAVAILABLE_POSTCHECK_STATUSES:
        return _build_response(
            command=command,
            mode=mode,
            plan=plan,
            success=False,
            outcome_status="click_failed_postcheck",
            execution=execution,
            postcheck=postcheck_payload,
            precheck_attempted=precheck_attempted,
            include_debug=include_debug,
            reason_detail=postcheck_payload.get("reason_detail"),
            recommended_next_action="inspect_page",
        )

    if postcheck_payload and postcheck_payload.get("status") not in CLICK_CONFIRMED_POSTCHECK_STATUSES:
        return _build_response(
            command=command,
            mode=mode,
            plan=plan,
            success=False,
            outcome_status="click_uncertain",
            execution=execution,
            postcheck=postcheck_payload,
            precheck_attempted=precheck_attempted,
            include_debug=include_debug,
            reason_detail=postcheck_payload.get("reason_detail"),
            recommended_next_action="inspect_page",
        )

    return _build_response(
        command=command,
        mode=mode,
        plan=plan,
        success=plan.outcome_status in CLICK_SUCCESS_STATUSES,
        outcome_status=plan.outcome_status,
        execution=execution,
        postcheck=postcheck_payload,
        precheck_attempted=precheck_attempted,
        include_debug=include_debug,
    )


def _gui_click_fallback(driver, selector: str, timeframe: float, fx, fy) -> dict:
    """Fallback GUI click when CDP is not available."""
    try:
        by = "css selector"
        if isinstance(selector, str) and selector.strip().startswith("/"):
            by = "xpath"

        element = driver.find_element(by, selector)

        try:
            driver.execute_script(
                'arguments[0].scrollIntoView({block:"center", inline:"nearest"});',
                element,
            )
            time.sleep(0.05)
        except Exception:
            pass

        rect = driver.execute_script(
            "var r = arguments[0].getBoundingClientRect();return {x:r.left, y:r.top, width:r.width, height:r.height};",
            element,
        ) or {"x": 0, "y": 0, "width": 0, "height": 0}

        wrect = driver.get_window_rect()
        win_x = float(wrect.get("x", 0))
        win_y = float(wrect.get("y", 0))
        win_h = float(wrect.get("height", 0))
        viewport_h = float(driver.execute_script("return window.innerHeight;"))

        rx = float(rect.get("x", 0))
        ry = float(rect.get("y", 0))
        rw = float(rect.get("width", 0))
        rh = float(rect.get("height", 0))

        x0 = win_x + rx
        y0 = (win_y + win_h - viewport_h) + ry

        fx_val = float(fx) if fx is not None else 0.5
        fy_val = float(fy) if fy is not None else 0.5
        cx = x0 + rw * fx_val
        cy = y0 + rh * fy_val

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


def handle_gui_press_keys_xy(driver, command: dict) -> dict:
    """Press keys at coordinates (click to focus, then send keys)."""
    x = command.get("x")
    y = command.get("y")
    keys = command.get("keys")
    timeframe = command.get("timeframe", 0.25)

    if x is None or y is None:
        return {"status": "error", "message": "x and y coordinates are required"}
    if not keys:
        return {"status": "error", "message": "keys is required"}

    _ensure_cdp_mode(driver)
    _bring_window_to_front(driver)

    try:
        _gui_click_at(driver, x, y, timeframe)
        time.sleep(0.2)

        focused = driver.execute_script("return document.activeElement;")
        if not focused:
            return {"status": "error", "message": "No element focused after click"}

        if "+" in keys:
            parts = [p.strip().upper() for p in keys.split("+")]
            modifiers = parts[:-1]
            final_key = parts[-1]

            actions = ActionChains(driver)
            for mod in modifiers:
                actions.key_down(KEY_MAP.get(mod) or mod)
            actions.send_keys(KEY_MAP.get(final_key) or final_key)
            for mod in reversed(modifiers):
                actions.key_up(KEY_MAP.get(mod) or mod)
            actions.perform()
        else:
            key = KEY_MAP.get(keys.upper()) or keys
            focused.send_keys(key)

        return {"status": "success", "message": "Pressed keys at coordinates", "x": x, "y": y, "keys": keys}
    except Exception as e:
        return {"status": "error", "message": f"Failed to press keys: {str(e)}"}
