"""Enhanced tool descriptions for MCP - provides AI agent guidance.

These descriptions are merged with auto-generated tools to give AI agents
better context about when and how to use each tool.
"""

TOOL_DESCRIPTIONS: dict[str, str] = {
    "what_is_visible": """
**PRIMARY TOOL FOR UNDERSTANDING WEBPAGES** - Comprehensive page state analysis.

This is the BEST tool to use when you need to understand what's currently happening on a webpage.
It automatically analyzes and reports on:

- **Form fields**: Which are filled, empty, or required
- **Interactive elements**: Checkbox/radio states, button availability
- **CAPTCHA status**: Present, solved, or needs attention
- **Messages**: Errors, success notifications, validation feedback
- **Form progress**: Multi-step form status and current step
- **Page purpose**: What the user should do next

**Use this when you need to:**
- Understand the current state of any webpage
- Check if forms are filled correctly
- Verify CAPTCHA completion
- Identify what actions are available
- Debug form submission issues
""",
    "detect_coordinates": """
**VISION-BASED ELEMENT DETECTION** - Find elements using AI vision when HTML parsing is impractical.

**Best for large/complex pages (>100KB HTML)**: When `get_page_content` returns too much data
to parse effectively, use this to locate elements by visual description instead.

**Alternative to HTML parsing**: Instead of analyzing HTML source, this takes a screenshot
and uses AI vision to find elements by natural language description.

**Perfect for:**
- CAPTCHAs in complex layouts ("find the hCaptcha checkbox")
- Dynamic content without stable selectors
- Elements easier to describe than locate in HTML ("the blue Submit button")
- Pages with overwhelming HTML structure

**Workflow**: Use this to get coordinates, then use `gui_click_xy` to click at those coordinates.

Returns:
- Bounding box coordinates (x, y, width, height)
- Recommended click point (center of element)
- Detection confidence score
- Screenshot path for verification
- Vision model used for detection
""",
    "gui_click": """
**GUI CLICK WITH SELECTOR** - Click elements using CSS/XPath selectors with undetectable GUI automation.

**WORKFLOW**: Always call `get_page_content` first to understand the page structure and identify
the correct selector for the element you want to click.

**CRITICAL FOR CAPTCHAs**: Use this for CAPTCHA interactions when you can identify them with
CSS selectors. For complex pages where selectors are hard to find, use `detect_coordinates` +
`gui_click_xy` instead.

**Best for pages < 100KB**: When HTML is manageable and you can parse it to find selectors.
For larger/complex pages, use the vision-based approach with `detect_coordinates`.

Uses Chrome DevTools Protocol to calculate screen coordinates and PyAutoGUI to perform
the actual click, making it undetectable by anti-automation measures.

**When to use this tool:**
- CAPTCHAs where you can identify the selector (e.g., iframe[src*="hcaptcha"])
- Elements that don't respond to regular clicks but have clear selectors
- Anti-automation sites when you know the element selector
- Elements inside iframes or shadow DOM with identifiable selectors

**Parameters:**
- fx, fy: Optional fractional offsets (0.0-1.0) within element to click
""",
    "gui_click_xy": """
**GUI CLICK WITH COORDINATES** - Click at specific screen coordinates using GUI automation.

**Best for large/complex pages (>100KB HTML)**: When `get_page_content` returns too much data
to parse effectively, use this coordinate-based approach instead of selector-based clicking.

**Required workflow**:
1. Call `detect_coordinates` with a description of the element to find its position
2. Use the returned coordinates with this tool to perform the undetectable click

**Use this when:**
- Page HTML is too large/complex for selector parsing
- CAPTCHAs in visually complex layouts
- Dynamic elements without stable selectors
- Elements that are easier to describe visually than locate in HTML

This performs the actual GUI click using PyAutoGUI, making it undetectable by anti-automation systems.
""",
    "get_content": """
**GET VISIBLE TEXT CONTENT** - Retrieve the visible text from the current page (no HTML).

Returns only the text that a user would see on the page, extracted from the DOM.
Much more compact than raw HTML and suitable for understanding page content.

**Use this to:**
- Read article or page content
- Extract visible text for analysis
- Understand what the user sees without HTML clutter
- Get page title and current URL

**Note**: Text is truncated at 50,000 characters to stay within token limits.
For visual understanding, use `what_is_visible` instead.

Returns: Visible text content, current URL, page title, and truncation flag.
""",
    "take_screenshot": """
Take a screenshot of the browser (returns image URL only).

NOTE: If you want to UNDERSTAND what's on the page, use `what_is_visible` instead!
`what_is_visible` combines screenshot + AI analysis for better understanding.
""",
    "console_logs": """
List recent browser console messages (best-effort; depends on Chrome/Selenium logging support).

Useful for debugging JavaScript errors, network issues, or application logs.
Use action="get" to retrieve logs, action="clear" to clear them.
""",
    "network_logs": """
List recent network events captured from Chrome performance logs.

This is best-effort and may require Chrome logging support in the underlying driver.
Useful for debugging API calls, failed requests, or performance issues.
Use action="get" to retrieve logs, action="clear" to clear them.
""",
    "fill_form": """
**BATCH FORM FILLING** - Fill multiple form fields at once.

More efficient than calling `type_text` multiple times. Pass an array of field definitions:
[{"selector": "#email", "value": "user@example.com"}, {"selector": "#password", "value": "secret"}]

Returns which fields were filled successfully and any errors encountered.
""",
    "emulate": """
**DEVICE EMULATION** - Emulate mobile devices, tablets, or custom viewports.

Use device presets like "iPhone 14", "iPad", "Pixel 7" or specify custom dimensions.
Affects viewport size, user agent, touch events, and device scale factor.

Call `list_devices` to see available device presets.
""",
    "dialog": """
**DIALOG HANDLING** - Accept, dismiss, or interact with browser dialogs.

Handles JavaScript alert(), confirm(), and prompt() dialogs.
- action="get": Get current dialog info
- action="accept": Click OK/Accept
- action="dismiss": Click Cancel/Dismiss
- text: For prompt dialogs, provide input text before accepting
""",
    "scroll": """
**SCROLL TO ELEMENT OR POSITION** - Scroll the page to bring an element into view or to specific coordinates.

Can scroll to:
- An element by CSS selector (scrolls element to center of viewport)
- Absolute coordinates (x, y position on page)

Use `scroll_by` for relative scrolling.
""",
}
