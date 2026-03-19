from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

AMBIGUITY_THRESHOLD = 4.0
DEFAULT_SNAP_RADIUS = 96.0
MAX_WINDOW_METRIC_DRIFT_PX = 4.0
VIEWPORT_TOLERANCE_PX = 2.0

CLICKABLE_INPUT_TYPES = {"button", "submit", "reset", "checkbox", "radio", "file", "image"}
LABELABLE_INPUT_TYPES = {"checkbox", "radio", "file"}
INTERACTIVE_ROLES = {"button", "link", "checkbox", "radio", "tab", "menuitem"}
NON_INTERACTIVE_REASONS = {
    "hit_html_root",
    "hit_body",
    "hit_non_interactive_element",
    "hit_hidden_element",
    "hit_pointer_events_none",
    "hit_disabled_element",
    "hit_aria_disabled_element",
    "hit_inert_element",
    "intent_mismatch",
}


class HitTestUnavailable(RuntimeError):
    """Raised when screen/viewport transforms cannot be trusted."""


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2.0, self.y + self.height / 2.0)

    def area(self) -> float:
        return max(0.0, self.width) * max(0.0, self.height)

    def contains_point(self, point: Point) -> bool:
        return self.x <= point.x <= self.right and self.y <= point.y <= self.bottom

    def intersects(self, other: Rect) -> bool:
        return not (self.right <= other.x or other.right <= self.x or self.bottom <= other.y or other.bottom <= self.y)

    def intersection_area(self, other: Rect) -> float:
        left = max(self.x, other.x)
        top = max(self.y, other.y)
        right = min(self.right, other.right)
        bottom = min(self.bottom, other.bottom)
        if right <= left or bottom <= top:
            return 0.0
        return (right - left) * (bottom - top)

    def nearest_point(self, point: Point) -> Point:
        x = min(max(point.x, self.x), self.right)
        y = min(max(point.y, self.y), self.bottom)
        return Point(x, y)

    @classmethod
    def from_mapping(cls, payload: dict[str, Any] | None) -> Rect | None:
        if not payload:
            return None
        return cls(
            float(payload.get("x", 0.0)),
            float(payload.get("y", 0.0)),
            float(payload.get("width", 0.0)),
            float(payload.get("height", 0.0)),
        )


@dataclass(frozen=True)
class WindowMetrics:
    window_x: float
    window_y: float
    screen_x: float
    screen_y: float
    inner_width: float
    inner_height: float
    outer_width: float
    outer_height: float
    scale: float
    offset_left: float
    offset_top: float
    device_pixel_ratio: float | None = None
    has_visual_viewport: bool = True

    @property
    def chrome_offset_y(self) -> float:
        return self.outer_height - self.inner_height


@dataclass(frozen=True)
class HitTestResult:
    viewport_point: Point
    target_rect: Rect | None
    tag: str
    text: str | None
    interactive: bool
    reason: str
    reason_detail: str | None = None
    element_path: str | None = None


HitTest = HitTestResult


@dataclass(frozen=True)
class SnapCandidate:
    tag: str
    text: str | None
    rect: Rect
    interactive: bool
    element_path: str | None = None
    href: str | None = None
    input_type: str | None = None
    role: str | None = None
    editable: bool = False
    has_onclick: bool = False
    tab_index: int | None = None
    disabled: bool = False
    aria_disabled: bool = False
    inert: bool = False
    visible: bool = True
    pointer_events: bool = True
    associated_control_type: str | None = None
    associated_control_disabled: bool = False
    associated_control_aria_disabled: bool = False
    associated_control_inert: bool = False


@dataclass(frozen=True)
class CandidateChoice:
    candidate: SnapCandidate | None
    reason: str | None
    top_score: float | None = None
    runner_up_score: float | None = None


@dataclass(frozen=True)
class SmartTargetResult:
    success: bool
    outcome_status: str
    reason: str | None
    reason_detail: str | None
    original_screen_point: Point
    original_viewport_point: Point | None
    resolved_screen_point: Point | None
    resolved_viewport_point: Point | None
    recommended_next_action: str
    hit_test_result: HitTestResult | None = None
    snap_candidate: SnapCandidate | None = None


def get_window_metrics(driver: Any) -> WindowMetrics:
    window_rect = driver.get_window_rect()
    payload = driver.execute_script(
        """
        const vv = window.visualViewport;
        return {
          screenX: window.screenX,
          screenY: window.screenY,
          innerWidth: window.innerWidth,
          innerHeight: window.innerHeight,
          outerWidth: window.outerWidth,
          outerHeight: window.outerHeight,
          scale: vv ? vv.scale : 1,
          offsetLeft: vv ? vv.offsetLeft : 0,
          offsetTop: vv ? vv.offsetTop : 0,
          devicePixelRatio: window.devicePixelRatio || 1,
          hasVisualViewport: !!vv,
        };
        """
    )
    return WindowMetrics(
        window_x=float(window_rect.get("x", 0.0)),
        window_y=float(window_rect.get("y", 0.0)),
        screen_x=float(payload.get("screenX", 0.0)),
        screen_y=float(payload.get("screenY", 0.0)),
        inner_width=float(payload.get("innerWidth", 0.0)),
        inner_height=float(payload.get("innerHeight", 0.0)),
        outer_width=float(payload.get("outerWidth", 0.0)),
        outer_height=float(payload.get("outerHeight", 0.0)),
        scale=float(payload.get("scale", 1.0)),
        offset_left=float(payload.get("offsetLeft", 0.0)),
        offset_top=float(payload.get("offsetTop", 0.0)),
        device_pixel_ratio=float(payload.get("devicePixelRatio", 1.0)),
        has_visual_viewport=bool(payload.get("hasVisualViewport", False)),
    )


