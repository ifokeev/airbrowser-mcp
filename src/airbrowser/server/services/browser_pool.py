#!/usr/bin/env python3
"""Adapter that talks to `browser_service` via file-based IPC."""

import logging
import os
import shutil
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from ..ipc.client import BrowserIPCClient
from ..models import ActionResult, BrowserAction, BrowserConfig, BrowserInfo

logger = logging.getLogger(__name__)


class BrowserInstance:
    """Wrapper for browser instance info"""

    def __init__(self, browser_id: str, config: BrowserConfig, status: str = "ready"):
        self.id = browser_id
        self.config = config
        self.status = status
        self.created_at = time.time()
        self.error_message: str | None = None
        self.session_id: str | None = None

    def to_info(self) -> BrowserInfo:
        from datetime import datetime

        from ..models import BrowserStatus

        # Convert status string to BrowserStatus enum
        try:
            status_enum = BrowserStatus(self.status)
        except:
            status_enum = BrowserStatus.READY

        return BrowserInfo(
            id=self.id,
            status=status_enum,
            config=self.config,
            created_at=datetime.fromtimestamp(self.created_at),
            last_activity=datetime.fromtimestamp(self.created_at),
            error_message=self.error_message,
            session_id=self.session_id,
        )

    def to_dict(self) -> dict:
        return self.to_info().to_dict()


