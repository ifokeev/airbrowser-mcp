from __future__ import annotations

import hashlib

import pytest

from airbrowser.server.browser.postclick_feedback import (
    PostClickSnapshot,
    capture_postclick_snapshot,
    diff_postclick_snapshot,
)
from airbrowser.server.browser.smart_targeting import (
    HitTestResult,
    HitTestUnavailable,
    Point,
    Rect,
    WindowMetrics,
    choose_candidate,
    collect_snap_candidates,
    hit_test_point,
    resolve_click_target,
    resolve_detect_target,
    screen_to_viewport_point,
    snapped_click_point,
)


class FakeDriver:
    def __init__(self, payload):
        self.payload = payload

    def execute_script(self, script, *args):
        return self.payload


class TargetAwareSnapshotDriver:
    def __init__(self, *, active_state, target_state):
        self.active_state = active_state
        self.target_state = target_state
        self.calls = []

    def execute_script(self, script, *args):
        self.calls.append(args)
        target_element_path = args[0] if args else None
        return {
            "url": "https://example.com/",
            "content": "abcdefghijklmnopqrstuvwxyz",
            "active_element": {"tag": "INPUT", "role": "textbox"},
            "visible_state": self.target_state if target_element_path else self.active_state,
        }


def _visible_state(**overrides):
    state = {
        "checked": False,
        "selected": False,
        "expanded": False,
        "pressed": False,
        "class_name": "toggle",
        "style": "display:block",
        "subtree_digest": "digest-before",
    }
    state.update(overrides)
    return state


def _postclick_snapshot(**overrides):
    snapshot = {
        "url": "https://example.com/",
        "content_hash": "hash-before",
        "content_summary": "before summary",
        "content": None,
        "active_element_tag": None,
        "active_element_role": None,
        "visible_state": _visible_state(),
    }
    snapshot.update(overrides)
    return PostClickSnapshot(**snapshot)


def test_raw_vision_point_when_validation_disabled():
    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        hit_test_mode="off",
        auto_snap="off",
    )

    assert result.success is True
    assert result.outcome_status == "raw_vision_point"
    assert result.reason is None
    assert result.recommended_next_action == "proceed"


def test_warn_non_interactive_when_auto_snap_off():
    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        raw_viewport_point=Point(325, 260),
        hit_test_mode="warn",
        auto_snap="off",
        hit_test_result=HitTestResult(
            viewport_point=Point(325, 260),
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
    )

    assert result.success is True
    assert result.outcome_status == "warn_non_interactive"
    assert result.reason == "hit_html_root"
    assert result.recommended_next_action == "inspect_page"


def test_hit_test_point_treats_tabindex_zero_as_interactive():
    driver = FakeDriver(
        {
            "viewport_point": {"x": 60, "y": 35},
            "target_rect": {"x": 40, "y": 20, "width": 80, "height": 30},
            "tag": "DIV",
            "text": "Focusable chip",
            "href": None,
            "input_type": None,
            "role": None,
            "editable": False,
            "disabled": False,
            "aria_disabled": False,
            "inert": False,
            "hidden": False,
            "pointer_events_none": False,
            "has_onclick": False,
            "tab_index": 0,
            "element_path": "HTML[0]>BODY[0]>DIV[0]",
        }
    )

    result = hit_test_point(driver, Point(60, 35))

    assert result.interactive is True
    assert result.reason == "hit_interactive_element"


def test_hit_test_unavailable_is_machine_readable_failure():
    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        hit_test_mode="strict",
        auto_snap="nearest_clickable",
        hit_test_error=HitTestUnavailable("window metrics disagreed"),
    )

    assert result.success is False
    assert result.outcome_status == "fail_hit_test_unavailable"
    assert result.reason == "hit_test_unavailable"
    assert result.recommended_next_action == "inspect_page"


def test_disabled_label_is_not_snap_candidate():
    driver = FakeDriver(
        [
            {
                "tag": "LABEL",
                "text": "Disabled label",
                "rect": {"x": 10, "y": 20, "width": 120, "height": 24},
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
                "associated_control": {"disabled": True, "aria_disabled": False, "inert": False},
                "associated_control_type": "checkbox",
            },
            {
                "tag": "LABEL",
                "text": "Enabled label",
                "rect": {"x": 10, "y": 60, "width": 120, "height": 24},
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
                "associated_control": {"disabled": False, "aria_disabled": False, "inert": False},
                "associated_control_type": "checkbox",
            },
        ]
    )

    candidates = collect_snap_candidates(driver, "nearest_clickable", Point(20, 32))

    assert [(candidate.tag, candidate.text) for candidate in candidates] == [("LABEL", "Enabled label")]