def screen_to_viewport_point(metrics: WindowMetrics, point: Point) -> Point:
    _validate_metrics(metrics)

    if abs(metrics.window_x - metrics.screen_x) > MAX_WINDOW_METRIC_DRIFT_PX:
        raise HitTestUnavailable("window x metrics disagreed")
    if abs(metrics.window_y - metrics.screen_y) > MAX_WINDOW_METRIC_DRIFT_PX:
        raise HitTestUnavailable("window y metrics disagreed")

    viewport_x = ((point.x - metrics.window_x) / metrics.scale) - metrics.offset_left
    viewport_y = ((point.y - (metrics.window_y + metrics.chrome_offset_y)) / metrics.scale) - metrics.offset_top
    _validate_viewport_point(metrics, viewport_x, viewport_y)

    return Point(
        min(max(viewport_x, 0.0), metrics.inner_width),
        min(max(viewport_y, 0.0), metrics.inner_height),
    )


def viewport_to_screen_point(metrics: WindowMetrics, point: Point) -> Point:
    _validate_metrics(metrics)
    return Point(
        metrics.window_x + (point.x + metrics.offset_left) * metrics.scale,
        metrics.window_y + metrics.chrome_offset_y + (point.y + metrics.offset_top) * metrics.scale,
    )


def hit_test_point(driver: Any, viewport_point: Point) -> HitTestResult:
    payload = driver.execute_script(
        """
        const x = arguments[0], y = arguments[1];
        const deepElementFromPoint = (root, pointX, pointY) => {
          if (!root || typeof root.elementFromPoint !== 'function') {
            return null;
          }
          let current = root.elementFromPoint(pointX, pointY);
          while (current && current.shadowRoot && typeof current.shadowRoot.elementFromPoint === 'function') {
            const nested = current.shadowRoot.elementFromPoint(pointX, pointY);
            if (!nested || nested === current) {
              break;
            }
            current = nested;
          }
          return current;
        };
        const elementPath = (node) => {
          const parts = [];
          for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; ) {
            let index = 0;
            for (let sibling = current; (sibling = sibling.previousElementSibling); ) index += 1;
            parts.push(`${current.tagName}[${index}]`);
            if (current.parentElement) {
              current = current.parentElement;
              continue;
            }
            const root = current.getRootNode();
            current = root && root.host ? root.host : null;
          }
          return parts.reverse().join('>');
        };
        const rawEl = document.elementFromPoint(x, y);
        const deepEl = deepElementFromPoint(document, x, y) || rawEl;
        if (!deepEl) {
          return {viewport_point: {x, y}, target_rect: null, tag: '', text: '', hidden: false, pointer_events_none: false, disabled: false, aria_disabled: false, inert: false, href: null, input_type: null, role: null, editable: false, has_onclick: false, tab_index: null, element_path: null, shadow_boundary: false};
        }

        const labelSurface = typeof deepEl.closest === 'function' ? deepEl.closest('label') : null;
        const labelControl = labelSurface && labelSurface.control ? labelSurface.control : null;
        const labelControlType = labelControl ? (labelControl.getAttribute('type') || 'text').toLowerCase() : null;
        const semanticLabelSurface = labelSurface && ['checkbox', 'radio', 'file'].includes(labelControlType) ? labelSurface : null;
        const el = semanticLabelSurface || deepEl;

        const style = getComputedStyle(el), rect = el.getBoundingClientRect();
        const tag = (el.tagName || '').toUpperCase(), role = (el.getAttribute('role') || '').toLowerCase();
        const inputType = (el.getAttribute('type') || '').toLowerCase(), disabled = !!el.disabled;
        const ariaDisabled = el.getAttribute('aria-disabled') === 'true', inert = !!el.closest('[inert]');
        const hidden = style.display === 'none' || style.visibility === 'hidden' || rect.width <= 0 || rect.height <= 0;
        const rawTag = (rawEl && rawEl.tagName) || '';
        const shadowBoundary = (
          !!rawEl &&
          rawEl === el &&
          rawEl.shadowRoot === null &&
          rawTag.includes('-') &&
          !rawEl.childElementCount &&
          !((rawEl.innerText || rawEl.textContent || '').trim())
        );
        return {
          viewport_point: {x, y},
          target_rect: {x: rect.left, y: rect.top, width: rect.width, height: rect.height},
          tag,
          text: (el.innerText || el.textContent || '').trim().slice(0, 200),
          hidden,
          pointer_events_none: style.pointerEvents === 'none',
          disabled,
          aria_disabled: ariaDisabled,
          inert,
          href: el.getAttribute('href'),
          input_type: inputType,
          role,
          associated_control: labelControl ? {disabled: !!labelControl.disabled || !!labelControl.closest('fieldset:disabled'), aria_disabled: labelControl.getAttribute('aria-disabled') === 'true', inert: !!labelControl.closest('[inert]')} : null,
          associated_control_type: labelControlType,
          editable: el.isContentEditable || tag === 'TEXTAREA' || tag === 'SELECT' || (tag === 'INPUT' && !['button', 'submit', 'reset', 'checkbox', 'radio', 'file', 'image'].includes(inputType)),
          has_onclick: typeof el.onclick === 'function',
          tab_index: Number.isFinite(el.tabIndex) ? el.tabIndex : null,
          element_path: elementPath(el),
          shadow_boundary: shadowBoundary,
        };
        """,
        viewport_point.x,
        viewport_point.y,
    )
    tag = (payload.get("tag") or "").upper()
    input_type = (payload.get("input_type") or "").lower()
    role = (payload.get("role") or "").lower()
    associated_control = payload.get("associated_control") or {}
    associated_control_type = (payload.get("associated_control_type") or "").lower()
    tab_index = payload.get("tab_index")
    try:
        tab_index = int(tab_index) if tab_index is not None else None
    except (TypeError, ValueError):
        tab_index = None

    is_clickable_input = tag == "INPUT" and input_type in CLICKABLE_INPUT_TYPES
    is_label_surface = tag == "LABEL" and associated_control_type in LABELABLE_INPUT_TYPES
    is_editable = (
        bool(payload.get("editable", False))
        or tag in {"TEXTAREA", "SELECT"}
        or (tag == "INPUT" and not is_clickable_input)
    )
    is_interactive = (
        is_label_surface
        or (tag == "A" and bool(payload.get("href")))
        or tag == "BUTTON"
        or is_clickable_input
        or is_editable
        or role in INTERACTIVE_ROLES
        or bool(payload.get("has_onclick", False))
        or (tab_index is not None and tab_index >= 0)
    )
    hidden = bool(payload.get("hidden", False))
    pointer_events_none = bool(payload.get("pointer_events_none", False))
    disabled = bool(payload.get("disabled", False)) or (
        is_label_surface and bool(associated_control.get("disabled", False))
    )
    aria_disabled = bool(payload.get("aria_disabled", False)) or (
        is_label_surface and bool(associated_control.get("aria_disabled", False))
    )
    inert = bool(payload.get("inert", False)) or (is_label_surface and bool(associated_control.get("inert", False)))
    shadow_boundary = bool(payload.get("shadow_boundary", False))
    if tag == "HTML":
        reason, reason_detail = "hit_html_root", "hit non-interactive root element"
    elif tag == "BODY":
        reason, reason_detail = "hit_body", "hit non-interactive body element"
    elif tag == "IFRAME":
        reason, reason_detail = "hit_iframe_boundary", "hit iframe boundary"
    elif shadow_boundary:
        reason, reason_detail = "shadow_boundary", "hit inaccessible shadow boundary"
    elif hidden:
        reason, reason_detail = "hit_hidden_element", "hit hidden element"
    elif pointer_events_none:
        reason, reason_detail = "hit_pointer_events_none", "hit pointer-events none element"
    elif disabled:
        reason, reason_detail = "hit_disabled_element", "hit disabled element"
    elif aria_disabled:
        reason, reason_detail = "hit_aria_disabled_element", "hit aria-disabled element"
    elif inert:
        reason, reason_detail = "hit_inert_element", "hit inert element"
    elif is_interactive:
        reason, reason_detail = "hit_interactive_element", None
    else:
        reason, reason_detail = "hit_non_interactive_element", None
    return HitTestResult(
        viewport_point=Point(float(payload["viewport_point"]["x"]), float(payload["viewport_point"]["y"])),
        target_rect=Rect.from_mapping(payload.get("target_rect")),
        tag=tag,
        text=payload.get("text"),
        interactive=is_interactive
        and tag != "IFRAME"
        and not hidden
        and not pointer_events_none
        and not disabled
        and not aria_disabled
        and not inert,
        reason=reason,
        reason_detail=reason_detail,
        element_path=payload.get("element_path"),
    )


