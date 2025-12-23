#!/usr/bin/env python3
"""
AI Vision Analysis Example

Demonstrates: using the `what_is_visible` endpoint to get AI-powered
analysis of page content. Useful for AI agents to understand page state.

Requirements:
    - OPENROUTER_API_KEY environment variable set in the container
"""

import time

from airbrowser_client import ApiClient, Configuration
from airbrowser_client.api import BrowserApi

import os
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:18080/api/v1")


def main():
    print("=" * 60)
    print("AI Vision Analysis Example (what_is_visible)")
    print("=" * 60)

    config = Configuration(host=API_BASE)

    with ApiClient(config) as client:
        api = BrowserApi(client)

        # Create browser
        print("\nCreating browser...")
        response = api.create_browser(payload={
            "uc": True,
            "headless": False,
            "window_size": [1280, 900]
        })
        browser_id = response.data.browser_id
        print(f"Browser created: {browser_id}")

        try:
            # Navigate to Steam signup page
            print("\nNavigating to Steam signup page...")
            api.navigate_browser(
                browser_id=browser_id,
                payload={
                    "url": "https://store.steampowered.com/join",
                    "timeout": 30
                }
            )
            print("Navigation successful")

            # Wait for page to fully load
            time.sleep(5)

            # Test what_is_visible tool
            print("\nAnalyzing page with AI vision...")
            analysis_start = time.time()

            analysis_result = api.what_is_visible(browser_id=browser_id)

            analysis_time = time.time() - analysis_start

            if not analysis_result.success:
                print(f"Analysis failed: {analysis_result.error}")
                return

            print(f"Page analysis completed in {analysis_time:.2f}s")
            print(f"Model used: {analysis_result.model or 'Unknown'}")

            # Display the analysis
            analysis = analysis_result.analysis or ''
            if analysis:
                print("\n" + "=" * 60)
                print("COMPREHENSIVE PAGE ANALYSIS:")
                print("=" * 60)
                print(analysis)
                print("=" * 60)

                # Check for key elements
                analysis_lower = analysis.lower()

                print("\nKEY ELEMENTS DETECTED:")
                print("-" * 30)

                checks = [
                    (['email', 'password', 'username', 'account', 'field'], "Form fields"),
                    (['captcha', 'hcaptcha', 'recaptcha'], "CAPTCHA"),
                    (['button', 'submit', 'continue', 'create'], "Buttons"),
                    (['required', 'mandatory', '*', 'must'], "Required fields"),
                    (['filled', 'empty', 'completed', 'incomplete'], "Form state"),
                ]

                for keywords, label in checks:
                    if any(kw in analysis_lower for kw in keywords):
                        print(f"  [OK] {label} detected")
                    else:
                        print(f"  [?]  {label} not clearly detected")
            else:
                print("No analysis content returned")

            # Test page state changes
            print("\nTesting page state changes...")

            try:
                # Try to fill email field
                api.type_text(
                    browser_id=browser_id,
                    payload={
                        "selector": "input[type='email'], input[name='email'], #email",
                        "text": "test@example.com",
                        "timeout": 5
                    }
                )
                print("Filled email field")
                time.sleep(2)

                # Re-analyze
                print("Re-analyzing page after filling email...")
                analysis2_result = api.what_is_visible(browser_id=browser_id)

                if analysis2_result.success:
                    analysis2 = analysis2_result.analysis or ''
                    print("\nUPDATED PAGE ANALYSIS:")
                    print("-" * 40)
                    print(analysis2[:500] + "..." if len(analysis2) > 500 else analysis2)

                    if 'filled' in analysis2.lower() or 'completed' in analysis2.lower():
                        print("\n[OK] Tool detected field was filled!")
                    else:
                        print("\n[?] Tool may not have detected field change")

            except Exception as e:
                print(f"Could not fill email field: {e}")

            # Final screenshot
            print("\nTaking final screenshot...")
            screenshot = api.take_screenshot(browser_id=browser_id)
            print(f"Screenshot: {screenshot.data.screenshot_url}")

            print("\n" + "=" * 60)
            print("SUCCESS! what_is_visible provides:")
            print("  - Form field states and requirements")
            print("  - Interactive element status")
            print("  - CAPTCHA detection")
            print("  - Page purpose and next actions")
            print("  - No prompt required - just browser_id!")
            print("=" * 60)

        finally:
            # Cleanup
            print(f"\nClosing browser {browser_id}...")
            api.delete_browser(browser_id=browser_id)
            print("Browser closed")


if __name__ == "__main__":
    main()
