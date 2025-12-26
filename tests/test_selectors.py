#!/usr/bin/env python3
"""
Test suite for different selector types (CSS, XPath, id, name).

Verifies that all element interaction functions work correctly with:
- CSS selectors (default)
- XPath selectors
- ID selectors
- Name attribute selectors

Run with: pytest tests/test_selectors.py -v
"""

import pytest
from airbrowser_client.models import (
    CreateBrowserRequest,
    ClickRequest,
    ExecuteScriptRequest,
    NavigateBrowserRequest,
    PressKeysRequest,
    TypeTextRequest,
    WaitElementRequest,
)


@pytest.fixture(scope="class")
def browser_with_test_page(browser_client):
    """Create a browser with a test page containing various elements."""
    config = CreateBrowserRequest(window_size=[1920, 1080])
    result = browser_client.create_browser(payload=config)
    assert result is not None and result.success
    bid = result.data['browser_id']

    # Navigate to example.com
    browser_client.navigate_browser(bid, payload=NavigateBrowserRequest(url="https://example.com"))

    # Create test elements with various attributes for selector testing
    exec_request = ExecuteScriptRequest(
        script="""
        // Create a container div
        var container = document.createElement('div');
        container.id = 'test-container';
        container.className = 'test-class';

        // Input with id
        var inputId = document.createElement('input');
        inputId.id = 'test-input-by-id';
        inputId.type = 'text';
        inputId.placeholder = 'Input by ID';
        container.appendChild(inputId);
        container.appendChild(document.createElement('br'));

        // Input with name
        var inputName = document.createElement('input');
        inputName.name = 'test-input-by-name';
        inputName.type = 'text';
        inputName.placeholder = 'Input by name';
        container.appendChild(inputName);
        container.appendChild(document.createElement('br'));

        // Input with class (for CSS selector)
        var inputClass = document.createElement('input');
        inputClass.className = 'test-input-class';
        inputClass.type = 'text';
        inputClass.placeholder = 'Input by class';
        container.appendChild(inputClass);
        container.appendChild(document.createElement('br'));

        // Button with data attribute (for XPath)
        var button = document.createElement('button');
        button.id = 'test-button';
        button.setAttribute('data-testid', 'submit-button');
        button.textContent = 'Click Me';
        container.appendChild(button);
        container.appendChild(document.createElement('br'));

        // Span with text (for XPath text matching)
        var span = document.createElement('span');
        span.id = 'test-span';
        span.className = 'test-span-class';
        span.textContent = 'Test Span Text';
        container.appendChild(span);

        // Insert at top of body
        document.body.insertBefore(container, document.body.firstChild);

        return 'Test elements created';
        """,
        timeout=30,
    )
    browser_client.execute_script(bid, payload=exec_request)

    yield bid

    # Cleanup
    try:
        browser_client.close_browser(bid)
    except Exception:
        pass