def collect_snap_candidates(source: Any, mode: str, viewport_point: Point) -> list[SnapCandidate]:
    if mode == "off":
        return []

    raw_candidates = _load_candidate_snapshot(source, mode, viewport_point)
    candidates: list[SnapCandidate] = []
    for item in raw_candidates:
        candidate = _candidate_from_snapshot(item)
        if candidate is None or not _candidate_allowed(candidate, mode):
            continue
        candidates.append(candidate)
    return candidates


def choose_candidate(
    candidates: Sequence[SnapCandidate],
    viewport_point: Point,
    original_bbox: Rect | None = None,
    snap_radius: float = DEFAULT_SNAP_RADIUS,
) -> CandidateChoice:
    ranked: list[tuple[float, float, SnapCandidate]] = []
    for candidate in candidates:
        distance = _distance_to_rect(viewport_point, candidate.rect)
        if distance > snap_radius:
            continue
        score = _candidate_score(candidate, viewport_point, original_bbox)
        ranked.append((score, distance, candidate))

    if not ranked:
        return CandidateChoice(candidate=None, reason="no_candidate_within_radius")

    ranked.sort(key=lambda item: (-item[0], item[1], item[2].rect.y, item[2].rect.x, item[2].tag, item[2].text or ""))
    top_score, _, top_candidate = ranked[0]
    if len(ranked) > 1:
        runner_up_score = ranked[1][0]
        if top_score - runner_up_score <= AMBIGUITY_THRESHOLD:
            return CandidateChoice(
                candidate=None, reason="ambiguous_target", top_score=top_score, runner_up_score=runner_up_score
            )
        return CandidateChoice(
            candidate=top_candidate, reason=None, top_score=top_score, runner_up_score=runner_up_score
        )

    return CandidateChoice(candidate=top_candidate, reason=None, top_score=top_score)