def test_reverse_transform_fails_closed_when_window_metrics_disagree():
    metrics = WindowMetrics(
        window_x=100,
        window_y=200,
        screen_x=112,
        screen_y=200,
        inner_width=1280,
        inner_height=720,
        outer_width=1280,
        outer_height=860,
        scale=1.0,
        offset_left=0.0,
        offset_top=0.0,
    )

    with pytest.raises(HitTestUnavailable):
        screen_to_viewport_point(metrics, Point(325, 403))


def test_reverse_transform_fails_closed_when_hidpi_metrics_lack_visual_viewport_data():
    metrics = WindowMetrics(
        window_x=100,
        window_y=200,
        screen_x=100,
        screen_y=200,
        inner_width=1280,
        inner_height=720,
        outer_width=1280,
        outer_height=860,
        scale=1.0,
        offset_left=0.0,
        offset_top=0.0,
        device_pixel_ratio=2.0,
        has_visual_viewport=False,
    )

    with pytest.raises(HitTestUnavailable):
        screen_to_viewport_point(metrics, Point(325, 403))


def test_reverse_transform_allows_hidpi_when_visual_viewport_metrics_are_consistent():
    metrics = WindowMetrics(
        window_x=100,
        window_y=200,
        screen_x=100,
        screen_y=200,
        inner_width=1280,
        inner_height=720,
        outer_width=1280,
        outer_height=860,
        scale=1.0,
        offset_left=0.0,
        offset_top=0.0,
        device_pixel_ratio=2.0,
        has_visual_viewport=True,
    )

    point = screen_to_viewport_point(metrics, Point(325, 403))

    assert point == Point(225, 63)


def test_scoring_uses_fixed_ambiguity_threshold():
    viewport_point = Point(100, 100)
    winner = collect_snap_candidates(
        [
            {
                "tag": "A",
                "text": "Primary",
                "href": "/primary",
                "rect": {"x": 90, "y": 90, "width": 20, "height": 20},
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            },
            {
                "tag": "BUTTON",
                "text": "Secondary",
                "rect": {"x": 110, "y": 90, "width": 20, "height": 20},
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            },
        ],
        "nearest_clickable",
        viewport_point,
    )

    result = choose_candidate(winner, viewport_point)

    assert result.candidate is None
    assert result.reason == "ambiguous_target"


def test_text_input_snap_point_uses_left_bias_not_center():
    candidate = collect_snap_candidates(
        [
            {
                "tag": "INPUT",
                "text": "",
                "input_type": "text",
                "editable": True,
                "rect": {"x": 0, "y": 0, "width": 400, "height": 40},
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            }
        ],
        "nearest_interactive",
        Point(50, 20),
    )[0]

    point = snapped_click_point(candidate)

    assert point.x == pytest.approx(100)
    assert point.y == pytest.approx(20)


