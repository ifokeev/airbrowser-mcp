"""Browser operations modules."""

from .debug import DebugOperations
from .dialogs import DialogOperations
from .elements import ElementOperations
from .emulation import EmulationOperations
from .enums import (
    BrowsersAction,
    DialogAction,
    ElementCheck,
    ElementDataType,
    EmulateAction,
    HistoryAction,
    LogAction,
    MouseAction,
    PerformanceAction,
    SelectAction,
    TabAction,
    WaitUntil,
)
from .gui import GuiOperations
from .lifecycle import LifecycleOperations
from .navigation import NavigationOperations
from .page import PageOperations
from .performance import PerformanceOperations
from .pool import PoolOperations
from .tabs import TabOperations
from .vision import VisionOperations

__all__ = [
    # Operations
    "LifecycleOperations",
    "NavigationOperations",
    "ElementOperations",
    "GuiOperations",
    "VisionOperations",
    "PageOperations",
    "DebugOperations",
    "PoolOperations",
    "TabOperations",
    "DialogOperations",
    "EmulationOperations",
    "PerformanceOperations",
    # Enums
    "BrowsersAction",
    "DialogAction",
    "ElementCheck",
    "ElementDataType",
    "EmulateAction",
    "HistoryAction",
    "LogAction",
    "MouseAction",
    "PerformanceAction",
    "SelectAction",
    "TabAction",
    "WaitUntil",
]
