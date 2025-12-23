"""Device emulation browser commands."""

import logging

logger = logging.getLogger(__name__)

# Common device presets
DEVICE_PRESETS = {
    "iPhone 14": {
        "width": 390,
        "height": 844,
        "device_scale_factor": 3,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
    "iPhone 14 Pro Max": {
        "width": 430,
        "height": 932,
        "device_scale_factor": 3,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
    "iPhone SE": {
        "width": 375,
        "height": 667,
        "device_scale_factor": 2,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    },
    "iPad": {
        "width": 768,
        "height": 1024,
        "device_scale_factor": 2,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
    "iPad Pro": {
        "width": 1024,
        "height": 1366,
        "device_scale_factor": 2,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    },
    "Pixel 7": {
        "width": 412,
        "height": 915,
        "device_scale_factor": 2.625,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    },
    "Samsung Galaxy S21": {
        "width": 360,
        "height": 800,
        "device_scale_factor": 3,
        "mobile": True,
        "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    },
    "Desktop 1080p": {
        "width": 1920,
        "height": 1080,
        "device_scale_factor": 1,
        "mobile": False,
        "user_agent": None,  # Keep default
    },
    "Desktop 1440p": {
        "width": 2560,
        "height": 1440,
        "device_scale_factor": 1,
        "mobile": False,
        "user_agent": None,
    },
    "Laptop": {
        "width": 1366,
        "height": 768,
        "device_scale_factor": 1,
        "mobile": False,
        "user_agent": None,
    },
}


def handle_emulate(driver, command: dict) -> dict:
    """Emulate a device (viewport, user agent, touch).

    Args:
        command: {
            "device": device preset name OR
            "width": viewport width,
            "height": viewport height,
            "device_scale_factor": pixel ratio (default 1),
            "mobile": enable touch events (default false),
            "user_agent": custom user agent (optional)
        }
    """
    device = command.get("device")

    if device:
        # Use preset
        if device not in DEVICE_PRESETS:
            return {
                "status": "error",
                "message": f"Unknown device: {device}",
                "available_devices": list(DEVICE_PRESETS.keys()),
            }
        config = DEVICE_PRESETS[device]
    else:
        # Use custom config
        config = {
            "width": command.get("width", 1920),
            "height": command.get("height", 1080),
            "device_scale_factor": command.get("device_scale_factor", 1),
            "mobile": command.get("mobile", False),
            "user_agent": command.get("user_agent"),
        }

    try:
        # Set viewport size
        driver.set_window_size(config["width"], config["height"])

        # Set device metrics via CDP
        driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": config["width"],
                "height": config["height"],
                "deviceScaleFactor": config["device_scale_factor"],
                "mobile": config["mobile"],
            },
        )

        # Set touch emulation if mobile
        if config["mobile"]:
            driver.execute_cdp_cmd(
                "Emulation.setTouchEmulationEnabled",
                {"enabled": True, "maxTouchPoints": 5},
            )

        # Set user agent if specified
        if config["user_agent"]:
            driver.execute_cdp_cmd(
                "Emulation.setUserAgentOverride",
                {"userAgent": config["user_agent"]},
            )

        return {
            "status": "success",
            "emulation": {
                "device": device,
                "width": config["width"],
                "height": config["height"],
                "device_scale_factor": config["device_scale_factor"],
                "mobile": config["mobile"],
                "user_agent": config["user_agent"],
            },
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to emulate device: {str(e)}"}


def handle_list_devices(driver, command: dict) -> dict:
    """List available device presets."""
    devices = []
    for name, config in DEVICE_PRESETS.items():
        devices.append(
            {
                "name": name,
                "width": config["width"],
                "height": config["height"],
                "mobile": config["mobile"],
            }
        )
    return {"status": "success", "devices": devices}


def handle_clear_emulation(driver, command: dict) -> dict:
    """Clear device emulation and restore defaults."""
    try:
        driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
        driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {"enabled": False})
        return {"status": "success", "message": "Emulation cleared"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear emulation: {str(e)}"}
