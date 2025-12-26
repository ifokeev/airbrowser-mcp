# airbrowser_client.BrowserApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**browsers**](BrowserApi.md#browsers) | **POST** /browser/browsers | Admin: list all, get info, or close all browsers
[**check_element**](BrowserApi.md#check_element) | **GET** /browser/{browser_id}/check_element | Check if element exists or is visible
[**click**](BrowserApi.md#click) | **POST** /browser/{browser_id}/click | Click element
[**close_browser**](BrowserApi.md#close_browser) | **DELETE** /browser/{browser_id}/close_browser | Close browser instance
[**console_logs**](BrowserApi.md#console_logs) | **POST** /browser/{browser_id}/console_logs | Console logs: get or clear
[**create_browser**](BrowserApi.md#create_browser) | **POST** /browser/create_browser | Create browser instance with optional persistent profile
[**detect_coordinates**](BrowserApi.md#detect_coordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using vision
[**dialog**](BrowserApi.md#dialog) | **POST** /browser/{browser_id}/dialog | Dialogs: get, accept, dismiss
[**emulate**](BrowserApi.md#emulate) | **POST** /browser/{browser_id}/emulate | Emulation: set, clear, list_devices
[**execute_script**](BrowserApi.md#execute_script) | **POST** /browser/{browser_id}/execute_script | Execute JavaScript
[**fill_form**](BrowserApi.md#fill_form) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields
[**get_content**](BrowserApi.md#get_content) | **GET** /browser/{browser_id}/get_content | Get page HTML
[**get_element_data**](BrowserApi.md#get_element_data) | **GET** /browser/{browser_id}/get_element_data | Get element text, attribute, or property
[**get_url**](BrowserApi.md#get_url) | **GET** /browser/{browser_id}/get_url | Get current URL
[**gui_click**](BrowserApi.md#gui_click) | **POST** /browser/{browser_id}/gui_click | GUI click by selector or coordinates
[**gui_hover_xy**](BrowserApi.md#gui_hover_xy) | **POST** /browser/{browser_id}/gui_hover_xy | GUI hover at coordinates
[**gui_press_keys_xy**](BrowserApi.md#gui_press_keys_xy) | **POST** /browser/{browser_id}/gui_press_keys_xy | Press keys at coordinates (click to focus, then send keys)
[**gui_type_xy**](BrowserApi.md#gui_type_xy) | **POST** /browser/{browser_id}/gui_type_xy | GUI type at coordinates - clicks then types text
[**history**](BrowserApi.md#history) | **POST** /browser/{browser_id}/history | History: back, forward, or refresh
[**mouse**](BrowserApi.md#mouse) | **POST** /browser/{browser_id}/mouse | Mouse: hover or drag
[**navigate_browser**](BrowserApi.md#navigate_browser) | **POST** /browser/{browser_id}/navigate | Navigate to URL
[**network_logs**](BrowserApi.md#network_logs) | **POST** /browser/{browser_id}/network_logs | Network logs: get or clear
[**performance**](BrowserApi.md#performance) | **POST** /browser/{browser_id}/performance | Performance: start_trace, stop_trace, metrics, analyze
[**press_keys**](BrowserApi.md#press_keys) | **POST** /browser/{browser_id}/press_keys | Press keyboard keys
[**resize**](BrowserApi.md#resize) | **POST** /browser/{browser_id}/resize | Resize viewport
[**scroll**](BrowserApi.md#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coords or by delta
[**select**](BrowserApi.md#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options
[**snapshot**](BrowserApi.md#snapshot) | **POST** /browser/{browser_id}/snapshot | DOM or accessibility snapshot
[**tabs**](BrowserApi.md#tabs) | **POST** /browser/{browser_id}/tabs | Tabs: list, new, switch, close, current
[**take_screenshot**](BrowserApi.md#take_screenshot) | **POST** /browser/{browser_id}/screenshot | Take screenshot
[**type_text**](BrowserApi.md#type_text) | **POST** /browser/{browser_id}/type | Type text into element
[**upload_file**](BrowserApi.md#upload_file) | **POST** /browser/{browser_id}/upload_file | Upload file to input
[**wait_element**](BrowserApi.md#wait_element) | **POST** /browser/{browser_id}/wait_element | Wait for element to be visible or hidden
[**what_is_visible**](BrowserApi.md#what_is_visible) | **POST** /browser/{browser_id}/what_is_visible | AI page analysis - what&#39;s visible


# **browsers**
> GenericResponse browsers(payload)

Admin: list all, get info, or close all browsers

### Example


```python
import airbrowser_client
from airbrowser_client.models.browsers_request import BrowsersRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    payload = airbrowser_client.BrowsersRequest() # BrowsersRequest | 

    try:
        # Admin: list all, get info, or close all browsers
        api_response = api_instance.browsers(payload)
        print("The response of BrowserApi->browsers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->browsers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**BrowsersRequest**](BrowsersRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_element**
> GenericResponse check_element(browser_id, selector, check, by=by)

Check if element exists or is visible

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    selector = 'selector_example' # str | selector
    check = 'check_example' # str | check
    by = 'by_example' # str | by (optional)

    try:
        # Check if element exists or is visible
        api_response = api_instance.check_element(browser_id, selector, check, by=by)
        print("The response of BrowserApi->check_element:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->check_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **selector** | **str**| selector | 
 **check** | **str**| check | 
 **by** | **str**| by | [optional] 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **click**
> GenericResponse click(browser_id, payload)

Click element

Use if_visible=True to only click if visible.

### Example


```python
import airbrowser_client
from airbrowser_client.models.click_request import ClickRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ClickRequest() # ClickRequest | 

    try:
        # Click element
        api_response = api_instance.click(browser_id, payload)
        print("The response of BrowserApi->click:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->click: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ClickRequest**](ClickRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **close_browser**
> GenericResponse close_browser(browser_id)

Close browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Close browser instance
        api_response = api_instance.close_browser(browser_id)
        print("The response of BrowserApi->close_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->close_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **console_logs**
> GenericResponse console_logs(browser_id, payload)

Console logs: get or clear

### Example


```python
import airbrowser_client
from airbrowser_client.models.console_logs_request import ConsoleLogsRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ConsoleLogsRequest() # ConsoleLogsRequest | 

    try:
        # Console logs: get or clear
        api_response = api_instance.console_logs(browser_id, payload)
        print("The response of BrowserApi->console_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->console_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ConsoleLogsRequest**](ConsoleLogsRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_browser**
> GenericResponse create_browser(payload)

Create browser instance with optional persistent profile

### Example


```python
import airbrowser_client
from airbrowser_client.models.create_browser_request import CreateBrowserRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    payload = airbrowser_client.CreateBrowserRequest() # CreateBrowserRequest | 

    try:
        # Create browser instance with optional persistent profile
        api_response = api_instance.create_browser(payload)
        print("The response of BrowserApi->create_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->create_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**CreateBrowserRequest**](CreateBrowserRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detect_coordinates**
> GenericResponse detect_coordinates(browser_id, payload)

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
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.DetectCoordinatesRequest() # DetectCoordinatesRequest | 

    try:
        # Detect element coordinates using vision
        api_response = api_instance.detect_coordinates(browser_id, payload)
        print("The response of BrowserApi->detect_coordinates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->detect_coordinates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**DetectCoordinatesRequest**](DetectCoordinatesRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dialog**
> GenericResponse dialog(browser_id, payload)

Dialogs: get, accept, dismiss

### Example


```python
import airbrowser_client
from airbrowser_client.models.dialog_request import DialogRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.DialogRequest() # DialogRequest | 

    try:
        # Dialogs: get, accept, dismiss
        api_response = api_instance.dialog(browser_id, payload)
        print("The response of BrowserApi->dialog:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->dialog: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**DialogRequest**](DialogRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **emulate**
> GenericResponse emulate(browser_id, payload)

Emulation: set, clear, list_devices

### Example


```python
import airbrowser_client
from airbrowser_client.models.emulate_request import EmulateRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.EmulateRequest() # EmulateRequest | 

    try:
        # Emulation: set, clear, list_devices
        api_response = api_instance.emulate(browser_id, payload)
        print("The response of BrowserApi->emulate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->emulate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**EmulateRequest**](EmulateRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_script**
> GenericResponse execute_script(browser_id, payload)

Execute JavaScript

### Example


```python
import airbrowser_client
from airbrowser_client.models.execute_script_request import ExecuteScriptRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ExecuteScriptRequest() # ExecuteScriptRequest | 

    try:
        # Execute JavaScript
        api_response = api_instance.execute_script(browser_id, payload)
        print("The response of BrowserApi->execute_script:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->execute_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ExecuteScriptRequest**](ExecuteScriptRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fill_form**
> GenericResponse fill_form(browser_id, payload)

Fill multiple form fields

### Example


```python
import airbrowser_client
from airbrowser_client.models.fill_form_request import FillFormRequest
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.FillFormRequest() # FillFormRequest | 

    try:
        # Fill multiple form fields
        api_response = api_instance.fill_form(browser_id, payload)
        print("The response of BrowserApi->fill_form:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->fill_form: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**FillFormRequest**](FillFormRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_content**
> GenericResponse get_content(browser_id)

Get page HTML

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Get page HTML
        api_response = api_instance.get_content(browser_id)
        print("The response of BrowserApi->get_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_element_data**
> GenericResponse get_element_data(browser_id, selector, data_type, name=name, by=by)

Get element text, attribute, or property

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    selector = 'selector_example' # str | selector
    data_type = 'data_type_example' # str | data_type
    name = 'name_example' # str | name (optional)
    by = 'by_example' # str | by (optional)

    try:
        # Get element text, attribute, or property
        api_response = api_instance.get_element_data(browser_id, selector, data_type, name=name, by=by)
        print("The response of BrowserApi->get_element_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_element_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **selector** | **str**| selector | 
 **data_type** | **str**| data_type | 
 **name** | **str**| name | [optional] 
 **by** | **str**| by | [optional] 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_url**
> GenericResponse get_url(browser_id)

Get current URL

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # Get current URL
        api_response = api_instance.get_url(browser_id)
        print("The response of BrowserApi->get_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_click**
> GenericResponse gui_click(browser_id, payload)

GUI click by selector or coordinates

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiClickRequest() # GuiClickRequest | 

    try:
        # GUI click by selector or coordinates
        api_response = api_instance.gui_click(browser_id, payload)
        print("The response of BrowserApi->gui_click:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->gui_click: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiClickRequest**](GuiClickRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_hover_xy**
> GenericResponse gui_hover_xy(browser_id, payload)

GUI hover at coordinates

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiHoverXyRequest() # GuiHoverXyRequest | 

    try:
        # GUI hover at coordinates
        api_response = api_instance.gui_hover_xy(browser_id, payload)
        print("The response of BrowserApi->gui_hover_xy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->gui_hover_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiHoverXyRequest**](GuiHoverXyRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_press_keys_xy**
> GenericResponse gui_press_keys_xy(browser_id, payload)

Press keys at coordinates (click to focus, then send keys)

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiPressKeysXyRequest() # GuiPressKeysXyRequest | 

    try:
        # Press keys at coordinates (click to focus, then send keys)
        api_response = api_instance.gui_press_keys_xy(browser_id, payload)
        print("The response of BrowserApi->gui_press_keys_xy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->gui_press_keys_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiPressKeysXyRequest**](GuiPressKeysXyRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gui_type_xy**
> GenericResponse gui_type_xy(browser_id, payload)

GUI type at coordinates - clicks then types text

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.GuiTypeXyRequest() # GuiTypeXyRequest | 

    try:
        # GUI type at coordinates - clicks then types text
        api_response = api_instance.gui_type_xy(browser_id, payload)
        print("The response of BrowserApi->gui_type_xy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->gui_type_xy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**GuiTypeXyRequest**](GuiTypeXyRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **history**
> GenericResponse history(browser_id, payload)

History: back, forward, or refresh

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.HistoryRequest() # HistoryRequest | 

    try:
        # History: back, forward, or refresh
        api_response = api_instance.history(browser_id, payload)
        print("The response of BrowserApi->history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**HistoryRequest**](HistoryRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mouse**
> GenericResponse mouse(browser_id, payload)

Mouse: hover or drag

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.MouseRequest() # MouseRequest | 

    try:
        # Mouse: hover or drag
        api_response = api_instance.mouse(browser_id, payload)
        print("The response of BrowserApi->mouse:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->mouse: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**MouseRequest**](MouseRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **navigate_browser**
> GenericResponse navigate_browser(browser_id, payload)

Navigate to URL

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.NavigateBrowserRequest() # NavigateBrowserRequest | 

    try:
        # Navigate to URL
        api_response = api_instance.navigate_browser(browser_id, payload)
        print("The response of BrowserApi->navigate_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->navigate_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**NavigateBrowserRequest**](NavigateBrowserRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **network_logs**
> GenericResponse network_logs(browser_id, payload)

Network logs: get or clear

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.NetworkLogsRequest() # NetworkLogsRequest | 

    try:
        # Network logs: get or clear
        api_response = api_instance.network_logs(browser_id, payload)
        print("The response of BrowserApi->network_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->network_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**NetworkLogsRequest**](NetworkLogsRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **performance**
> GenericResponse performance(browser_id, payload)

Performance: start_trace, stop_trace, metrics, analyze

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.PerformanceRequest() # PerformanceRequest | 

    try:
        # Performance: start_trace, stop_trace, metrics, analyze
        api_response = api_instance.performance(browser_id, payload)
        print("The response of BrowserApi->performance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->performance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**PerformanceRequest**](PerformanceRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **press_keys**
> GenericResponse press_keys(browser_id, payload)

Press keyboard keys

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.PressKeysRequest() # PressKeysRequest | 

    try:
        # Press keyboard keys
        api_response = api_instance.press_keys(browser_id, payload)
        print("The response of BrowserApi->press_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->press_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**PressKeysRequest**](PressKeysRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resize**
> GenericResponse resize(browser_id, payload)

Resize viewport

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ResizeRequest() # ResizeRequest | 

    try:
        # Resize viewport
        api_response = api_instance.resize(browser_id, payload)
        print("The response of BrowserApi->resize:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->resize: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ResizeRequest**](ResizeRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scroll**
> GenericResponse scroll(browser_id, payload)

Scroll to element/coords or by delta

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.ScrollRequest() # ScrollRequest | 

    try:
        # Scroll to element/coords or by delta
        api_response = api_instance.scroll(browser_id, payload)
        print("The response of BrowserApi->scroll:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->scroll: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**ScrollRequest**](ScrollRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **select**
> GenericResponse select(browser_id, payload)

Select dropdown: select option or get options

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.SelectRequest() # SelectRequest | 

    try:
        # Select dropdown: select option or get options
        api_response = api_instance.select(browser_id, payload)
        print("The response of BrowserApi->select:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->select: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**SelectRequest**](SelectRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **snapshot**
> GenericResponse snapshot(browser_id, payload)

DOM or accessibility snapshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.SnapshotRequest() # SnapshotRequest | 

    try:
        # DOM or accessibility snapshot
        api_response = api_instance.snapshot(browser_id, payload)
        print("The response of BrowserApi->snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**SnapshotRequest**](SnapshotRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tabs**
> GenericResponse tabs(browser_id, payload)

Tabs: list, new, switch, close, current

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TabsRequest() # TabsRequest | 

    try:
        # Tabs: list, new, switch, close, current
        api_response = api_instance.tabs(browser_id, payload)
        print("The response of BrowserApi->tabs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->tabs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TabsRequest**](TabsRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **take_screenshot**
> GenericResponse take_screenshot(browser_id, payload)

Take screenshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TakeScreenshotRequest() # TakeScreenshotRequest | 

    try:
        # Take screenshot
        api_response = api_instance.take_screenshot(browser_id, payload)
        print("The response of BrowserApi->take_screenshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->take_screenshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TakeScreenshotRequest**](TakeScreenshotRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **type_text**
> GenericResponse type_text(browser_id, payload)

Type text into element

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.TypeTextRequest() # TypeTextRequest | 

    try:
        # Type text into element
        api_response = api_instance.type_text(browser_id, payload)
        print("The response of BrowserApi->type_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->type_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**TypeTextRequest**](TypeTextRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_file**
> GenericResponse upload_file(browser_id, payload)

Upload file to input

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.UploadFileRequest() # UploadFileRequest | 

    try:
        # Upload file to input
        api_response = api_instance.upload_file(browser_id, payload)
        print("The response of BrowserApi->upload_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**UploadFileRequest**](UploadFileRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **wait_element**
> GenericResponse wait_element(browser_id, payload)

Wait for element to be visible or hidden

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 
    payload = airbrowser_client.WaitElementRequest() # WaitElementRequest | 

    try:
        # Wait for element to be visible or hidden
        api_response = api_instance.wait_element(browser_id, payload)
        print("The response of BrowserApi->wait_element:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->wait_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 
 **payload** | [**WaitElementRequest**](WaitElementRequest.md)|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **what_is_visible**
> GenericResponse what_is_visible(browser_id)

AI page analysis - what's visible

### Example


```python
import airbrowser_client
from airbrowser_client.models.generic_response import GenericResponse
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | 

    try:
        # AI page analysis - what's visible
        api_response = api_instance.what_is_visible(browser_id)
        print("The response of BrowserApi->what_is_visible:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->what_is_visible: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**|  | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