@pytest.mark.browser
class TestCSSSelectors:
    """Test element interactions using CSS selectors."""

    def test_click_css_id_selector(self, browser_client, browser_with_test_page):
        """Test click with CSS ID selector (#id)."""
        request = ClickRequest(selector="#test-button", by="css", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_click_css_class_selector(self, browser_client, browser_with_test_page):
        """Test click with CSS class selector (.class)."""
        request = ClickRequest(selector=".test-span-class", by="css", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_click_css_attribute_selector(self, browser_client, browser_with_test_page):
        """Test click with CSS attribute selector ([attr=value])."""
        request = ClickRequest(selector="[data-testid='submit-button']", by="css", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_type_css_selector(self, browser_client, browser_with_test_page):
        """Test type with CSS selector."""
        request = TypeTextRequest(selector=".test-input-class", text="CSS typed text", by="css", timeout=10)
        result = browser_client.type_text(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Type failed: {result.message}"

    def test_wait_css_selector(self, browser_client, browser_with_test_page):
        """Test wait_element with CSS selector."""
        request = WaitElementRequest(selector="#test-container", by="css", until="visible", timeout=10)
        result = browser_client.wait_element(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Wait failed: {result.message}"

    def test_check_element_css_selector(self, browser_client, browser_with_test_page):
        """Test check_element with CSS selector."""
        result = browser_client.check_element(browser_with_test_page, selector="#test-button", by="css", check="exists")
        assert result is not None
        assert result.success

        result = browser_client.check_element(browser_with_test_page, selector="#test-button", by="css", check="visible")
        assert result is not None
        assert result.success


@pytest.mark.browser
class TestXPathSelectors:
    """Test element interactions using XPath selectors."""

    def test_click_xpath_by_id(self, browser_client, browser_with_test_page):
        """Test click with XPath selector using @id."""
        request = ClickRequest(selector="//*[@id='test-button']", by="xpath", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_click_xpath_by_text(self, browser_client, browser_with_test_page):
        """Test click with XPath selector using text()."""
        request = ClickRequest(selector="//button[text()='Click Me']", by="xpath", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_click_xpath_by_contains_text(self, browser_client, browser_with_test_page):
        """Test click with XPath selector using contains(text())."""
        request = ClickRequest(selector="//span[contains(text(), 'Span Text')]", by="xpath", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_click_xpath_by_attribute(self, browser_client, browser_with_test_page):
        """Test click with XPath selector using @attribute."""
        request = ClickRequest(selector="//button[@data-testid='submit-button']", by="xpath", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_type_xpath_selector(self, browser_client, browser_with_test_page):
        """Test type with XPath selector."""
        request = TypeTextRequest(
            selector="//input[@id='test-input-by-id']",
            text="XPath typed text",
            by="xpath",
            timeout=10,
        )
        result = browser_client.type_text(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Type failed: {result.message}"

    def test_wait_xpath_selector(self, browser_client, browser_with_test_page):
        """Test wait_element with XPath selector."""
        request = WaitElementRequest(
            selector="//div[@id='test-container']",
            by="xpath",
            until="visible",
            timeout=10,
        )
        result = browser_client.wait_element(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Wait failed: {result.message}"

    def test_check_element_xpath_selector(self, browser_client, browser_with_test_page):
        """Test check_element with XPath selector."""
        result = browser_client.check_element(browser_with_test_page, selector="//button[@id='test-button']", by="xpath", check="exists")
        assert result is not None
        assert result.success

        result = browser_client.check_element(browser_with_test_page, selector="//button[@id='test-button']", by="xpath", check="visible")
        assert result is not None
        assert result.success

    def test_press_keys_xpath_selector(self, browser_client, browser_with_test_page):
        """Test press_keys with XPath selector."""
        # First type something
        type_request = TypeTextRequest(
            selector="//input[@id='test-input-by-id']",
            text="test",
            by="xpath",
            timeout=10,
        )
        browser_client.type_text(browser_with_test_page, payload=type_request)

        # Then press keys
        request = PressKeysRequest(
            selector="//input[@id='test-input-by-id']",
            keys="ENTER",
            by="xpath",
        )
        result = browser_client.press_keys(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Press keys failed: {result.message}"


@pytest.mark.browser
class TestIDSelectors:
    """Test element interactions using ID selectors (by='id')."""

    def test_click_id_selector(self, browser_client, browser_with_test_page):
        """Test click with id selector."""
        request = ClickRequest(selector="test-button", by="id", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_type_id_selector(self, browser_client, browser_with_test_page):
        """Test type with id selector."""
        request = TypeTextRequest(selector="test-input-by-id", text="ID typed text", by="id", timeout=10)
        result = browser_client.type_text(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Type failed: {result.message}"

    def test_wait_id_selector(self, browser_client, browser_with_test_page):
        """Test wait_element with id selector."""
        request = WaitElementRequest(selector="test-container", by="id", until="visible", timeout=10)
        result = browser_client.wait_element(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Wait failed: {result.message}"

    def test_check_element_id_selector(self, browser_client, browser_with_test_page):
        """Test check_element with id selector."""
        result = browser_client.check_element(browser_with_test_page, selector="test-button", by="id", check="exists")
        assert result is not None
        assert result.success

    def test_press_keys_id_selector(self, browser_client, browser_with_test_page):
        """Test press_keys with id selector."""
        request = PressKeysRequest(selector="test-input-by-id", keys="TAB", by="id")
        result = browser_client.press_keys(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Press keys failed: {result.message}"


@pytest.mark.browser
class TestNameSelectors:
    """Test element interactions using name attribute selectors (by='name')."""

    def test_click_name_selector(self, browser_client, browser_with_test_page):
        """Test click with name selector."""
        request = ClickRequest(selector="test-input-by-name", by="name", timeout=10)
        result = browser_client.click(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Click failed: {result.message}"

    def test_type_name_selector(self, browser_client, browser_with_test_page):
        """Test type with name selector."""
        request = TypeTextRequest(selector="test-input-by-name", text="Name typed text", by="name", timeout=10)
        result = browser_client.type_text(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Type failed: {result.message}"

    def test_check_element_name_selector(self, browser_client, browser_with_test_page):
        """Test check_element with name selector."""
        result = browser_client.check_element(browser_with_test_page, selector="test-input-by-name", by="name", check="exists")
        assert result is not None
        assert result.success

    def test_press_keys_name_selector(self, browser_client, browser_with_test_page):
        """Test press_keys with name selector."""
        request = PressKeysRequest(selector="test-input-by-name", keys="ESCAPE", by="name")
        result = browser_client.press_keys(browser_with_test_page, payload=request)
        assert result is not None
        assert result.success, f"Press keys failed: {result.message}"


@pytest.mark.browser
class TestNonExistentSelectors:
    """Test error handling for non-existent elements with different selector types."""

    def test_click_nonexistent_css(self, browser_client, browser_with_test_page):
        """Test click on non-existent element with CSS selector returns error."""
        from airbrowser_client.exceptions import BadRequestException

        request = ClickRequest(selector="#does-not-exist", by="css", timeout=5)
        try:
            result = browser_client.click(browser_with_test_page, payload=request)
            # If no exception, should return success=false
            assert result.success is False, "Click on non-existent element should fail"
        except BadRequestException:
            pass  # Expected for HTTP 400 errors

    def test_click_nonexistent_xpath(self, browser_client, browser_with_test_page):
        """Test click on non-existent element with XPath selector returns error."""
        from airbrowser_client.exceptions import BadRequestException

        request = ClickRequest(selector="//div[@id='does-not-exist']", by="xpath", timeout=5)
        try:
            result = browser_client.click(browser_with_test_page, payload=request)
            assert result.success is False, "Click on non-existent element should fail"
        except BadRequestException:
            pass  # Expected for HTTP 400 errors

    def test_click_nonexistent_id(self, browser_client, browser_with_test_page):
        """Test click on non-existent element with id selector returns error."""
        from airbrowser_client.exceptions import BadRequestException

        request = ClickRequest(selector="does-not-exist", by="id", timeout=5)
        try:
            result = browser_client.click(browser_with_test_page, payload=request)
            assert result.success is False, "Click on non-existent element should fail"
        except BadRequestException:
            pass  # Expected for HTTP 400 errors

    def test_check_nonexistent_element(self, browser_client, browser_with_test_page):
        """Test check_element correctly reports non-existent elements."""
        # CSS - check_element should return success with found=False
        result = browser_client.check_element(browser_with_test_page, selector="#nonexistent", by="css", check="exists")
        assert result is not None
        assert result.success  # API call succeeds
        # The response data is a dict with 'found' key
        assert result.data.get("found") is False or result.data.get("exists") is False

        # XPath
        result = browser_client.check_element(browser_with_test_page, selector="//div[@id='nonexistent']", by="xpath", check="exists")
        assert result is not None
        assert result.success
        assert result.data.get("found") is False or result.data.get("exists") is False

        # ID
        result = browser_client.check_element(browser_with_test_page, selector="nonexistent", by="id", check="exists")
        assert result is not None
        assert result.success
        assert result.data.get("found") is False or result.data.get("exists") is False
