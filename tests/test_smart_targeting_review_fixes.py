from __future__ import annotations

from airbrowser.server.browser.smart_targeting import (
    HitTestResult,
    Point,
    Rect,
    collect_snap_candidates,
    hit_test_point,
    resolve_click_target,
)


class FakeDriver:
    def __init__(self, payload):
        self.payload = payload

    def execute_script(self, script, *args):
        return self.payload


def _label_hit_payload(*, element_path: str = "HTML[0]>BODY[0]>LABEL[0]", text: str = "Accept terms") -> dict:
    return {
        "viewport_point": {"x": 72, "y": 48},
        "target_rect": {"x": 20, "y": 32, "width": 140, "height": 32},
        "tag": "LABEL",
        "text": text,
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
        "tab_index": None,
        "element_path": element_path,
        "associated_control": {"disabled": False, "aria_disabled": False, "inert": False},
        "associated_control_type": "checkbox",
    }


def test_click_target_accepts_exact_label_surface_hit():
    hit = hit_test_point(FakeDriver(_label_hit_payload()), Point(72, 48))

    result = resolve_click_target(
        raw_point=Point(325, 403),
        raw_viewport_point=Point(72, 48),
        pre_click_validate="strict",
        auto_snap="off",
        hit_test_result=hit,
    )

    assert result.success is True
    assert result.outcome_status == "clicked_exact"
    assert result.reason == "hit_interactive_element"


def test_click_target_accepts_snapped_label_surface_hit():
    candidate = collect_snap_candidates(
        [
            {
                "tag": "LABEL",
                "text": "Accept terms",
                "rect": {"x": 20, "y": 32, "width": 140, "height": 32},
                "element_path": "HTML[0]>BODY[0]>LABEL[0]",
                "visible": True,
                "pointer_events": True,
                "disabled": False,
                "aria_disabled": False,
                "inert": False,
                "interactive": True,
                "associated_control": {"disabled": False, "aria_disabled": False, "inert": False},
                "associated_control_type": "checkbox",
            }
        ],
        "nearest_clickable",
        Point(10, 10),
    )
    resolved_hit = hit_test_point(FakeDriver(_label_hit_payload()), Point(90, 48))

    result = resolve_click_target(
        raw_point=Point(325, 403),
        raw_viewport_point=Point(10, 10),
        pre_click_validate="strict",
        auto_snap="nearest_clickable",
        hit_test_result=HitTestResult(
            viewport_point=Point(10, 10),
            target_rect=Rect(0, 0, 1280, 720),
            tag="HTML",
            text="",
            interactive=False,
            reason="hit_html_root",
            reason_detail="hit non-interactive root element",
        ),
        snap_candidates=candidate,
        resolved_hit_test_result=resolved_hit,
    )

    assert result.success is True
    assert result.outcome_status == "clicked_snapped"
    assert result.snap_candidate is not None
    assert result.snap_candidate.tag == "LABEL"
