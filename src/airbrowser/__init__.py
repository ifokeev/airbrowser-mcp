"""Airbrowser Python package."""

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

__all__ = ["__version__"]


def _get_version() -> str:
    """Get version from package metadata or pyproject.toml."""
    try:
        return version("airbrowser-mcp")
    except PackageNotFoundError:
        pass

    # Fallback: read from pyproject.toml
    try:
        pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
            if match:
                return match.group(1)
    except Exception:
        pass

    return "0.0.0"


__version__ = _get_version()
