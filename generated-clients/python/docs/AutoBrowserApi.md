# airbrowser_client.AutoBrowserApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**browsers**](AutoBrowserApi.md#browsers) | **POST** /browser/browsers | Admin: list all, get info, or close all browsers
[**check_element**](AutoBrowserApi.md#check_element) | **GET** /browser/{browser_id}/check_element | Check if element exists or is visible
[**click**](AutoBrowserApi.md#click) | **POST** /browser/{browser_id}/click | Click element
[**close_browser**](AutoBrowserApi.md#close_browser) | **DELETE** /browser/{browser_id}/close_browser | Close browser instance
[**console_logs**](AutoBrowserApi.md#console_logs) | **POST** /browser/{browser_id}/console_logs | Console logs: get or clear
[**create_browser**](AutoBrowserApi.md#create_browser) | **POST** /browser/create_browser | Create browser instance
[**detect_coordinates**](AutoBrowserApi.md#detect_coordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using vision
[**dialog**](AutoBrowserApi.md#dialog) | **POST** /browser/{browser_id}/dialog | Dialogs: get, accept, dismiss
[**emulate**](AutoBrowserApi.md#emulate) | **POST** /browser/{browser_id}/emulate | Emulation: set, clear, list_devices
[**execute_script**](AutoBrowserApi.md#execute_script) | **POST** /browser/{browser_id}/execute_script | Execute JavaScript
[**fill_form**](AutoBrowserApi.md#fill_form) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields
[**get_content**](AutoBrowserApi.md#get_content) | **GET** /browser/{browser_id}/get_content | Get page HTML
[**get_element_data**](AutoBrowserApi.md#get_element_data) | **GET** /browser/{browser_id}/get_element_data | Get element text, attribute, or property
[**get_url**](AutoBrowserApi.md#get_url) | **GET** /browser/{browser_id}/get_url | Get current URL
[**gui_click**](AutoBrowserApi.md#gui_click) | **POST** /browser/{browser_id}/gui_click | GUI click by selector or coordinates
[**gui_hover_xy**](AutoBrowserApi.md#gui_hover_xy) | **POST** /browser/{browser_id}/gui_hover_xy | GUI hover at coordinates
[**gui_press_keys_xy**](AutoBrowserApi.md#gui_press_keys_xy) | **POST** /browser/{browser_id}/gui_press_keys_xy | Press keys at coordinates (click to focus, then send keys)
[**gui_type_xy**](AutoBrowserApi.md#gui_type_xy) | **POST** /browser/{browser_id}/gui_type_xy | GUI type at coordinates - clicks then types text
[**history**](AutoBrowserApi.md#history) | **POST** /browser/{browser_id}/history | History: back, forward, or refresh
[**mouse**](AutoBrowserApi.md#mouse) | **POST** /browser/{browser_id}/mouse | Mouse: hover or drag
[**navigate_browser**](AutoBrowserApi.md#navigate_browser) | **POST** /browser/{browser_id}/navigate | Navigate to URL
[**network_logs**](AutoBrowserApi.md#network_logs) | **POST** /browser/{browser_id}/network_logs | Network logs: get or clear
[**performance**](AutoBrowserApi.md#performance) | **POST** /browser/{browser_id}/performance | Performance: start_trace, stop_trace, metrics, analyze
[**press_keys**](AutoBrowserApi.md#press_keys) | **POST** /browser/{browser_id}/press_keys | Press keyboard keys
[**resize**](AutoBrowserApi.md#resize) | **POST** /browser/{browser_id}/resize | Resize viewport
[**scroll**](AutoBrowserApi.md#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coords or by delta
[**select**](AutoBrowserApi.md#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options
[**snapshot**](AutoBrowserApi.md#snapshot) | **POST** /browser/{browser_id}/snapshot | DOM or accessibility snapshot
[**tabs**](AutoBrowserApi.md#tabs) | **POST** /browser/{browser_id}/tabs | Tabs: list, new, switch, close, current
[**take_screenshot**](AutoBrowserApi.md#take_screenshot) | **POST** /browser/{browser_id}/screenshot | Take screenshot
[**type_text**](AutoBrowserApi.md#type_text) | **POST** /browser/{browser_id}/type | Type text into element
[**upload_file**](AutoBrowserApi.md#upload_file) | **POST** /browser/{browser_id}/upload_file | Upload file to input
[**wait_element**](AutoBrowserApi.md#wait_element) | **POST** /browser/{browser_id}/wait_element | Wait for element to be visible or hidden
[**what_is_visible**](AutoBrowserApi.md#what_is_visible) | **POST** /browser/{browser_id}/what_is_visible | AI page analysis - what&#39;s visible


# **browsers**
> browsers(payload)

Admin: list all, get info, or close all browsers

### Example


```python
import airbrowser_client
from airbrowser_client.models.browsers_request import BrowsersRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    payload = airbrowser_client.BrowsersRequest() # BrowsersRequest | 

    try:
        # Admin: list all, get info, or close all browsers
        api_instance.browsers(payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->browsers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**BrowsersRequest**](BrowsersRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_element**
> check_element(browser_id)

Check if element exists or is visible

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Check if element exists or is visible
        api_instance.check_element(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->check_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **click**
> click(browser_id, payload)

Click element

Use if_visible=True to only click if visible.

### Example


```python
import airbrowser_client
from airbrowser_client.models.click_request import ClickRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ClickRequest() # ClickRequest | 

    try:
        # Click element
        api_instance.click(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->click: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ClickRequest**](ClickRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **close_browser**
> close_browser(browser_id)

Close browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Close browser instance
        api_instance.close_browser(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->close_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **console_logs**
> console_logs(browser_id, payload)

Console logs: get or clear

### Example


```python
import airbrowser_client
from airbrowser_client.models.console_logs_request import ConsoleLogsRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ConsoleLogsRequest() # ConsoleLogsRequest | 

    try:
        # Console logs: get or clear
        api_instance.console_logs(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->console_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ConsoleLogsRequest**](ConsoleLogsRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_browser**
> create_browser(payload)

Create browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.models.create_browser_request import CreateBrowserRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    payload = airbrowser_client.CreateBrowserRequest() # CreateBrowserRequest | 

    try:
        # Create browser instance
        api_instance.create_browser(payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->create_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**CreateBrowserRequest**](CreateBrowserRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detect_coordinates**
> detect_coordinates(browser_id, payload)

Detect element coordinates using vision

Args:
    browser_id: Browser instance identifier
    prompt: Natural language description of element to find
    fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right).
        Use fx=0.2 for wide elements with icons on the right (like Google search).
    fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom)

### Example


```python
import airbrowser_client
from airbrowser_client.models.detect_coordinates_request import DetectCoordinatesRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.DetectCoordinatesRequest() # DetectCoordinatesRequest | 

    try:
        # Detect element coordinates using vision
        api_instance.detect_coordinates(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->detect_coordinates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**DetectCoordinatesRequest**](DetectCoordinatesRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dialog**
> dialog(browser_id, payload)

Dialogs: get, accept, dismiss

### Example


```python
import airbrowser_client
from airbrowser_client.models.dialog_request import DialogRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.DialogRequest() # DialogRequest | 

    try:
        # Dialogs: get, accept, dismiss
        api_instance.dialog(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->dialog: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**DialogRequest**](DialogRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **emulate**
> emulate(browser_id, payload)

Emulation: set, clear, list_devices

### Example


```python
import airbrowser_client
from airbrowser_client.models.emulate_request import EmulateRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.EmulateRequest() # EmulateRequest | 

    try:
        # Emulation: set, clear, list_devices
        api_instance.emulate(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->emulate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**EmulateRequest**](EmulateRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_script**
> execute_script(browser_id, payload)

Execute JavaScript

### Example


```python
import airbrowser_client
from airbrowser_client.models.execute_script_request import ExecuteScriptRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ExecuteScriptRequest() # ExecuteScriptRequest | 

    try:
        # Execute JavaScript
        api_instance.execute_script(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->execute_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ExecuteScriptRequest**](ExecuteScriptRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fill_form**
> fill_form(browser_id, payload)

Fill multiple form fields

### Example


```python
import airbrowser_client
from airbrowser_client.models.fill_form_request import FillFormRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.FillFormRequest() # FillFormRequest | 

    try:
        # Fill multiple form fields
        api_instance.fill_form(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->fill_form: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**FillFormRequest**](FillFormRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_content**
> get_content(browser_id)

Get page HTML

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Get page HTML
        api_instance.get_content(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->get_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_element_data**
> get_element_data(browser_id)

Get element text, attribute, or property

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Get element text, attribute, or property
        api_instance.get_element_data(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->get_element_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_url**
> get_url(browser_id)

Get current URL

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Get current URL
        api_instance.get_url(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->get_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_click**
> gui_click(browser_id, payload)

GUI click by selector or coordinates

### Example


```python
import airbrowser_client
from airbrowser_client.models.gui_click_request import GuiClickRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiClickRequest() # GuiClickRequest | 

    try:
        # GUI click by selector or coordinates
        api_instance.gui_click(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->gui_click: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiClickRequest**](GuiClickRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_hover_xy**
> gui_hover_xy(browser_id, payload)

GUI hover at coordinates

### Example


```python
import airbrowser_client
from airbrowser_client.models.gui_hover_xy_request import GuiHoverXyRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiHoverXyRequest() # GuiHoverXyRequest | 

    try:
        # GUI hover at coordinates
        api_instance.gui_hover_xy(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->gui_hover_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiHoverXyRequest**](GuiHoverXyRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_press_keys_xy**
> gui_press_keys_xy(browser_id, payload)

Press keys at coordinates (click to focus, then send keys)

### Example


```python
import airbrowser_client
from airbrowser_client.models.gui_press_keys_xy_request import GuiPressKeysXyRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiPressKeysXyRequest() # GuiPressKeysXyRequest | 

    try:
        # Press keys at coordinates (click to focus, then send keys)
        api_instance.gui_press_keys_xy(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->gui_press_keys_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiPressKeysXyRequest**](GuiPressKeysXyRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_type_xy**
> gui_type_xy(browser_id, payload)

GUI type at coordinates - clicks then types text

### Example


```python
import airbrowser_client
from airbrowser_client.models.gui_type_xy_request import GuiTypeXyRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiTypeXyRequest() # GuiTypeXyRequest | 

    try:
        # GUI type at coordinates - clicks then types text
        api_instance.gui_type_xy(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->gui_type_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiTypeXyRequest**](GuiTypeXyRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **history**
> history(browser_id, payload)

History: back, forward, or refresh

### Example


```python
import airbrowser_client
from airbrowser_client.models.history_request import HistoryRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.HistoryRequest() # HistoryRequest | 

    try:
        # History: back, forward, or refresh
        api_instance.history(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**HistoryRequest**](HistoryRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mouse**
> mouse(browser_id, payload)

Mouse: hover or drag

### Example


```python
import airbrowser_client
from airbrowser_client.models.mouse_request import MouseRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.MouseRequest() # MouseRequest | 

    try:
        # Mouse: hover or drag
        api_instance.mouse(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->mouse: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**MouseRequest**](MouseRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **navigate_browser**
> navigate_browser(browser_id, payload)

Navigate to URL

### Example


```python
import airbrowser_client
from airbrowser_client.models.navigate_browser_request import NavigateBrowserRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.NavigateBrowserRequest() # NavigateBrowserRequest | 

    try:
        # Navigate to URL
        api_instance.navigate_browser(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->navigate_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**NavigateBrowserRequest**](NavigateBrowserRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **network_logs**
> network_logs(browser_id, payload)

Network logs: get or clear

### Example


```python
import airbrowser_client
from airbrowser_client.models.network_logs_request import NetworkLogsRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.NetworkLogsRequest() # NetworkLogsRequest | 

    try:
        # Network logs: get or clear
        api_instance.network_logs(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->network_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**NetworkLogsRequest**](NetworkLogsRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **performance**
> performance(browser_id, payload)

Performance: start_trace, stop_trace, metrics, analyze

### Example


```python
import airbrowser_client
from airbrowser_client.models.performance_request import PerformanceRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.PerformanceRequest() # PerformanceRequest | 

    try:
        # Performance: start_trace, stop_trace, metrics, analyze
        api_instance.performance(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->performance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**PerformanceRequest**](PerformanceRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **press_keys**
> press_keys(browser_id, payload)

Press keyboard keys

### Example


```python
import airbrowser_client
from airbrowser_client.models.press_keys_request import PressKeysRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.PressKeysRequest() # PressKeysRequest | 

    try:
        # Press keyboard keys
        api_instance.press_keys(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->press_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**PressKeysRequest**](PressKeysRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resize**
> resize(browser_id, payload)

Resize viewport

### Example


```python
import airbrowser_client
from airbrowser_client.models.resize_request import ResizeRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ResizeRequest() # ResizeRequest | 

    try:
        # Resize viewport
        api_instance.resize(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->resize: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ResizeRequest**](ResizeRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scroll**
> scroll(browser_id, payload)

Scroll to element/coords or by delta

### Example


```python
import airbrowser_client
from airbrowser_client.models.scroll_request import ScrollRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ScrollRequest() # ScrollRequest | 

    try:
        # Scroll to element/coords or by delta
        api_instance.scroll(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->scroll: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ScrollRequest**](ScrollRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **select**
> select(browser_id, payload)

Select dropdown: select option or get options

### Example


```python
import airbrowser_client
from airbrowser_client.models.select_request import SelectRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.SelectRequest() # SelectRequest | 

    try:
        # Select dropdown: select option or get options
        api_instance.select(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->select: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**SelectRequest**](SelectRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **snapshot**
> snapshot(browser_id, payload)

DOM or accessibility snapshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.snapshot_request import SnapshotRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.SnapshotRequest() # SnapshotRequest | 

    try:
        # DOM or accessibility snapshot
        api_instance.snapshot(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**SnapshotRequest**](SnapshotRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tabs**
> tabs(browser_id, payload)

Tabs: list, new, switch, close, current

### Example


```python
import airbrowser_client
from airbrowser_client.models.tabs_request import TabsRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TabsRequest() # TabsRequest | 

    try:
        # Tabs: list, new, switch, close, current
        api_instance.tabs(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->tabs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TabsRequest**](TabsRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **take_screenshot**
> take_screenshot(browser_id, payload)

Take screenshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.take_screenshot_request import TakeScreenshotRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TakeScreenshotRequest() # TakeScreenshotRequest | 

    try:
        # Take screenshot
        api_instance.take_screenshot(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->take_screenshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TakeScreenshotRequest**](TakeScreenshotRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **type_text**
> type_text(browser_id, payload)

Type text into element

### Example


```python
import airbrowser_client
from airbrowser_client.models.type_text_request import TypeTextRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TypeTextRequest() # TypeTextRequest | 

    try:
        # Type text into element
        api_instance.type_text(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->type_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TypeTextRequest**](TypeTextRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> upload_file(browser_id, payload)

Upload file to input

### Example


```python
import airbrowser_client
from airbrowser_client.models.upload_file_request import UploadFileRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.UploadFileRequest() # UploadFileRequest | 

    try:
        # Upload file to input
        api_instance.upload_file(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**UploadFileRequest**](UploadFileRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **wait_element**
> wait_element(browser_id, payload)

Wait for element to be visible or hidden

### Example


```python
import airbrowser_client
from airbrowser_client.models.wait_element_request import WaitElementRequest
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.WaitElementRequest() # WaitElementRequest | 

    try:
        # Wait for element to be visible or hidden
        api_instance.wait_element(browser_id, payload)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->wait_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**WaitElementRequest**](WaitElementRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **what_is_visible**
> what_is_visible(browser_id)

AI page analysis - what's visible

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.AutoBrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # AI page analysis - what's visible
        api_instance.what_is_visible(browser_id)
    except Exception as e:
        print("Exception when calling AutoBrowserApi->what_is_visible: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

