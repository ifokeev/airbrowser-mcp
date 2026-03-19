from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

VISIBLE_STATE_FIELDS = (
    "checked",
    "selected",
    "expanded",
    "pressed",
    "class_name",
    "style",
    "subtree_digest",
)

POSTCLICK_SNAPSHOT_SCRIPT = r"""
const targetElementPath = arguments[0];
const active = document.activeElement && document.activeElement !== document.body ? document.activeElement : null;
const content = document.body ? (document.body.innerText || document.body.textContent || '') : '';
const normalizeText = (value, limit) =>
  String(value || '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, limit);
const elementPath = (node) => {
  const parts = [];
  for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; ) {
    let index = 0;
    for (let sibling = current; (sibling = sibling.previousElementSibling); ) {
      index += 1;
    }
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
const resolvePathChild = (current, tagName, childIndex) => {
  const roots = [];
  if (current && current.children) {
    roots.push(current);
  }
  if (current && current.shadowRoot && current.shadowRoot.children) {
    roots.push(current.shadowRoot);
  }
  for (const root of roots) {
    if (!root.children || childIndex >= root.children.length) {
      continue;
    }
    const next = root.children[childIndex];
    if (next && next.tagName === tagName) {
      return next;
    }
  }
  return null;
};
const resolveElementPath = (path) => {
  if (!path) {
    return null;
  }
  const segments = String(path).split('>');
  let current = null;
  for (let index = 0; index < segments.length; index += 1) {
    const match = /^([A-Z0-9_-]+)\[(\d+)\]$/.exec(segments[index]);
    if (!match) {
      return null;
    }
    const tagName = match[1];
    const childIndex = Number(match[2]);
    if (index === 0) {
      if (!document.documentElement || document.documentElement.tagName !== tagName || childIndex !== 0) {
        return null;
      }
      current = document.documentElement;
      continue;
    }
    const next = resolvePathChild(current, tagName, childIndex);
    if (!next) {
      return null;
    }
    current = next;
  }
  return current;
};
const buildSubtreeSignature = (element) => {
  if (!element) {
    return null;
  }
  const walker = document.createTreeWalker(element, NodeFilter.SHOW_ELEMENT);
  const tags = [];
  let descendantCount = 0;
  let node = walker.currentNode;
  while (node) {
    if (tags.length < 16) {
      tags.push(node.tagName || '');
    }
    descendantCount += 1;
    node = walker.nextNode();
  }
  return JSON.stringify({
    root: element.tagName || null,
    child_count: element.childElementCount || 0,
    descendant_count: descendantCount,
    tags,
    text: normalizeText(element.innerText || element.textContent || '', 120),
    value: 'value' in element ? normalizeText(element.value, 80) : null,
  });
};
const buildStateSignals = (element) => {
  if (!element) {
    return {
      checked: null,
      selected: null,
      expanded: null,
      pressed: null,
    };
  }
  const tagName = element.tagName || '';
  const inputType = (element.getAttribute('type') || '').toLowerCase();
  const hasFiles = tagName === 'INPUT' && inputType === 'file' && element.files;
  return {
    checked: typeof element.checked === 'boolean' ? element.checked : null,
    selected:
      typeof element.selected === 'boolean'
        ? element.selected
        : hasFiles
          ? element.files.length > 0
          : null,
    expanded:
      element.getAttribute('aria-expanded') === 'true' || element.open === true
        ? true
        : element.getAttribute('aria-expanded') === 'false'
          ? false
          : null,
    pressed:
      element.getAttribute('aria-pressed') === 'true' || element.pressed === true
        ? true
        : element.getAttribute('aria-pressed') === 'false'
          ? false
          : null,
  };
};
const buildVisibleState = (element) => {
  if (!element) {
    return {};
  }
  const className = typeof element.className === 'string' ? element.className : element.getAttribute('class') || '';
  const control = element.tagName === 'LABEL' && element.control ? element.control : null;
  const elementSignals = buildStateSignals(element);
  const controlSignals = buildStateSignals(control);
  return {
    checked: elementSignals.checked ?? controlSignals.checked,
    selected: elementSignals.selected ?? controlSignals.selected,
    expanded: elementSignals.expanded ?? controlSignals.expanded,
    pressed: elementSignals.pressed ?? controlSignals.pressed,
    class_name: className || '',
    style: element.getAttribute('style') || '',
    subtree_signature: buildSubtreeSignature(element),
    associated_control: control ? controlSignals : null,
  };
};
const tracked = resolveElementPath(targetElementPath) || active;
return {
  url: window.location.href || null,
  content,
  active_element: active
    ? {
        tag: active.tagName || null,
        role: active.getAttribute('role') || null,
        path: elementPath(active),
      }
    : null,
  visible_state: buildVisibleState(tracked),
};
"""