class BrowserPoolAdapter:
    """Adapter to communicate with browser service via IPC"""

    def __init__(self, max_browsers: int = 10):
        self.client = BrowserIPCClient()
        self.ipc_client = self.client  # Alias for API compatibility
        self.max_browsers = max_browsers
        self.browser_configs: dict[str, BrowserConfig] = {}
        self.browser_instances: dict[str, BrowserInstance] = {}

        # Profile tracking
        self.active_profiles: dict[str, str] = {}  # profile_name -> browser_id
        self.profiles_dir = Path(os.environ.get("PROFILES_DIR", "/app/browser-profiles"))
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger.info("BrowserPoolAdapter initialized with IPC client")

    def create_browser(self, config: BrowserConfig | None = None) -> str:
        """Create a new browser with the given configuration (synchronous)"""
        if config is None:
            config = BrowserConfig()

        profile_name = config.profile_name

        # Check if profile is already in use
        if profile_name and profile_name in self.active_profiles:
            raise ValueError(f"Profile '{profile_name}' is already in use by browser {self.active_profiles[profile_name]}")

        logger.info(f"Creating browser with config: proxy={config.proxy}, profile={profile_name}")

        # Convert BrowserConfig to dict for subprocess manager
        config_dict = {
            "profile_name": profile_name,
            "proxy": config.proxy,
            "uc": bool(getattr(config, "uc", True)),
            "window_size": list(config.window_size) if isinstance(config.window_size, tuple) else config.window_size,
            "disable_images": config.disable_images,
            "disable_gpu": config.disable_gpu,
            "user_agent": config.user_agent,
        }

        # Generate browser_id upfront so we can track it immediately
        browser_id = str(uuid.uuid4())

        # Store config and instance BEFORE IPC call (so it appears in list immediately)
        self.browser_configs[browser_id] = config
        instance = BrowserInstance(browser_id, config)
        instance.status = "creating"
        self.browser_instances[browser_id] = instance

        # Track active profile
        if profile_name:
            self.active_profiles[profile_name] = browser_id

        try:
            # Create browser through IPC (blocking - waits for browser to be ready)
            self.client.create_browser(config_dict, browser_id=browser_id)
            instance.status = "ready"
        except Exception as e:
            instance.status = "error"
            instance.error_message = str(e)
            # Clean up on failure
            del self.browser_instances[browser_id]
            del self.browser_configs[browser_id]
            if profile_name and profile_name in self.active_profiles:
                del self.active_profiles[profile_name]
            raise

        return browser_id

    def get_browser_status(self, browser_id: str) -> dict[str, Any]:
        """Get the status of a specific browser"""
        try:
            # Get status from service
            response = self.client.get_browser_status(browser_id)

            # Update local instance status if successful
            if response.get("status") == "success" and browser_id in self.browser_instances:
                self.browser_instances[browser_id].status = response.get("browser_status", "unknown")

            return response
        except Exception as e:
            logger.error(f"Error getting browser status: {e}")
            return {"status": "error", "message": str(e)}

    def get_browser(self, browser_id: str) -> BrowserInstance | None:
        """Get browser instance info"""
        return self.browser_instances.get(browser_id)

    def close_browser(self, browser_id: str) -> bool:
        """Close a browser"""
        if browser_id in self.browser_instances:
            # Release profile lock
            for profile_name, bid in list(self.active_profiles.items()):
                if bid == browser_id:
                    del self.active_profiles[profile_name]
                    logger.info(f"Released profile lock for '{profile_name}'")
                    break

            result = self.client.close_browser(browser_id)
            if result:
                del self.browser_instances[browser_id]
                del self.browser_configs[browser_id]
            return result
        return False

    def execute_action(self, browser_id: str, action: BrowserAction) -> ActionResult:
        """Execute an action on a browser"""
        try:
            logger.info(f"Executing action {action.action} on browser {browser_id}")

            if action.action == "navigate":
                # Use timeout from action or default to 60 seconds for navigation
                nav_timeout = action.timeout if hasattr(action, "timeout") and action.timeout else 60
                response = self.client.execute_command(browser_id, "navigate", timeout=nav_timeout, url=action.url)
            elif action.action == "click":
                response = self.client.execute_command(
                    browser_id,
                    "click",
                    selector=action.selector,
                    by=getattr(action, "by", "css"),
                    timeout=action.timeout,
                )
            elif action.action == "type":
                response = self.client.execute_command(
                    browser_id,
                    "type",
                    selector=action.selector,
                    text=action.text,
                    by=getattr(action, "by", "css"),
                    timeout=action.timeout,
                )
            elif action.action == "wait":
                response = self.client.execute_command(
                    browser_id,
                    "wait",
                    selector=action.selector,
                    timeout=action.timeout,
                    by=getattr(action, "by", "css"),
                )
            elif action.action == "screenshot":
                # Save screenshot to a writable directory and return URL
                # Prefer env var SCREENSHOTS_DIR, else default to /tmp/screenshots
                base_dir = os.environ.get("SCREENSHOTS_DIR", "/tmp/screenshots")
                screenshots_dir = Path(base_dir)
                screenshots_dir.mkdir(parents=True, exist_ok=True)
                filename = f"{browser_id}_{int(time.time())}.png"
                screenshot_path = screenshots_dir / filename

                response = self.client.execute_command(browser_id, "screenshot", filename=str(screenshot_path))

                if response.get("status") == "success" and screenshot_path.exists():
                    # Map to nginx-served URL
                    screenshot_url = f"/screenshots/{filename}"
                    response["screenshot_url"] = screenshot_url
                    response["screenshot_path"] = screenshot_url

            elif action.action == "get_text":
                response = self.client.execute_command(
                    browser_id,
                    "get_text",
                    selector=action.selector,
                    by=getattr(action, "by", "css"),
                    timeout=action.timeout,
                )

            elif action.action == "execute_script":
                response = self.client.execute_command(
                    browser_id, "execute_script", timeout=action.timeout, script=action.text
                )

            elif action.action == "get_url":
                response = self.client.execute_command(browser_id, "url", timeout=action.timeout)

            elif action.action == "get_content":
                response = self.client.execute_command(browser_id, "get_content")

            elif action.action == "get_console_logs":
                # Best-effort: relies on underlying driver exposing Chrome logs
                response = self.client.execute_command(
                    browser_id,
                    "get_console_logs",
                    timeout=action.timeout,
                    limit=(action.options or {}).get("limit", 200),
                )

            elif action.action == "clear_console_logs":
                response = self.client.execute_command(
                    browser_id,
                    "clear_console_logs",
                    timeout=action.timeout,
                )

            elif action.action == "get_performance_logs":
                response = self.client.execute_command(
                    browser_id,
                    "get_performance_logs",
                    timeout=action.timeout,
                    limit=(action.options or {}).get("limit", 500),
                )

            elif action.action == "clear_performance_logs":
                response = self.client.execute_command(
                    browser_id,
                    "clear_performance_logs",
                    timeout=action.timeout,
                )

            elif action.action == "click_if_visible":
                response = self.client.execute_command(browser_id, "click_if_visible", selector=action.selector)

            elif action.action == "wait_for_element_not_visible":
                response = self.client.execute_command(
                    browser_id, "wait_for_element_not_visible", selector=action.selector, timeout=action.timeout
                )

            elif action.action == "press_keys":
                response = self.client.execute_command(
                    browser_id, "press_keys", selector=action.selector, text=action.text,
                    by=getattr(action, "by", "css")
                )

            elif action.action == "gui_click":
                # GUI-based click using screen coordinates computed via CDP
                timeframe = action.options.get("timeframe", 0.25) if action.options else 0.25
                fx = action.options.get("fx") if action.options else None
                fy = action.options.get("fy") if action.options else None
                response = self.client.execute_command(
                    browser_id,
                    "gui_click",
                    selector=action.selector,
                    timeframe=timeframe,
                    fx=fx,
                    fy=fy,
                )

            elif action.action == "gui_click_xy":
                # Absolute screen-coordinate click via PyAutoGUI
                x = action.options.get("x") if action.options else None
                y = action.options.get("y") if action.options else None
                timeframe = action.options.get("timeframe", 0.25) if action.options else 0.25
                response = self.client.execute_command(browser_id, "gui_click_xy", x=x, y=y, timeframe=timeframe)

            elif action.action == "gui_type_xy":
                # Click at coordinates then type text via PyAutoGUI
                x = action.options.get("x") if action.options else None
                y = action.options.get("y") if action.options else None
                text = action.options.get("text") if action.options else None
                timeframe = action.options.get("timeframe", 0.25) if action.options else 0.25
                response = self.client.execute_command(
                    browser_id, "gui_type_xy", x=x, y=y, text=text, timeframe=timeframe
                )

            elif action.action == "gui_hover_xy":
                # Hover at coordinates via PyAutoGUI
                x = action.options.get("x") if action.options else None
                y = action.options.get("y") if action.options else None
                timeframe = action.options.get("timeframe", 0.25) if action.options else 0.25
                response = self.client.execute_command(browser_id, "gui_hover_xy", x=x, y=y, timeframe=timeframe)

            elif action.action == "gui_press_keys_xy":
                # Press keys at coordinates via PyAutoGUI
                x = action.options.get("x") if action.options else None
                y = action.options.get("y") if action.options else None
                keys = action.options.get("keys") if action.options else None
                timeframe = action.options.get("timeframe", 0.25) if action.options else 0.25
                response = self.client.execute_command(
                    browser_id, "gui_press_keys_xy", x=x, y=y, keys=keys, timeframe=timeframe
                )

            elif action.action == "detect_coordinates":
                # Detect element coordinates using vision models
                prompt = action.options.get("prompt") if action.options else None
                # Only pass fx/fy if explicitly set - otherwise let vision handler auto-bias
                kwargs = {"prompt": prompt}
                if action.options:
                    if "fx" in action.options:
                        kwargs["fx"] = action.options["fx"]
                    if "fy" in action.options:
                        kwargs["fy"] = action.options["fy"]
                response = self.client.execute_command(browser_id, "detect_coordinates", **kwargs)

            elif action.action == "what_is_visible":
                # Comprehensive page state analysis - what's visible on the current page
                response = self.client.execute_command(browser_id, "what_is_visible")

            # Tab operations
            elif action.action == "list_tabs":
                response = self.client.execute_command(browser_id, "list_tabs")

            elif action.action == "new_tab":
                url = action.options.get("url") if action.options else None
                response = self.client.execute_command(browser_id, "new_tab", url=url)

            elif action.action == "switch_tab":
                index = action.options.get("index") if action.options else None
                handle = action.options.get("handle") if action.options else None
                response = self.client.execute_command(browser_id, "switch_tab", index=index, handle=handle)

            elif action.action == "close_tab":
                index = action.options.get("index") if action.options else None
                handle = action.options.get("handle") if action.options else None
                response = self.client.execute_command(browser_id, "close_tab", index=index, handle=handle)

            elif action.action == "get_current_tab":
                response = self.client.execute_command(browser_id, "get_current_tab")

            # Input automation
            elif action.action == "hover":
                response = self.client.execute_command(
                    browser_id,
                    "hover",
                    selector=action.selector,
                    by=getattr(action, "by", "css"),
                )

            elif action.action == "drag":
                source = action.options.get("source") if action.options else None
                target = action.options.get("target") if action.options else None
                response = self.client.execute_command(
                    browser_id,
                    "drag",
                    source=source,
                    target=target,
                    by=getattr(action, "by", "css"),
                )

            elif action.action == "fill_form":
                fields = action.options.get("fields") if action.options else []
                response = self.client.execute_command(
                    browser_id,
                    "fill_form",
                    fields=fields,
                    by=getattr(action, "by", "css"),
                )

            elif action.action == "upload_file":
                file_path = action.options.get("file_path") if action.options else None
                response = self.client.execute_command(
                    browser_id,
                    "upload_file",
                    selector=action.selector,
                    file_path=file_path,
                    by=getattr(action, "by", "css"),
                )

            # Scroll operations
            elif action.action == "scroll":
                opts = action.options or {}
                response = self.client.execute_command(
                    browser_id,
                    "scroll",
                    selector=action.selector,
                    x=opts.get("x"),
                    y=opts.get("y"),
                    delta_x=opts.get("delta_x"),
                    delta_y=opts.get("delta_y"),
                    behavior=opts.get("behavior", "smooth"),
                    by=getattr(action, "by", "css"),
                )

            elif action.action == "scroll_by":
                opts = action.options or {}
                response = self.client.execute_command(
                    browser_id,
                    "scroll_by",
                    delta_x=opts.get("delta_x", 0),
                    delta_y=opts.get("delta_y", 0),
                    behavior=opts.get("behavior", "smooth"),
                )

            # Dialog handling
            elif action.action == "handle_dialog":
                dialog_action = action.options.get("action", "accept") if action.options else "accept"
                dialog_text = action.options.get("text") if action.options else None
                response = self.client.execute_command(
                    browser_id,
                    "handle_dialog",
                    action=dialog_action,
                    text=dialog_text,
                )

            elif action.action == "get_dialog":
                response = self.client.execute_command(browser_id, "get_dialog")

            # Page operations
            elif action.action == "resize":
                width = action.options.get("width") if action.options else None
                height = action.options.get("height") if action.options else None
                response = self.client.execute_command(browser_id, "resize", width=width, height=height)

            elif action.action == "snapshot":
                snapshot_type = action.options.get("type", "dom") if action.options else "dom"
                response = self.client.execute_command(browser_id, "snapshot", type=snapshot_type)

            # Emulation
            elif action.action == "emulate":
                device = action.options.get("device") if action.options else None
                width = action.options.get("width") if action.options else None
                height = action.options.get("height") if action.options else None
                device_scale_factor = action.options.get("device_scale_factor") if action.options else None
                mobile = action.options.get("mobile") if action.options else None
                user_agent = action.options.get("user_agent") if action.options else None
                response = self.client.execute_command(
                    browser_id,
                    "emulate",
                    device=device,
                    width=width,
                    height=height,
                    device_scale_factor=device_scale_factor,
                    mobile=mobile,
                    user_agent=user_agent,
                )

            elif action.action == "list_devices":
                response = self.client.execute_command(browser_id, "list_devices")

            elif action.action == "clear_emulation":
                response = self.client.execute_command(browser_id, "clear_emulation")

            # Performance
            elif action.action == "start_trace":
                categories = action.options.get("categories") if action.options else None
                response = self.client.execute_command(browser_id, "start_trace", categories=categories)

            elif action.action == "stop_trace":
                response = self.client.execute_command(browser_id, "stop_trace")

            elif action.action == "get_metrics":
                response = self.client.execute_command(browser_id, "get_metrics")

            elif action.action == "analyze_insight":
                response = self.client.execute_command(browser_id, "analyze_insight")

            # Navigation history
            elif action.action == "go_back":
                response = self.client.execute_command(browser_id, "go_back")

            elif action.action == "go_forward":
                response = self.client.execute_command(browser_id, "go_forward")

            elif action.action == "refresh":
                response = self.client.execute_command(browser_id, "refresh")

            elif action.action == "get_url":
                response = self.client.execute_command(browser_id, "get_url")

            # Element checks
            elif action.action == "find_element":
                response = self.client.execute_command(
                    browser_id,
                    "find_element",
                    selector=action.selector,
                    by=getattr(action, "by", "css"),
                )

            elif action.action == "is_visible":
                response = self.client.execute_command(
                    browser_id,
                    "is_visible",
                    selector=action.selector,
                    by=getattr(action, "by", "css"),
                )

            else:
                response = {"status": "error", "message": f"Unknown action: {action.action}"}

            # Convert response to ActionResult
            if response.get("status") == "success":
                return ActionResult(
                    success=True,
                    message=response.get("message", "Action completed successfully"),
                    data=response,
                    screenshot_path=response.get("screenshot_url") if isinstance(response, dict) else None,
                )
            else:
                # Include more details in error message
                error_details = response.get("error", response.get("message", "Action failed"))
                logger.error(f"Action failed for browser {browser_id}: {error_details}")
                logger.error(f"Full response: {response}")
                return ActionResult(success=False, message=error_details, data=response)

        except Exception as e:
            return ActionResult(success=False, message=str(e))

    def list_browsers(self) -> list[BrowserInfo]:
        """List all browsers - syncs with IPC service"""
        # Get actual browser list from IPC service
        service_status = self.client.get_status()
        service_browsers = service_status.get("browsers", {})

        # Sync local cache with service
        service_ids = set(service_browsers.keys())
        local_ids = set(self.browser_instances.keys())

        # Add missing browsers to local cache
        for browser_id in service_ids - local_ids:
            browser_data = service_browsers[browser_id]
            # Create a minimal BrowserInstance for browsers created outside this session
            config = self.browser_configs.get(browser_id, BrowserConfig())
            instance = BrowserInstance(browser_id, config)
            instance.status = browser_data.get("status", "unknown")
            instance.session_id = browser_data.get("session_id")
            instance.created_at = browser_data.get("created_at", time.time())
            self.browser_instances[browser_id] = instance

        # Remove stale browsers from local cache (but keep "creating" ones)
        for browser_id in local_ids - service_ids:
            instance = self.browser_instances.get(browser_id)
            # Keep browsers that are still being created
            if instance and instance.status == "creating":
                continue
            del self.browser_instances[browser_id]
            if browser_id in self.browser_configs:
                del self.browser_configs[browser_id]

        # Build return list
        browser_list = []
        for _browser_id, instance in self.browser_instances.items():
            browser_list.append(instance.to_info())
        return browser_list

    def close_all_browsers(self):
        """Close all browsers"""
        # Close each browser individually via IPC
        for browser_id in list(self.browser_instances.keys()):
            try:
                self.client.close_browser(browser_id)
            except:
                pass
        self.browser_instances.clear()
        self.browser_configs.clear()
        self.active_profiles.clear()

    def get_status(self) -> dict[str, Any]:
        """Get pool status"""
        service_status = self.client.get_status()

        # Calculate memory usage (rough estimate)
        memory_mb = len(self.browser_instances) * 200  # Estimate 200MB per browser

        return {
            "healthy": service_status.get("status") == "success",
            "total_browsers": service_status.get("total_browsers", 0),
            "active_browsers": service_status.get("active_browsers", 0),
            "available_browsers": service_status.get("max_browsers", 0) - service_status.get("total_browsers", 0),
            "memory_usage_mb": memory_mb,
            "cpu_usage_percent": 0,  # Would need psutil for real CPU usage
            "uptime_seconds": 0,  # Would need to track start time
        }

    # Profile management methods

    def list_profiles(self) -> list[dict[str, Any]]:
        """List all available browser profiles."""
        profiles = []
        if self.profiles_dir.exists():
            for profile_path in self.profiles_dir.iterdir():
                if profile_path.is_dir():
                    name = profile_path.name
                    # Calculate size
                    size_bytes = sum(f.stat().st_size for f in profile_path.rglob("*") if f.is_file())
                    size_mb = size_bytes / (1024 * 1024)
                    # Get last modified time
                    mtime = profile_path.stat().st_mtime
                    profiles.append({
                        "name": name,
                        "path": str(profile_path),
                        "size_mb": round(size_mb, 2),
                        "last_used": datetime.fromtimestamp(mtime).isoformat(),
                        "in_use": name in self.active_profiles,
                    })
        return sorted(profiles, key=lambda p: p["name"])

    def create_profile(self, name: str) -> dict[str, Any]:
        """Create a new browser profile directory."""
        if not name or not name.strip():
            raise ValueError("Profile name is required")

        name = name.strip()

        # Validate profile name (alphanumeric, hyphens, underscores only)
        if not all(c.isalnum() or c in "-_" for c in name):
            raise ValueError("Profile name can only contain letters, numbers, hyphens, and underscores")

        profile_path = self.profiles_dir / name
        if profile_path.exists():
            raise ValueError(f"Profile '{name}' already exists")

        profile_path.mkdir(parents=True)
        logger.info(f"Created profile '{name}' at {profile_path}")

        return {
            "name": name,
            "path": str(profile_path),
            "size_mb": 0,
            "last_used": datetime.now().isoformat(),
            "in_use": False,
        }

    def delete_profile(self, name: str) -> bool:
        """Delete a browser profile."""
        if name in self.active_profiles:
            raise ValueError(f"Profile '{name}' is currently in use by browser {self.active_profiles[name]}")

        profile_path = self.profiles_dir / name
        if not profile_path.exists():
            return False

        shutil.rmtree(profile_path)
        logger.info(f"Deleted profile '{name}'")
        return True

    def get_profile(self, name: str) -> dict[str, Any] | None:
        """Get information about a specific profile."""
        profile_path = self.profiles_dir / name
        if not profile_path.exists():
            return None

        # Calculate size
        size_bytes = sum(f.stat().st_size for f in profile_path.rglob("*") if f.is_file())
        size_mb = size_bytes / (1024 * 1024)
        # Get last modified time
        mtime = profile_path.stat().st_mtime

        return {
            "name": name,
            "path": str(profile_path),
            "size_mb": round(size_mb, 2),
            "last_used": datetime.fromtimestamp(mtime).isoformat(),
            "in_use": name in self.active_profiles,
        }