def snapped_click_point(candidate: SnapCandidate) -> Point:
    if _is_editable_candidate(candidate):
        return Point(candidate.rect.x + candidate.rect.width * 0.25, candidate.rect.y + candidate.rect.height * 0.5)
    return candidate.rect.center


def resolve_detect_target(
    raw_point: Point,
    raw_bbox: Rect | None = None,
    *,
    raw_viewport_point: Point | None = None,
    window_metrics: WindowMetrics | None = None,
    driver: Any | None = None,
    hit_test_mode: str = "off",
    auto_snap: str = "off",
    snap_radius: float = DEFAULT_SNAP_RADIUS,
    hit_test_result: HitTestResult | None = None,
    hit_test_error: Exception | None = None,
    snap_candidates: Sequence[SnapCandidate] | None = None,
    resolved_hit_test_result: HitTestResult | None = None,
    resolved_hit_test_error: Exception | None = None,
) -> SmartTargetResult:
    return _resolve_target(
        raw_point=raw_point,
        raw_bbox=raw_bbox,
        raw_viewport_point=raw_viewport_point,
        window_metrics=window_metrics,
        driver=driver,
        validation_mode=hit_test_mode,
        auto_snap=auto_snap,
        snap_radius=snap_radius,
        hit_test_result=hit_test_result,
        hit_test_error=hit_test_error,
        snap_candidates=snap_candidates,
        resolved_hit_test_result=resolved_hit_test_result,
        resolved_hit_test_error=resolved_hit_test_error,
        disabled_status="raw_vision_point",
        result_kind="detect",
    )


def resolve_click_target(
    raw_point: Point,
    *,
    raw_viewport_point: Point | None = None,
    window_metrics: WindowMetrics | None = None,
    driver: Any | None = None,
    pre_click_validate: str = "off",
    auto_snap: str = "off",
    snap_radius: float = DEFAULT_SNAP_RADIUS,
    hit_test_result: HitTestResult | None = None,
    hit_test_error: Exception | None = None,
    snap_candidates: Sequence[SnapCandidate] | None = None,
    resolved_hit_test_result: HitTestResult | None = None,
    resolved_hit_test_error: Exception | None = None,
) -> SmartTargetResult:
    return _resolve_target(
        raw_point=raw_point,
        raw_bbox=None,
        raw_viewport_point=raw_viewport_point,
        window_metrics=window_metrics,
        driver=driver,
        validation_mode=pre_click_validate,
        auto_snap=auto_snap,
        snap_radius=snap_radius,
        hit_test_result=hit_test_result,
        hit_test_error=hit_test_error,
        snap_candidates=snap_candidates,
        resolved_hit_test_result=resolved_hit_test_result,
        resolved_hit_test_error=resolved_hit_test_error,
        disabled_status="clicked_raw",
        result_kind="click",
    )