@dataclass(frozen=True)
class PostClickSnapshot:
    url: str | None
    content_hash: str | None
    content_summary: str | None
    active_element_tag: str | None
    active_element_role: str | None
    visible_state: dict[str, Any]
    active_element_path: str | None = None
    content: str | None = None


@dataclass(frozen=True)
class PostClickResult:
    status: str
    before_url: str | None = None
    after_url: str | None = None
    before_content_hash: str | None = None
    after_content_hash: str | None = None
    before_content_summary: str | None = None
    after_content_summary: str | None = None
    before_content: str | None = None
    after_content: str | None = None
    before_active_element_tag: str | None = None
    after_active_element_tag: str | None = None
    before_active_element_role: str | None = None
    after_active_element_role: str | None = None
    before_active_element_path: str | None = None
    after_active_element_path: str | None = None
    changed_fields: tuple[str, ...] = ()


def capture_postclick_snapshot(
    driver: Any,
    mode: str,
    content_limit_chars: int,
    return_content: bool = False,
    target_element_path: str | None = None,
) -> PostClickSnapshot:
    if mode == "none":
        return _empty_snapshot()

    payload = driver.execute_script(POSTCLICK_SNAPSHOT_SCRIPT, target_element_path) or {}
    return _snapshot_from_payload(payload, content_limit_chars=content_limit_chars, return_content=return_content)


def diff_postclick_snapshot(
    before: PostClickSnapshot,
    after: PostClickSnapshot,
    mode: str,
) -> PostClickResult:
    if mode == "auto":
        for candidate_mode in ("url", "content", "focus", "visible"):
            result = diff_postclick_snapshot(before, after, candidate_mode)
            if result.status != "no_observable_change":
                return result
        return PostClickResult(status="no_observable_change")

    if mode == "url":
        if before.url != after.url:
            return PostClickResult(status="url_changed", before_url=before.url, after_url=after.url)
        return PostClickResult(status="no_observable_change", before_url=before.url, after_url=after.url)

    if mode == "content":
        if before.content_hash != after.content_hash:
            return PostClickResult(
                status="content_changed",
                before_content_hash=before.content_hash,
                after_content_hash=after.content_hash,
                before_content_summary=before.content_summary,
                after_content_summary=after.content_summary,
                before_content=before.content,
                after_content=after.content,
            )
        return PostClickResult(
            status="no_observable_change",
            before_content_hash=before.content_hash,
            after_content_hash=after.content_hash,
            before_content_summary=before.content_summary,
            after_content_summary=after.content_summary,
            before_content=before.content,
            after_content=after.content,
        )

    if mode == "focus":
        before_focus = (before.active_element_path, before.active_element_tag, before.active_element_role)
        after_focus = (after.active_element_path, after.active_element_tag, after.active_element_role)
        if before_focus != after_focus:
            return PostClickResult(
                status="focus_changed",
                before_active_element_tag=before.active_element_tag,
                after_active_element_tag=after.active_element_tag,
                before_active_element_role=before.active_element_role,
                after_active_element_role=after.active_element_role,
                before_active_element_path=before.active_element_path,
                after_active_element_path=after.active_element_path,
            )
        return PostClickResult(
            status="no_observable_change",
            before_active_element_tag=before.active_element_tag,
            after_active_element_tag=after.active_element_tag,
            before_active_element_role=before.active_element_role,
            after_active_element_role=after.active_element_role,
            before_active_element_path=before.active_element_path,
            after_active_element_path=after.active_element_path,
        )

    if mode == "visible":
        changed_fields = tuple(
            field for field in VISIBLE_STATE_FIELDS if before.visible_state.get(field) != after.visible_state.get(field)
        )
        if changed_fields:
            return PostClickResult(status="visible_state_changed", changed_fields=changed_fields)
        return PostClickResult(status="no_observable_change")

    raise ValueError(f"unsupported post-click feedback mode: {mode}")


