"""Action enums for combined operations."""

from enum import Enum


class HistoryAction(str, Enum):
    """Actions for browser history navigation."""

    BACK = "back"
    FORWARD = "forward"
    REFRESH = "refresh"


class ElementCheck(str, Enum):
    """Check types for element state."""

    EXISTS = "exists"
    VISIBLE = "visible"


class WaitUntil(str, Enum):
    """Wait conditions for elements."""

    VISIBLE = "visible"
    HIDDEN = "hidden"


class ElementDataType(str, Enum):
    """Types of element data to retrieve."""

    TEXT = "text"
    ATTRIBUTE = "attribute"
    PROPERTY = "property"


class MouseAction(str, Enum):
    """Mouse actions."""

    HOVER = "hover"
    DRAG = "drag"


class SelectAction(str, Enum):
    """Select dropdown actions."""

    SELECT = "select"
    OPTIONS = "options"


class BrowsersAction(str, Enum):
    """Admin browser actions."""

    LIST = "list"
    INFO = "info"
    CLOSE_ALL = "close_all"


class LogAction(str, Enum):
    """Actions for log management."""

    GET = "get"
    CLEAR = "clear"


class TabAction(str, Enum):
    """Actions for tab management."""

    LIST = "list"
    NEW = "new"
    SWITCH = "switch"
    CLOSE = "close"
    CURRENT = "current"


class DialogAction(str, Enum):
    """Actions for dialog handling."""

    GET = "get"
    ACCEPT = "accept"
    DISMISS = "dismiss"


class EmulateAction(str, Enum):
    """Actions for device emulation."""

    SET = "set"
    CLEAR = "clear"
    LIST_DEVICES = "list_devices"


class PerformanceAction(str, Enum):
    """Actions for performance tracing."""

    START_TRACE = "start_trace"
    STOP_TRACE = "stop_trace"
    METRICS = "metrics"
    ANALYZE = "analyze"