def test_detect_target_rejects_snap_when_resolved_point_fails_final_validation():
    candidate = collect_snap_candidates(
        [
            {
                "tag": "BUTTON",
                "text": "Continue",
                "rect": {"x": 40, "y": 30, "width": 80, "height": 20},
                "element_path": "HTML[0]>BODY[0]>DIV[0]>BUTTON[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            }
        ],
        "nearest_clickable",
        Point(20, 20),
    )

    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        raw_viewport_point=Point(20, 20),
        hit_test_mode="strict",
        auto_snap="nearest_clickable",
        hit_test_result=HitTestResult(
            viewport_point=Point(20, 20),
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidate,
        resolved_hit_test_result=HitTestResult(
            viewport_point=Point(80, 40),
            target_rect=Rect(0, 0, 1280, 720),
            tag="DIV",
            text="Overlay",
            interactive=False,
            reason="hit_non_interactive_element",
            reason_detail="final snapped point hit overlay",
        ),
    )

    assert result.success is False
    assert result.outcome_status == "fail_non_interactive"
    assert result.reason == "hit_non_interactive_element"


def test_detect_target_rejects_overlapping_interactive_element_at_resolved_point():
    candidate = collect_snap_candidates(
        [
            {
                "tag": "BUTTON",
                "text": "Continue",
                "rect": {"x": 40, "y": 30, "width": 80, "height": 20},
                "element_path": "HTML[0]>BODY[0]>DIV[0]>BUTTON[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            }
        ],
        "nearest_clickable",
        Point(20, 20),
    )

    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        raw_viewport_point=Point(20, 20),
        hit_test_mode="strict",
        auto_snap="nearest_clickable",
        hit_test_result=HitTestResult(
            viewport_point=Point(20, 20),
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidate,
        resolved_hit_test_result=HitTestResult(
            viewport_point=Point(80, 40),
            target_rect=Rect(40, 30, 80, 20),
            tag="BUTTON",
            text="Continue",
            interactive=True,
            reason="hit_interactive_element",
            reason_detail=None,
            element_path="HTML[0]>BODY[0]>DIV[0]>BUTTON[1]",
        ),
    )

    assert result.success is False
    assert result.outcome_status == "fail_non_interactive"
    assert result.reason == "intent_mismatch"


def test_click_target_returns_clicked_raw_when_validation_disabled():
    result = resolve_click_target(
        raw_point=Point(325, 403),
        pre_click_validate="off",
        auto_snap="off",
    )

    assert result.success is True
    assert result.outcome_status == "clicked_raw"
    assert result.recommended_next_action == "proceed"


def test_click_target_returns_clicked_snapped_after_validated_snap():
    candidate = collect_snap_candidates(
        [
            {
                "tag": "BUTTON",
                "text": "Continue",
                "rect": {"x": 40, "y": 30, "width": 80, "height": 20},
                "element_path": "HTML[0]>BODY[0]>DIV[0]>BUTTON[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            }
        ],
        "nearest_clickable",
        Point(20, 20),
    )

    result = resolve_click_target(
        raw_point=Point(325, 403),
        raw_viewport_point=Point(20, 20),
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        hit_test_result=HitTestResult(
            viewport_point=Point(20, 20),
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidate,
        resolved_hit_test_result=HitTestResult(
            viewport_point=Point(80, 40),
            target_rect=Rect(48, 34, 24, 8),
            tag="SPAN",
            text="Continue",
            interactive=True,
            reason="hit_interactive_element",
            reason_detail=None,
            element_path="HTML[0]>BODY[0]>DIV[0]>BUTTON[0]>SPAN[0]",
        ),
    )

    assert result.success is True
    assert result.outcome_status == "clicked_snapped"
    assert result.recommended_next_action == "proceed"


@pytest.mark.parametrize(
    (
        "raw_viewport_point",
        "snap_radius",
        "candidate_payloads",
        "expected_reason",
        "expected_reason_detail",
        "expected_next_action",
    ),
    [
        (
            Point(100, 100),
            96,
            [
                {
                    "tag": "A",
                    "text": "Primary",
                    "href": "/primary",
                    "rect": {"x": 90, "y": 90, "width": 20, "height": 20},
                    "element_path": "HTML[0]>BODY[0]>A[0]",
                    "visible": True,
                    "pointer_events": True,
                    "disabled": False,
                    "aria_disabled": False,
                    "inert": False,
                    "interactive": True,
                },
                {
                    "tag": "BUTTON",
                    "text": "Secondary",
                    "rect": {"x": 110, "y": 90, "width": 20, "height": 20},
                    "element_path": "HTML[0]>BODY[0]>BUTTON[0]",
                    "visible": True,
                    "pointer_events": True,
                    "disabled": False,
                    "aria_disabled": False,
                    "inert": False,
                    "interactive": True,
                },
            ],
            "ambiguous_target",
            "nearby candidates were too close to disambiguate safely",
            "switch_to_selector_click",
        ),
        (
            Point(20, 20),
            5,
            [
                {
                    "tag": "BUTTON",
                    "text": "Primary",
                    "rect": {"x": 40, "y": 30, "width": 30, "height": 20},
                    "element_path": "HTML[0]>BODY[0]>DIV[0]>BUTTON[0]",
                    "visible": True,
                    "pointer_events": True,
                    "disabled": False,
                    "aria_disabled": False,
                    "inert": False,
                    "interactive": True,
                },
                {
                    "tag": "A",
                    "text": "Secondary",
                    "href": "/secondary",
                    "rect": {"x": 74, "y": 30, "width": 30, "height": 20},
                    "element_path": "HTML[0]>BODY[0]>DIV[0]>A[0]",
                    "visible": True,
                    "pointer_events": True,
                    "disabled": False,
                    "aria_disabled": False,
                    "inert": False,
                    "interactive": True,
                },
            ],
            "no_candidate_within_radius",
            "no candidate fell within the configured snap radius",
            "retry_with_larger_radius",
        ),
    ],
)
def test_click_target_snap_failures_use_final_reason_detail(
    raw_viewport_point,
    snap_radius,
    candidate_payloads,
    expected_reason,
    expected_reason_detail,
    expected_next_action,
):
    candidates = collect_snap_candidates(candidate_payloads, "nearest_clickable", raw_viewport_point)

    result = resolve_click_target(
        raw_point=Point(325, 403),
        raw_viewport_point=raw_viewport_point,
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        snap_radius=snap_radius,
        hit_test_result=HitTestResult(
            viewport_point=raw_viewport_point,
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidates,
    )

    assert result.success is False
    assert result.outcome_status == "click_failed_precheck"
    assert result.reason == expected_reason
    assert result.reason_detail == expected_reason_detail
    assert result.recommended_next_action == expected_next_action


def test_warn_auto_snap_ambiguous_target_still_fails_precheck():
    raw_viewport_point = Point(100, 100)
    candidates = collect_snap_candidates(
        [
            {
                "tag": "A",
                "text": "Primary",
                "href": "/primary",
                "rect": {"x": 90, "y": 90, "width": 20, "height": 20},
                "element_path": "HTML[0]>BODY[0]>A[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            },
            {
                "tag": "BUTTON",
                "text": "Secondary",
                "rect": {"x": 110, "y": 90, "width": 20, "height": 20},
                "element_path": "HTML[0]>BODY[0]>BUTTON[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
            },
        ],
        "nearest_clickable",
        raw_viewport_point,
    )

    result = resolve_click_target(
        raw_point=Point(325, 403),
        raw_viewport_point=raw_viewport_point,
        pre_click_validate="warn",
        auto_snap="nearest_clickable",
        hit_test_result=HitTestResult(
            viewport_point=raw_viewport_point,
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidates,
    )

    assert result.success is False
    assert result.outcome_status == "click_failed_precheck"
    assert result.reason == "ambiguous_target"
    assert result.recommended_next_action == "switch_to_selector_click"


def test_intent_mismatch_is_explicit_when_interactive_hit_misses_bbox():
    result = resolve_detect_target(
        raw_point=Point(325, 403),
        raw_bbox=Rect(280, 393, 90, 20),
        raw_viewport_point=Point(500, 500),
        hit_test_mode="strict",
        auto_snap="off",
        hit_test_result=HitTestResult(
            viewport_point=Point(500, 500),
            target_rect=Rect(480, 480, 60, 24),
            tag="A",
            text="Far away link",
            interactive=True,
            reason="hit_interactive_element",
            reason_detail=None,
        ),
    )

    assert result.success is False
    assert result.outcome_status == "fail_non_interactive"
    assert result.reason == "intent_mismatch"
    assert result.recommended_next_action == "inspect_page"


def test_capture_postclick_snapshot_includes_expected_fields_and_truncates_content():
    driver = FakeDriver(
        {
            "url": "https://example.com/",
            "content": "abcdefghijklmnopqrstuvwxyz",
            "active_element": {"tag": "INPUT", "role": "textbox"},
            "visible_state": _visible_state(checked=True, subtree_digest="digest-after"),
        }
    )

    snapshot = capture_postclick_snapshot(driver, mode="auto", content_limit_chars=10, return_content=True)

    assert snapshot.url == "https://example.com/"
    assert snapshot.content_hash
    assert snapshot.content_summary == "abcdefghij"
    assert snapshot.content == "abcdefghij"
    assert snapshot.active_element_tag == "INPUT"
    assert snapshot.active_element_role == "textbox"
    assert snapshot.visible_state == _visible_state(checked=True, subtree_digest="digest-after")


def test_capture_postclick_snapshot_omits_full_content_when_not_requested():
    driver = FakeDriver(
        {
            "url": "https://example.com/",
            "content": "abcdefghijklmnopqrstuvwxyz",
            "active_element": {"tag": "BUTTON", "role": "button"},
            "visible_state": _visible_state(),
        }
    )

    snapshot = capture_postclick_snapshot(driver, mode="content", content_limit_chars=10)

    assert snapshot.content_summary == "abcdefghij"
    assert snapshot.content is None


def test_capture_postclick_snapshot_prefers_resolved_target_visible_state_over_active_element():
    driver = TargetAwareSnapshotDriver(
        active_state={
            "checked": False,
            "selected": False,
            "expanded": False,
            "pressed": False,
            "class_name": "focus-ring",
            "style": "outline:auto",
            "subtree_signature": "active-input-signature",
        },
        target_state={
            "checked": True,
            "selected": False,
            "expanded": False,
            "pressed": True,
            "class_name": "toggle is-active",
            "style": "display:block",
            "subtree_signature": "resolved-target-signature",
        },
    )

    snapshot = capture_postclick_snapshot(
        driver,
        mode="visible",
        content_limit_chars=10,
        target_element_path="HTML[0]>BODY[0]>BUTTON[0]",
    )

    assert driver.calls[-1] == ("HTML[0]>BODY[0]>BUTTON[0]",)
    assert snapshot.active_element_tag == "INPUT"
    assert snapshot.active_element_role == "textbox"
    assert snapshot.visible_state["checked"] is True
    assert snapshot.visible_state["pressed"] is True
    assert snapshot.visible_state["class_name"] == "toggle is-active"


def test_capture_postclick_snapshot_hashes_lightweight_subtree_signature():
    driver = TargetAwareSnapshotDriver(
        active_state={
            "checked": False,
            "selected": False,
            "expanded": False,
            "pressed": False,
            "class_name": "focus-ring",
            "style": "outline:auto",
            "subtree_signature": "active-input-signature",
        },
        target_state={
            "checked": False,
            "selected": False,
            "expanded": True,
            "pressed": False,
            "class_name": "accordion open",
            "style": "display:block",
            "subtree_signature": "resolved-target-signature",
        },
    )

    snapshot = capture_postclick_snapshot(
        driver,
        mode="visible",
        content_limit_chars=10,
        target_element_path="HTML[0]>BODY[0]>BUTTON[0]",
    )

    assert snapshot.visible_state["subtree_digest"] == hashlib.sha256(b"resolved-target-signature").hexdigest()


def test_visible_feedback_detects_label_surface_toggle_from_associated_control():
    before = capture_postclick_snapshot(
        FakeDriver(
            {
                "url": "https://example.com/",
                "content": "label toggle",
                "active_element": {"tag": "LABEL", "role": None, "path": "HTML[0]>BODY[0]>LABEL[0]"},
                "visible_state": {
                    "checked": None,
                    "selected": None,
                    "expanded": None,
                    "pressed": None,
                    "class_name": "consent-label",
                    "style": "display:block",
                    "subtree_signature": "label-before",
                    "associated_control": {
                        "checked": False,
                        "selected": None,
                        "expanded": None,
                        "pressed": None,
                    },
                },
            }
        ),
        mode="visible",
        content_limit_chars=10,
        target_element_path="HTML[0]>BODY[0]>LABEL[0]",
    )
    after = capture_postclick_snapshot(
        FakeDriver(
            {
                "url": "https://example.com/",
                "content": "label toggle",
                "active_element": {"tag": "LABEL", "role": None, "path": "HTML[0]>BODY[0]>LABEL[0]"},
                "visible_state": {
                    "checked": None,
                    "selected": None,
                    "expanded": None,
                    "pressed": None,
                    "class_name": "consent-label",
                    "style": "display:block",
                    "subtree_signature": "label-before",
                    "associated_control": {
                        "checked": True,
                        "selected": None,
                        "expanded": None,
                        "pressed": None,
                    },
                },
            }
        ),
        mode="visible",
        content_limit_chars=10,
        target_element_path="HTML[0]>BODY[0]>LABEL[0]",
    )

    result = diff_postclick_snapshot(before, after, mode="visible")

    assert result.status == "visible_state_changed"
    assert result.changed_fields == ("checked",)


def test_focus_feedback_detects_same_tag_role_transfer_between_distinct_elements():
    before = capture_postclick_snapshot(
        FakeDriver(
            {
                "url": "https://example.com/",
                "content": "focus transfer",
                "active_element": {
                    "tag": "INPUT",
                    "role": "textbox",
                    "path": "HTML[0]>BODY[0]>FORM[0]>INPUT[0]",
                },
                "visible_state": _visible_state(),
            }
        ),
        mode="focus",
        content_limit_chars=10,
    )
    after = capture_postclick_snapshot(
        FakeDriver(
            {
                "url": "https://example.com/",
                "content": "focus transfer",
                "active_element": {
                    "tag": "INPUT",
                    "role": "textbox",
                    "path": "HTML[0]>BODY[0]>FORM[0]>INPUT[1]",
                },
                "visible_state": _visible_state(),
            }
        ),
        mode="focus",
        content_limit_chars=10,
    )

    result = diff_postclick_snapshot(before, after, mode="focus")

    assert result.status == "focus_changed"


def test_diff_postclick_snapshot_reports_url_change():
    before = _postclick_snapshot()
    after = _postclick_snapshot(url="https://iana.org/")

    result = diff_postclick_snapshot(before, after, mode="url")

    assert result.status == "url_changed"
    assert result.before_url == "https://example.com/"
    assert result.after_url == "https://iana.org/"


def test_diff_postclick_snapshot_reports_content_change():
    before = _postclick_snapshot()
    after = _postclick_snapshot(content_hash="hash-after", content_summary="after summary")

    result = diff_postclick_snapshot(before, after, mode="content")

    assert result.status == "content_changed"
    assert result.before_content_hash == "hash-before"
    assert result.after_content_hash == "hash-after"


def test_diff_postclick_snapshot_reports_focus_change():
    before = _postclick_snapshot()
    after = _postclick_snapshot(active_element_tag="INPUT", active_element_role="textbox")

    result = diff_postclick_snapshot(before, after, mode="focus")

    assert result.status == "focus_changed"
    assert result.before_active_element_tag is None
    assert result.after_active_element_tag == "INPUT"


def test_visible_feedback_detects_checkbox_change():
    before = _postclick_snapshot(visible_state=_visible_state(checked=False))
    after = _postclick_snapshot(visible_state=_visible_state(checked=True))

    result = diff_postclick_snapshot(before, after, mode="visible")

    assert result.status == "visible_state_changed"
    assert result.changed_fields == ("checked",)


@pytest.mark.parametrize(
    ("field", "before_value", "after_value"),
    [
        ("selected", False, True),
        ("expanded", False, True),
        ("pressed", False, True),
        ("class_name", "toggle", "toggle is-active"),
        ("style", "display:block", "display:none"),
        ("subtree_digest", "digest-before", "digest-after"),
    ],
)
def test_visible_feedback_detects_other_visible_state_signals(field, before_value, after_value):
    before = _postclick_snapshot(visible_state=_visible_state(**{field: before_value}))
    after = _postclick_snapshot(visible_state=_visible_state(**{field: after_value}))

    result = diff_postclick_snapshot(before, after, mode="visible")

    assert result.status == "visible_state_changed"
    assert result.changed_fields == (field,)


@pytest.mark.parametrize(
    ("after", "expected_status"),
    [
        (
            _postclick_snapshot(
                url="https://iana.org/",
                content_hash="hash-after",
                content_summary="after summary",
                active_element_tag="INPUT",
                active_element_role="textbox",
                visible_state=_visible_state(checked=True),
            ),
            "url_changed",
        ),
        (
            _postclick_snapshot(
                content_hash="hash-after",
                content_summary="after summary",
                active_element_tag="INPUT",
                active_element_role="textbox",
                visible_state=_visible_state(checked=True),
            ),
            "content_changed",
        ),
        (
            _postclick_snapshot(
                active_element_tag="INPUT",
                active_element_role="textbox",
                visible_state=_visible_state(checked=True),
            ),
            "focus_changed",
        ),
        (_postclick_snapshot(visible_state=_visible_state(checked=True)), "visible_state_changed"),
    ],
)
def test_auto_feedback_prefers_url_then_content_then_focus_then_visible(after, expected_status):
    result = diff_postclick_snapshot(_postclick_snapshot(), after, mode="auto")

    assert result.status == expected_status