def _resolve_target(
    *,
    raw_point: Point,
    raw_bbox: Rect | None,
    raw_viewport_point: Point | None,
    window_metrics: WindowMetrics | None,
    driver: Any | None,
    validation_mode: str,
    auto_snap: str,
    snap_radius: float,
    hit_test_result: HitTestResult | None,
    hit_test_error: Exception | None,
    snap_candidates: Sequence[SnapCandidate] | None,
    resolved_hit_test_result: HitTestResult | None,
    resolved_hit_test_error: Exception | None,
    disabled_status: str,
    result_kind: str,
) -> SmartTargetResult:
    if validation_mode == "off" and auto_snap == "off":
        return SmartTargetResult(
            success=True,
            outcome_status=disabled_status,
            reason=None,
            reason_detail=None,
            original_screen_point=raw_point,
            original_viewport_point=raw_viewport_point,
            resolved_screen_point=raw_point,
            resolved_viewport_point=raw_viewport_point,
            recommended_next_action="proceed",
        )

    try:
        metrics = window_metrics or (get_window_metrics(driver) if driver is not None else None)
        viewport_point = raw_viewport_point or (
            screen_to_viewport_point(metrics, raw_point) if metrics is not None else None
        )
        if viewport_point is None:
            raise HitTestUnavailable("viewport transform unavailable")
    except HitTestUnavailable as exc:
        hit_test_error = exc
        viewport_point = raw_viewport_point
        metrics = window_metrics
    else:
        if hit_test_result is None and driver is not None:
            try:
                hit_test_result = hit_test_point(driver, viewport_point)
            except Exception as exc:  # pragma: no cover - exercised in browser flows later
                hit_test_error = HitTestUnavailable(str(exc))
        if snap_candidates is None and driver is not None and auto_snap != "off":
            snap_candidates = collect_snap_candidates(driver, auto_snap, viewport_point)

    if hit_test_error is not None:
        return _failure_result(
            result_kind=result_kind,
            reason="hit_test_unavailable",
            reason_detail=str(hit_test_error),
            validation_mode=validation_mode,
            auto_snap=auto_snap,
            raw_point=raw_point,
            raw_viewport_point=viewport_point,
        )

    if hit_test_result is None:
        return _failure_result(
            result_kind=result_kind,
            reason="hit_test_unavailable",
            reason_detail="hit test result missing",
            validation_mode=validation_mode,
            auto_snap=auto_snap,
            raw_point=raw_point,
            raw_viewport_point=viewport_point,
        )

    unsafe_reason = hit_test_result.reason
    if unsafe_reason in {"hit_iframe_boundary", "shadow_boundary"}:
        return _failure_result(
            result_kind=result_kind,
            reason=unsafe_reason,
            reason_detail=hit_test_result.reason_detail,
            validation_mode=validation_mode,
            auto_snap=auto_snap,
            raw_point=raw_point,
            raw_viewport_point=viewport_point,
            hit_test_result=hit_test_result,
        )

    if hit_test_result.interactive and _is_intent_consistent(raw_bbox, hit_test_result.target_rect):
        return SmartTargetResult(
            success=True,
            outcome_status="clicked_exact" if result_kind == "click" else "exact_match",
            reason="hit_interactive_element",
            reason_detail=hit_test_result.reason_detail,
            original_screen_point=raw_point,
            original_viewport_point=viewport_point,
            resolved_screen_point=raw_point,
            resolved_viewport_point=viewport_point,
            recommended_next_action="proceed",
            hit_test_result=hit_test_result,
        )

    if hit_test_result.interactive and not _is_intent_consistent(raw_bbox, hit_test_result.target_rect):
        unsafe_reason = "intent_mismatch"

    if auto_snap != "off":
        assert viewport_point is not None
        candidates = list(snap_candidates or [])
        choice = choose_candidate(candidates, viewport_point, raw_bbox, snap_radius)
        if choice.candidate is None:
            failure_reason = choice.reason or unsafe_reason
            failure_detail = hit_test_result.reason_detail if failure_reason == unsafe_reason else None
            return _failure_result(
                result_kind=result_kind,
                reason=failure_reason,
                reason_detail=failure_detail,
                validation_mode=validation_mode,
                auto_snap=auto_snap,
                raw_point=raw_point,
                raw_viewport_point=viewport_point,
                hit_test_result=hit_test_result,
            )

        resolved_viewport_point = snapped_click_point(choice.candidate)
        if resolved_hit_test_result is None and resolved_hit_test_error is None and driver is not None:
            try:
                resolved_hit_test_result = hit_test_point(driver, resolved_viewport_point)
            except Exception as exc:  # pragma: no cover - exercised in browser flows later
                resolved_hit_test_error = HitTestUnavailable(str(exc))
        if resolved_hit_test_error is not None or resolved_hit_test_result is None:
            return _failure_result(
                result_kind=result_kind,
                reason="hit_test_unavailable",
                reason_detail=str(resolved_hit_test_error or "resolved hit test result missing"),
                validation_mode=validation_mode,
                auto_snap=auto_snap,
                raw_point=raw_point,
                raw_viewport_point=viewport_point,
                hit_test_result=resolved_hit_test_result,
            )
        if not _candidate_hit_matches(choice.candidate, resolved_hit_test_result):
            mismatch_reason = (
                "intent_mismatch" if resolved_hit_test_result.interactive else resolved_hit_test_result.reason
            )
            return _failure_result(
                result_kind=result_kind,
                reason=mismatch_reason,
                reason_detail=resolved_hit_test_result.reason_detail or "resolved point missed chosen candidate",
                validation_mode=validation_mode,
                auto_snap=auto_snap,
                raw_point=raw_point,
                raw_viewport_point=viewport_point,
                hit_test_result=resolved_hit_test_result,
            )
        resolved_screen_point = _resolve_screen_point(raw_point, viewport_point, resolved_viewport_point, metrics)
        return SmartTargetResult(
            success=True,
            outcome_status="clicked_snapped" if result_kind == "click" else "snapped_match",
            reason=unsafe_reason,
            reason_detail=hit_test_result.reason_detail,
            original_screen_point=raw_point,
            original_viewport_point=viewport_point,
            resolved_screen_point=resolved_screen_point,
            resolved_viewport_point=resolved_viewport_point,
            recommended_next_action="proceed",
            hit_test_result=hit_test_result,
            snap_candidate=choice.candidate,
        )

    return _failure_result(
        result_kind=result_kind,
        reason=unsafe_reason,
        reason_detail=hit_test_result.reason_detail,
        validation_mode=validation_mode,
        auto_snap=auto_snap,
        raw_point=raw_point,
        raw_viewport_point=viewport_point,
        hit_test_result=hit_test_result,
    )


