"""Dialog handling browser commands."""

import logging

from selenium.common.exceptions import NoAlertPresentException

logger = logging.getLogger(__name__)


def handle_dialog(driver, command: dict) -> dict:
    """Handle browser dialog (alert, confirm, prompt).

    Args:
        command: {
            "action": "accept" | "dismiss",
            "text": optional text for prompt dialogs
        }
    """
    action = command.get("action", "accept")
    text = command.get("text")

    try:
        alert = driver.switch_to.alert
        dialog_text = alert.text

        if action == "accept":
            if text is not None:
                alert.send_keys(text)
            alert.accept()
            return {
                "status": "success",
                "action": "accepted",
                "dialog_text": dialog_text,
            }
        else:
            alert.dismiss()
            return {
                "status": "success",
                "action": "dismissed",
                "dialog_text": dialog_text,
            }

    except NoAlertPresentException:
        return {"status": "error", "message": "No dialog present"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to handle dialog: {str(e)}"}


def handle_get_dialog(driver, command: dict) -> dict:
    """Get current dialog text without dismissing it."""
    try:
        alert = driver.switch_to.alert
        return {
            "status": "success",
            "present": True,
            "text": alert.text,
        }
    except NoAlertPresentException:
        return {
            "status": "success",
            "present": False,
            "text": None,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to get dialog: {str(e)}"}