def _snapshot_from_payload(
    payload: Mapping[str, Any],
    *,
    content_limit_chars: int,
    return_content: bool,
) -> PostClickSnapshot:
    raw_content = payload.get("content")
    content = None if raw_content is None else str(raw_content)
    truncated_content = _truncate_content(content, content_limit_chars)
    active_element = payload.get("active_element") or {}

    return PostClickSnapshot(
        url=_coerce_optional_str(payload.get("url")),
        content_hash=_content_hash(content),
        content_summary=truncated_content,
        active_element_tag=_coerce_optional_str(active_element.get("tag") or payload.get("active_element_tag")),
        active_element_role=_coerce_optional_str(active_element.get("role") or payload.get("active_element_role")),
        visible_state=_normalize_visible_state(payload.get("visible_state")),
        active_element_path=_coerce_optional_str(active_element.get("path") or payload.get("active_element_path")),
        content=truncated_content if return_content else None,
    )


def _content_hash(content: str | None) -> str | None:
    if content is None:
        return None
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _truncate_content(content: str | None, content_limit_chars: int) -> str | None:
    if content is None:
        return None
    if content_limit_chars <= 0:
        return ""
    return content[:content_limit_chars]


def _normalize_visible_state(payload: Any) -> dict[str, Any]:
    state = payload if isinstance(payload, Mapping) else {}
    raw_associated_control = state.get("associated_control")
    associated_control: Mapping[str, Any] = (
        raw_associated_control if isinstance(raw_associated_control, Mapping) else {}
    )
    normalized = {
        "checked": _state_signal(state.get("checked"), associated_control.get("checked")),
        "selected": _state_signal(state.get("selected"), associated_control.get("selected")),
        "expanded": _state_signal(state.get("expanded"), associated_control.get("expanded")),
        "pressed": _state_signal(state.get("pressed"), associated_control.get("pressed")),
        "class_name": state.get("class_name"),
        "style": state.get("style"),
    }
    normalized["subtree_digest"] = _subtree_digest(state)
    return normalized


def _state_signal(primary: Any, fallback: Any) -> Any:
    return primary if primary is not None else fallback


def _subtree_digest(state: Mapping[str, Any]) -> str | None:
    digest = state.get("subtree_digest")
    if digest is not None:
        return str(digest)
    signature = state.get("subtree_signature")
    if signature is None:
        return None
    return hashlib.sha256(str(signature).encode("utf-8")).hexdigest()


def _coerce_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text or None


def _empty_snapshot() -> PostClickSnapshot:
    return PostClickSnapshot(
        url=None,
        content_hash=None,
        content_summary=None,
        active_element_tag=None,
        active_element_role=None,
        visible_state=_normalize_visible_state({}),
        content=None,
    )


__all__ = [
    "POSTCLICK_SNAPSHOT_SCRIPT",
    "PostClickResult",
    "PostClickSnapshot",
    "VISIBLE_STATE_FIELDS",
    "capture_postclick_snapshot",
    "diff_postclick_snapshot",
]