def _detect_failure_result(
    *,
    reason: str,
    reason_detail: str | None,
    validation_mode: str,
    auto_snap: str,
    raw_point: Point,
    raw_viewport_point: Point | None,
    hit_test_result: HitTestResult | None = None,
) -> SmartTargetResult:
    if reason == "ambiguous_target":
        outcome_status = "fail_ambiguous_target"
        success = False
        next_action = "switch_to_selector_click"
    elif reason == "hit_iframe_boundary":
        outcome_status = "fail_iframe_boundary"
        success = False
        next_action = "switch_to_iframe_context"
    elif reason == "shadow_boundary":
        outcome_status = "fail_hit_test_unavailable"
        success = False
        next_action = "switch_to_selector_click"
    elif reason == "no_candidate_within_radius":
        outcome_status = "fail_no_target"
        success = False
        next_action = "retry_with_larger_radius"
    elif reason == "hit_test_unavailable":
        if auto_snap != "off" or validation_mode == "strict":
            outcome_status = "fail_hit_test_unavailable"
            success = False
        else:
            outcome_status = "warn_hit_test_unavailable"
            success = True
        next_action = "inspect_page"
    elif reason in NON_INTERACTIVE_REASONS:
        if validation_mode == "warn":
            outcome_status = "warn_non_interactive"
            success = True
        else:
            outcome_status = "fail_non_interactive"
            success = False
        next_action = "inspect_page"
    else:
        outcome_status = "fail_non_interactive"
        success = False
        next_action = "inspect_page"

    return SmartTargetResult(
        success=success,
        outcome_status=outcome_status,
        reason=reason,
        reason_detail=reason_detail or _default_reason_detail(reason),
        original_screen_point=raw_point,
        original_viewport_point=raw_viewport_point,
        resolved_screen_point=raw_point,
        resolved_viewport_point=raw_viewport_point,
        recommended_next_action=next_action,
        hit_test_result=hit_test_result,
    )


def _click_failure_result(
    *,
    reason: str,
    reason_detail: str | None,
    validation_mode: str,
    auto_snap: str,
    raw_point: Point,
    raw_viewport_point: Point | None,
    hit_test_result: HitTestResult | None = None,
) -> SmartTargetResult:
    if reason == "ambiguous_target":
        outcome_status, success, next_action = "click_failed_precheck", False, "switch_to_selector_click"
    elif reason == "hit_iframe_boundary":
        outcome_status, success, next_action = "click_failed_precheck", False, "switch_to_iframe_context"
    elif reason == "shadow_boundary":
        outcome_status, success, next_action = "click_failed_precheck", False, "switch_to_selector_click"
    elif reason == "hit_test_unavailable" and auto_snap != "off":
        outcome_status, success, next_action = "click_failed_precheck", False, "inspect_page"
    elif validation_mode == "strict":
        next_action = "switch_to_selector_click" if reason == "ambiguous_target" else "inspect_page"
        if reason == "no_candidate_within_radius":
            next_action = "retry_with_larger_radius"
        outcome_status, success = "click_failed_precheck", False
    else:
        outcome_status, success, next_action = "clicked_raw", True, "inspect_page"

    return SmartTargetResult(
        success=success,
        outcome_status=outcome_status,
        reason=reason,
        reason_detail=reason_detail or _default_reason_detail(reason),
        original_screen_point=raw_point,
        original_viewport_point=raw_viewport_point,
        resolved_screen_point=raw_point,
        resolved_viewport_point=raw_viewport_point,
        recommended_next_action=next_action,
        hit_test_result=hit_test_result,
    )


def _failure_result(*, result_kind: str, **kwargs: Any) -> SmartTargetResult:
    if result_kind == "click":
        return _click_failure_result(**kwargs)
    return _detect_failure_result(**kwargs)


def _load_candidate_snapshot(source: Any, mode: str, viewport_point: Point) -> Iterable[dict[str, Any]]:
    if hasattr(source, "execute_script"):
        payload = source.execute_script(
            """
            const mode = arguments[0], point = arguments[1];
            const elementPath = (node) => {
              const parts = [];
              for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; ) {
                let index = 0;
                for (let sibling = current; (sibling = sibling.previousElementSibling); ) index += 1;
                parts.push(`${current.tagName}[${index}]`);
                if (current.parentElement) {
                  current = current.parentElement;
                  continue;
                }
                const root = current.getRootNode();
                current = root && root.host ? root.host : null;
              }
              return parts.reverse().join('>');
            };
            const selectors = ['a[href]', 'button', 'input', 'textarea', 'select', 'label', '[role]', '[onclick]', '[tabindex]', '[contenteditable]'];
            const selectorText = selectors.join(',');
            const seen = new Set();
            const nodes = [];
            const visit = (root) => {
              if (!root || !root.children) {
                return;
              }
              for (const child of Array.from(root.children)) {
                if (typeof child.matches === 'function' && child.matches(selectorText) && !seen.has(child)) {
                  seen.add(child);
                  nodes.push(child);
                }
                if (child.shadowRoot) {
                  visit(child.shadowRoot);
                }
                visit(child);
              }
            };
            visit(document);
            return nodes.map((el) => {
              const tag = (el.tagName || '').toUpperCase(), style = getComputedStyle(el), rect = el.getBoundingClientRect();
              const control = tag === 'LABEL' && el.control ? el.control : null;
              return {
                tag,
                text: (el.innerText || el.textContent || '').trim().slice(0, 200),
                element_path: elementPath(el),
                href: el.getAttribute('href'),
                input_type: (el.getAttribute('type') || '').toLowerCase(),
                role: (el.getAttribute('role') || '').toLowerCase(),
                editable: !!el.isContentEditable || ['TEXTAREA', 'SELECT'].includes(tag),
                has_onclick: typeof el.onclick === 'function',
                tab_index: Number.isFinite(el.tabIndex) ? el.tabIndex : null,
                visible: style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0 && rect.bottom >= 0 && rect.right >= 0 && rect.top <= window.innerHeight && rect.left <= window.innerWidth,
                pointer_events: style.pointerEvents !== 'none',
                disabled: !!el.disabled || !!el.closest('fieldset:disabled'),
                aria_disabled: el.getAttribute('aria-disabled') === 'true',
                inert: !!el.closest('[inert]'),
                interactive: mode === 'nearest_clickable' ? true : true,
                associated_control: control ? {disabled: !!control.disabled || !!control.closest('fieldset:disabled'), aria_disabled: control.getAttribute('aria-disabled') === 'true', inert: !!control.closest('[inert]')} : null,
                associated_control_type: control ? (control.getAttribute('type') || '').toLowerCase() : null,
                rect: {x: rect.left, y: rect.top, width: rect.width, height: rect.height},
              };
            });
            """,
            mode,
            {"x": viewport_point.x, "y": viewport_point.y},
        )
        if isinstance(payload, dict) and "candidates" in payload:
            return payload["candidates"]
        return payload or []

    if isinstance(source, Sequence) and not isinstance(source, (str, bytes, bytearray, dict)):
        return source

    return []


