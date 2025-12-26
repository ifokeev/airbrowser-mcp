"""Enhanced tool descriptions for MCP - provides AI agent guidance.

These descriptions are merged with auto-generated tools to give AI agents
better context about when and how to use each tool.
"""

TOOL_DESCRIPTIONS: dict[str, str] = {
    "what_is_visible": """
**PRIMARY TOOL FOR VISUAL VERIFICATION** - Use this instead of take_screenshot + curl + Read.

This is the BEST and FASTEST way to see what's on the page. It takes a screenshot internally
and uses AI to analyze it, so you don't need to manually download and view screenshots.

**Automatically analyzes:**
- **Form fields**: Which are filled, empty, or required
- **Interactive elements**: Checkbox/radio states, button availability
- **CAPTCHA status**: Present, solved, or needs attention
- **Messages**: Errors, success notifications, validation feedback
- **Page purpose**: What the user should do next

**Use this to:**
- Verify actions worked (after click, type, navigate)
- Understand current page state
- Find elements to interact with
- Debug issues
""",
    "detect_coordinates": """
**VISION-BASED ELEMENT DETECTION** - Find elements using AI vision. PREFER THIS over HTML parsing.

**RECOMMENDED APPROACH**: When AI vision is enabled, use this tool to locate elements instead of
parsing HTML. It's more robust, works on any page, and enables undetectable GUI interactions.

**Workflow - CLICK**: `detect_coordinates` → `gui_click_xy`
**Workflow - TYPE**: `detect_coordinates` → `gui_type_xy`
**Workflow - HOVER**: `detect_coordinates` → `gui_hover_xy`

**Perfect for:**
- Any page when AI vision is enabled (preferred over selectors)
- CAPTCHAs in complex layouts ("find the hCaptcha checkbox")
- Dynamic content without stable selectors
- Elements easier to describe than locate in HTML ("the blue Submit button")
- Large/complex pages where HTML parsing is impractical

**IMPORTANT - BE SPECIFIC IN YOUR PROMPTS**: The tool clicks at the CENTER of detected elements.
For wide elements with icons (like search boxes with camera/voice icons on the right), be specific
about which part you want to click:

**Good prompts** (specific):
- "the text input area of the search box" (not the whole search bar)
- "the Google Search button" (specific button, not the search box)
- "the email text field" (clickable input area)
- "the Submit button with blue background"
- "the checkbox next to 'Remember me'"

**Bad prompts** (too broad):
- "the search box" (may include icons, clicking center could hit camera icon)
- "the input field" (ambiguous if multiple exist)
- "the button" (which button?)

**More examples:**
- "the password input field"
- "the blue Submit button at the bottom of the form"
- "the login button in the top right corner"
- "the dropdown menu labeled 'Country'"

**Click Position Control (fx, fy parameters):**
For wide elements with icons on the right (like Google's search box), use fx to click
left of center and avoid hitting the wrong element:
- `fx=0.2` - clicks at 20% from left edge (avoids right-side icons like Google Lens)
- `fx=0.5` - clicks at center (default)
- `fx=0.8` - clicks at 80% from left edge
- `fy` controls vertical position similarly (0.0=top, 0.5=center, 1.0=bottom)

Example: For Google search, use `fx=0.2` to click the text input area, not the camera icon.

Returns:
- Bounding box coordinates (x, y, width, height)
- Recommended click point (calculated using fx, fy offsets)
- Detection confidence score
""",
    "gui_click": """
**GUI CLICK WITH SELECTOR** - Click elements using CSS/XPath selectors with undetectable GUI automation.

**SELECTOR SYNTAX**: Use standard CSS selectors or XPath only. Playwright-style selectors
like `:has-text()` are NOT supported. Examples:
- CSS: `iframe[src*="hcaptcha"]`, `button.submit`, `#checkbox`
- XPath (use by="xpath"): `//button[contains(text(), "Submit")]`

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

**VERIFICATION**: After clicking, use `what_is_visible` to verify the action worked.

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

**VERIFICATION**: After clicking, use `what_is_visible` to verify the action worked.
""",
    "gui_type_xy": """
**GUI TYPE AT COORDINATES** - Click at coordinates then type text using undetectable GUI automation.

**PREFERRED WORKFLOW** when AI vision is enabled:
1. Call `detect_coordinates` with a description like "the email input field"
2. Use the returned coordinates with this tool to click and type text

**Use this when:**
- AI vision is enabled and you need to type into an element
- Page HTML is too large/complex for selector parsing
- Input fields on anti-automation sites
- Dynamic elements without stable selectors

This performs a real GUI click at coordinates, then types using PyAutoGUI - completely undetectable.

**VERIFICATION**: After typing, use `what_is_visible` to verify the text was entered correctly.
""",
    "gui_hover_xy": """
**GUI HOVER AT COORDINATES** - Move mouse to coordinates using GUI automation.

**Use with `detect_coordinates`**:
1. Call `detect_coordinates` to find element position
2. Use this tool to hover over the element

**Use this for:**
- Revealing tooltips or dropdown menus
- Triggering hover effects before clicking
- Elements that require mouse interaction to become visible

**VERIFICATION**: After hovering, use `what_is_visible` to see what appeared.
""",
    "gui_press_keys_xy": """
**GUI PRESS KEYS AT COORDINATES** - Click to focus, then press special keys.

**Use with `detect_coordinates`**:
1. Call `detect_coordinates` to find element position
2. Use `gui_press_keys_xy` to click and press keys (ENTER, TAB, etc.)

**Supports:**
- Single keys: ENTER, TAB, ESCAPE, BACKSPACE, DELETE, SPACE
- Arrow keys: UP, DOWN, LEFT, RIGHT, HOME, END, PAGE_UP, PAGE_DOWN
- Function keys: F1-F12
- Modifiers: CTRL, ALT, SHIFT, META, COMMAND
- Combinations: "CTRL+a", "SHIFT+TAB", "CTRL+ENTER"

**Example workflow for Google search:**
1. `detect_coordinates` → find search box
2. `gui_type_xy` → type "openai"
3. `gui_press_keys_xy` → press "ENTER" to search

**VERIFICATION**: Use `what_is_visible` after pressing keys to verify result.
""",
    "get_content": """
**GET VISIBLE TEXT CONTENT** - Retrieve the visible text from the current page (no HTML).

**PREFER `what_is_visible`**: If AI vision is enabled, use `what_is_visible` instead - it provides
richer context including form states, interactive elements, and visual understanding without
needing to parse raw text.

**Use `get_content` only when:**
- You need to extract large amounts of text for processing (articles, documentation)
- You need exact text for string matching or comparison
- AI vision is not available

Returns only the text that a user would see on the page, extracted from the DOM.
Text is truncated at 50,000 characters to stay within token limits.

Returns: Visible text content, current URL, page title, and truncation flag.
""",
    "take_screenshot": """
Take a screenshot of the browser.

**PREFER `what_is_visible`**: If AI vision is enabled (OPENROUTER_API_KEY set), use `what_is_visible`
instead - it's faster and provides AI analysis without manual screenshot download.

**MANUAL SCREENSHOT WORKFLOW** (only if `what_is_visible` is not available):
1. Call `take_screenshot` → get `screenshot_url`
2. Download with curl: `curl -s <screenshot_url> -o /tmp/screenshot.png`
3. Use the Read tool on `/tmp/screenshot.png` to view the image
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
    "navigate": """
Navigate the browser to a URL.

**VERIFICATION**: After navigating, verify the page loaded correctly:
- **If AI vision enabled**: Use `what_is_visible` - provides URL, page state, and visual confirmation
- **Otherwise**: Use `get_content` to check page title and text content

Don't assume navigation succeeded just because the API returned success.
""",
    "click": """
Click on an element using CSS selector or XPath.

**PREFER VISION + GUI**: If AI vision is enabled, prefer using `detect_coordinates` + `gui_click_xy`:
1. Use `detect_coordinates` to find the element by description
2. Use `gui_click_xy` with the returned coordinates
This approach is more robust and undetectable by anti-automation systems.

**Use this tool only when:**
- You already know the exact CSS/XPath selector
- The page HTML is small enough to parse
- Vision tools are not available

**SELECTOR SYNTAX**: Use standard CSS selectors or XPath only. Playwright-style selectors
like `:has-text()` are NOT supported. Examples:
- CSS: `a[href*="example"]`, `button.submit`, `#login-btn`
- XPath (use by="xpath"): `//a[contains(text(), "Click me")]`, `//button[@type="submit"]`

**COMMON ISSUES:**
- Generic `input` selector may match file inputs, which cannot be clicked (use more specific selectors)
- For file uploads, use `upload_file` tool instead of click

**VERIFICATION**: Use `what_is_visible` to verify the action worked.
""",
    "type_text": """
Type text into an input field using CSS selector or XPath.

**PREFER VISION + GUI**: If AI vision is enabled, prefer using `detect_coordinates` + `gui_type_xy`:
1. Use `detect_coordinates` to find the input field by description
2. Use `gui_type_xy` with the returned coordinates and text to type
This approach is more robust and undetectable by anti-automation systems.

**Use this tool only when:**
- You already know the exact CSS/XPath selector
- The page HTML is small enough to parse
- Vision tools are not available

**SELECTOR SYNTAX**: Use standard CSS selectors or XPath only. Playwright-style selectors
like `:has-text()` are NOT supported.

**COMMON SELECTOR ISSUES:**
- Google search now uses `<textarea name="q">` NOT `<input name="q">`
- For Google: use `textarea[name="q"]` or prefer vision-based `detect_coordinates` + `gui_type_xy`

**VERIFICATION**: Use `what_is_visible` to verify the text was entered correctly.
""",
    "press_keys": """
Press keyboard keys on an element. Supports special keys (ENTER, TAB, ESCAPE, etc.)
and key combinations (CTRL+a, SHIFT+TAB).

**VERIFICATION**: After pressing ENTER to submit a form or perform a search, ALWAYS verify:
- **If AI vision enabled**: Use `what_is_visible` - shows resulting page, success/error messages
- **Otherwise**: Use `get_content` to check the resulting page

Don't assume the key press had the intended effect without verification.
""",
    "get_url": """
Get the current page URL.

**NOTE**: If you just called `what_is_visible`, the URL is already included in its response.
Don't call this tool redundantly after using vision tools.

Use this only when you specifically need the URL without visual verification.
""",
}
