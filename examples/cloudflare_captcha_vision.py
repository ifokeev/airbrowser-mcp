#!/usr/bin/env python3
"""
Cloudflare Captcha AI Vision Example

Demonstrates using AI vision tools to:
1. detect_coordinates - Find the captcha checkbox using natural language
2. gui_click - Click on the detected coordinates (human-like mouse movement)
3. what_is_visible - Verify the captcha state after clicking

Requirements:
    - OPENROUTER_API_KEY environment variable set in the container
"""

import os
import time

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi, HealthApi

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def main():
    print("=" * 60)
    print("Cloudflare Captcha - AI Vision Click Example")
    print("=" * 60)

    config = Configuration(host=API_BASE)

    with ApiClient(config) as client:
        # Check if vision is enabled
        health_api = HealthApi(client)
        health = health_api.health_check()
        vision_enabled = getattr(health, "vision_enabled", False)
        if not vision_enabled:
            print("\nERROR: Vision tools are not available!")
            print("Start the container with: OPENROUTER_API_KEY=sk-or-... docker compose up")
            return

        print("\n✓ Vision tools enabled")

        api = BrowserApi(client)

        # Create browser
        print("\nCreating browser...")
        response = api.create_browser(payload={"window_size": [1280, 900]})
        browser_id = response.data["browser_id"]
        print(f"Browser created: {browser_id}")

        try:
            # Navigate to Cloudflare login
            print("\nNavigating to Cloudflare login page...")
            api.navigate_browser(
                browser_id=browser_id,
                payload={"url": "https://dash.cloudflare.com/login", "timeout": 30},
            )
            print("Navigation successful")

            # Wait for page to fully load (captcha needs time to render)
            print("Waiting for page and captcha to load (10s)...")
            time.sleep(10)

            # Take initial screenshot
            print("\nTaking screenshot before clicking...")
            screenshot_before = api.take_screenshot(browser_id=browser_id, payload={})
            print(f"Screenshot: {screenshot_before.data.get('screenshot_url')}")

            # Step 1: Use AI vision to detect the captcha checkbox
            print("\n" + "-" * 40)
            print("STEP 1: Detecting captcha checkbox with AI vision...")
            print("-" * 40)

            detect_result = api.detect_coordinates(
                browser_id=browser_id,
                payload={"prompt": "the 'Verify you are human' checkbox"},
            )

            if not detect_result.success:
                error_msg = getattr(detect_result, "error", None) or getattr(detect_result, "message", "Unknown error")
                print(f"Detection failed: {error_msg}")
                print("Make sure OPENROUTER_API_KEY is set in the container.")
                print("Taking screenshot to debug...")
                api.take_screenshot(browser_id=browser_id, payload={})
                return

            # Extract coordinates from response data
            data = detect_result.data or {}
            click_point = data.get("click_point", {})
            x = click_point.get("x")
            y = click_point.get("y")
            confidence = data.get("confidence", 0)
            model_used = data.get("model_used", "Unknown")

            print("Captcha checkbox detected!")
            print(f"  Coordinates: ({x}, {y})")
            print(f"  Confidence: {confidence:.2%}")
            print(f"  Model used: {model_used}")

            if x is None or y is None:
                print("ERROR: Could not extract coordinates from detection result")
                return

            # Step 2: Click on the captcha using gui_click (human-like movement)
            print("\n" + "-" * 40)
            print("STEP 2: Clicking captcha with gui_click (human-like)...")
            print("-" * 40)

            click_result = api.gui_click(
                browser_id=browser_id,
                payload={
                    "x": x,
                    "y": y,
                    "timeframe": 0.3,  # Slow, human-like mouse movement
                },
            )

            if click_result.success:
                print(f"Click successful at ({x}, {y})")
            else:
                print(f"Click failed: {click_result.message}")

            # Wait for captcha to process
            print("Waiting for captcha to process...")
            time.sleep(3)

            # Take screenshot after clicking
            print("\nTaking screenshot after clicking...")
            screenshot_after = api.take_screenshot(browser_id=browser_id, payload={})
            print(f"Screenshot: {screenshot_after.data.get('screenshot_url')}")

            # Step 3: Use AI vision to verify the captcha state
            print("\n" + "-" * 40)
            print("STEP 3: Verifying captcha state with what_is_visible...")
            print("-" * 40)

            analysis_result = api.what_is_visible(browser_id=browser_id)

            if analysis_result.success:
                # Extract data from GenericResponse
                data = analysis_result.data or {}
                analysis = data.get("analysis", "")
                model_used = data.get("model", "Unknown")

                print(f"Model used: {model_used}")
                print("\nAI Analysis of current page state:")
                print("-" * 40)
                print(analysis[:1000] + "..." if len(analysis) > 1000 else analysis)

                # Check if captcha appears to be verified
                analysis_lower = analysis.lower()
                captcha_indicators = [
                    "verified",
                    "checked",
                    "completed",
                    "success",
                    "passed",
                    "green",
                    "checkmark",
                ]
                pending_indicators = [
                    "verifying",
                    "processing",
                    "loading",
                    "spinning",
                ]
                failed_indicators = ["failed", "error", "retry", "again"]

                print("\n" + "-" * 40)
                print("CAPTCHA STATE ANALYSIS:")
                print("-" * 40)

                if any(ind in analysis_lower for ind in captcha_indicators):
                    print("[SUCCESS] Captcha appears to be verified!")
                elif any(ind in analysis_lower for ind in pending_indicators):
                    print("[PENDING] Captcha is still processing...")
                elif any(ind in analysis_lower for ind in failed_indicators):
                    print("[FAILED] Captcha verification may have failed")
                else:
                    print("[UNKNOWN] Captcha state unclear from analysis")

            else:
                error_msg = getattr(analysis_result, "error", None) or getattr(
                    analysis_result, "message", "Unknown error"
                )
                print(f"Analysis failed: {error_msg}")

            # Summary
            print("\n" + "=" * 60)
            print("EXAMPLE COMPLETE")
            print("=" * 60)
            print("\nThis example demonstrated:")
            print("  1. detect_coordinates - AI finds elements by description")
            print("  2. gui_click - Human-like mouse movement and click")
            print("  3. what_is_visible - AI analyzes page state")
            print("\nThese tools enable AI agents to interact with")
            print("protected pages that block traditional automation.")
            print("=" * 60)

        finally:
            # Cleanup
            print(f"\nClosing browser {browser_id}...")
            api.close_browser(browser_id=browser_id)
            print("Browser closed")


if __name__ == "__main__":
    main()