def _candidate_from_snapshot(payload: dict[str, Any]) -> SnapCandidate | None:
    rect = Rect.from_mapping(payload.get("rect"))
    if rect is None:
        return None

    associated = payload.get("associated_control") or {}
    tab_index = payload.get("tab_index")
    if tab_index is not None:
        try:
            tab_index = int(tab_index)
        except (TypeError, ValueError):
            tab_index = None

    return SnapCandidate(
        tag=(payload.get("tag") or "").upper(),
        text=payload.get("text"),
        rect=rect,
        interactive=bool(payload.get("interactive", False)),
        element_path=payload.get("element_path"),
        href=payload.get("href"),
        input_type=(payload.get("input_type") or None),
        role=(payload.get("role") or None),
        editable=bool(payload.get("editable", False)),
        has_onclick=bool(payload.get("has_onclick", False)),
        tab_index=tab_index,
        disabled=bool(payload.get("disabled", False)),
        aria_disabled=bool(payload.get("aria_disabled", False)),
        inert=bool(payload.get("inert", False)),
        visible=bool(payload.get("visible", False)),
        pointer_events=bool(payload.get("pointer_events", False)),
        associated_control_type=(payload.get("associated_control_type") or None),
        associated_control_disabled=bool(associated.get("disabled", False)),
        associated_control_aria_disabled=bool(associated.get("aria_disabled", False)),
        associated_control_inert=bool(associated.get("inert", False)),
    )


def _candidate_allowed(candidate: SnapCandidate, mode: str) -> bool:
    if candidate.tag in {"", "HTML", "BODY"}:
        return False
    if not candidate.visible or not candidate.pointer_events:
        return False
    if candidate.disabled or candidate.aria_disabled or candidate.inert:
        return False
    if candidate.rect.width <= 0 or candidate.rect.height <= 0:
        return False
    if _is_label_surface(candidate):
        return not (
            candidate.associated_control_disabled
            or candidate.associated_control_aria_disabled
            or candidate.associated_control_inert
        )
    if mode == "nearest_clickable":
        return _is_clickable_candidate(candidate)
    if mode == "nearest_interactive":
        return _is_clickable_candidate(candidate) or _is_interactive_candidate(candidate)
    return False


def _is_clickable_candidate(candidate: SnapCandidate) -> bool:
    if candidate.tag == "A" and candidate.href:
        return True
    if candidate.tag == "BUTTON":
        return True
    if candidate.tag == "INPUT" and _normalized_input_type(candidate.input_type) in CLICKABLE_INPUT_TYPES:
        return True
    return _is_label_surface(candidate)


def _is_interactive_candidate(candidate: SnapCandidate) -> bool:
    if _is_editable_candidate(candidate):
        return True
    if candidate.role in INTERACTIVE_ROLES:
        return True
    if candidate.has_onclick:
        return True
    return candidate.tab_index is not None and candidate.tab_index >= 0


def _is_label_surface(candidate: SnapCandidate) -> bool:
    return candidate.tag == "LABEL" and candidate.associated_control_type in LABELABLE_INPUT_TYPES


def _is_editable_candidate(candidate: SnapCandidate) -> bool:
    if candidate.editable:
        return True
    if candidate.tag in {"TEXTAREA", "SELECT"}:
        return True
    if candidate.tag == "INPUT":
        return _normalized_input_type(candidate.input_type) not in CLICKABLE_INPUT_TYPES
    return False


def _normalized_input_type(value: str | None) -> str:
    normalized = (value or "text").strip().lower()
    return normalized or "text"


def _candidate_score(candidate: SnapCandidate, viewport_point: Point, original_bbox: Rect | None) -> float:
    score = _semantic_score(candidate)
    if original_bbox is not None:
        if original_bbox.contains_point(candidate.rect.center):
            score += 15.0
        elif original_bbox.intersects(candidate.rect):
            score += 8.0
    distance = _distance_to_rect(viewport_point, candidate.rect)
    score += max(0.0, 30.0 - distance * 0.3)
    return score


def _semantic_score(candidate: SnapCandidate) -> float:
    if candidate.tag == "A" and candidate.href:
        return 40.0
    if candidate.tag == "BUTTON":
        return 40.0
    if candidate.tag == "INPUT" and _normalized_input_type(candidate.input_type) in CLICKABLE_INPUT_TYPES:
        return 38.0
    if _is_label_surface(candidate):
        return 36.0
    if _is_editable_candidate(candidate):
        return 35.0
    if candidate.role in INTERACTIVE_ROLES:
        return 28.0
    if candidate.has_onclick:
        return 20.0
    if candidate.tab_index is not None and candidate.tab_index >= 0:
        return 12.0
    return 0.0


def _distance_to_rect(point: Point, rect: Rect) -> float:
    nearest = rect.nearest_point(point)
    return math.hypot(point.x - nearest.x, point.y - nearest.y)


def _candidate_hit_matches(candidate: SnapCandidate, hit_test_result: HitTestResult) -> bool:
    if hit_test_result.target_rect is None:
        return False
    candidate_path = candidate.element_path
    hit_path = hit_test_result.element_path
    if not candidate_path or not hit_path:
        return False
    path_matches = hit_path == candidate_path or hit_path.startswith(f"{candidate_path}>")
    if not path_matches:
        return False
    return hit_test_result.interactive or _is_label_surface(candidate)


def _is_intent_consistent(original_bbox: Rect | None, target_rect: Rect | None) -> bool:
    if original_bbox is None:
        return True
    if target_rect is None:
        return False
    if original_bbox.contains_point(target_rect.center):
        return True
    overlap = original_bbox.intersection_area(target_rect)
    if overlap <= 0.0:
        return False
    return overlap / max(target_rect.area(), 1.0) >= 0.25


def _resolve_screen_point(
    raw_point: Point,
    raw_viewport_point: Point | None,
    resolved_viewport_point: Point | None,
    metrics: WindowMetrics | None,
) -> Point | None:
    if resolved_viewport_point is None:
        return None
    if raw_viewport_point is not None and raw_viewport_point == resolved_viewport_point:
        return raw_point
    if metrics is None:
        return None
    return viewport_to_screen_point(metrics, resolved_viewport_point)


def _validate_metrics(metrics: WindowMetrics) -> None:
    values = (
        metrics.window_x,
        metrics.window_y,
        metrics.screen_x,
        metrics.screen_y,
        metrics.inner_width,
        metrics.inner_height,
        metrics.outer_width,
        metrics.outer_height,
        metrics.scale,
        metrics.offset_left,
        metrics.offset_top,
    )
    if not all(math.isfinite(value) for value in values):
        raise HitTestUnavailable("window metrics were not finite")
    if metrics.scale <= 0:
        raise HitTestUnavailable("visual viewport scale was invalid")
    if metrics.inner_width <= 0 or metrics.inner_height <= 0:
        raise HitTestUnavailable("viewport metrics were invalid")
    if (metrics.device_pixel_ratio or 1.0) != 1.0 and not metrics.has_visual_viewport:
        raise HitTestUnavailable("visual viewport metrics unavailable for HiDPI or scaled viewport")


def _validate_viewport_point(metrics: WindowMetrics, viewport_x: float, viewport_y: float) -> None:
    if not math.isfinite(viewport_x) or not math.isfinite(viewport_y):
        raise HitTestUnavailable("viewport point was not finite")
    if viewport_x < -VIEWPORT_TOLERANCE_PX or viewport_x > metrics.inner_width + VIEWPORT_TOLERANCE_PX:
        raise HitTestUnavailable("viewport x fell outside trusted bounds")
    if viewport_y < -VIEWPORT_TOLERANCE_PX or viewport_y > metrics.inner_height + VIEWPORT_TOLERANCE_PX:
        raise HitTestUnavailable("viewport y fell outside trusted bounds")


def _default_reason_detail(reason: str) -> str:
    return {
        "hit_html_root": "hit non-interactive root element",
        "hit_body": "hit non-interactive body element",
        "hit_non_interactive_element": "hit non-interactive element",
        "hit_hidden_element": "hit hidden element",
        "hit_pointer_events_none": "hit pointer-events none element",
        "hit_disabled_element": "hit disabled element",
        "hit_aria_disabled_element": "hit aria-disabled element",
        "hit_inert_element": "hit inert element",
        "hit_iframe_boundary": "hit iframe boundary",
        "shadow_boundary": "hit inaccessible shadow boundary",
        "hit_test_unavailable": "hit test could not produce trustworthy coordinates",
        "intent_mismatch": "interactive hit did not align with the original vision box",
        "ambiguous_target": "nearby candidates were too close to disambiguate safely",
        "no_candidate_within_radius": "no candidate fell within the configured snap radius",
    }.get(reason, reason)


__all__ = [
    "AMBIGUITY_THRESHOLD",
    "CandidateChoice",
    "DEFAULT_SNAP_RADIUS",
    "HitTest",
    "HitTestResult",
    "HitTestUnavailable",
    "Point",
    "Rect",
    "SmartTargetResult",
    "SnapCandidate",
    "WindowMetrics",
    "choose_candidate",
    "collect_snap_candidates",
    "get_window_metrics",
    "hit_test_point",
    "resolve_click_target",
    "resolve_detect_target",
    "screen_to_viewport_point",
    "snapped_click_point",
    "viewport_to_screen_point",
]
