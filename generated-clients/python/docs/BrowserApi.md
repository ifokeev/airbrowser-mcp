# airbrowser_client.BrowserApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**check_element**](BrowserApi.md#check_element) | **POST** /browser/{browser_id}/check_element | Check if element exists or is visible
[**click**](BrowserApi.md#click) | **POST** /browser/{browser_id}/click | Click element
[**close_all_browsers**](BrowserApi.md#close_all_browsers) | **POST** /browser/close_all | Close all active browser instances
[**close_browser**](BrowserApi.md#close_browser) | **POST** /browser/{browser_id}/close | Close a browser instance
[**console_logs**](BrowserApi.md#console_logs) | **POST** /browser/{browser_id}/console | Get or clear console logs
[**create_browser**](BrowserApi.md#create_browser) | **POST** /browser/create | Create a new browser instance
[**delete_browser**](BrowserApi.md#delete_browser) | **DELETE** /browser/{browser_id} | Close and remove a browser instance
[**detect_coordinates**](BrowserApi.md#detect_coordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using AI vision
[**dialog**](BrowserApi.md#dialog) | **POST** /browser/{browser_id}/dialog | Manage browser dialogs: get, accept, or dismiss
[**emulate**](BrowserApi.md#emulate) | **POST** /browser/{browser_id}/emulate | Manage device emulation: set, clear, or list_devices
[**execute_script**](BrowserApi.md#execute_script) | **POST** /browser/{browser_id}/execute | Execute JavaScript
[**fill_form**](BrowserApi.md#fill_form) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields
[**get_browser**](BrowserApi.md#get_browser) | **GET** /browser/{browser_id} | Get browser instance details
[**get_browser_status**](BrowserApi.md#get_browser_status) | **GET** /browser/{browser_id}/status | Get browser status
[**get_content**](BrowserApi.md#get_content) | **GET** /browser/{browser_id}/content | Get page HTML content
[**get_element_data**](BrowserApi.md#get_element_data) | **POST** /browser/{browser_id}/element_data | Get element text, attribute, or property
[**get_pool_status**](BrowserApi.md#get_pool_status) | **GET** /browser/pool/status | Get browser pool status
[**get_url**](BrowserApi.md#get_url) | **GET** /browser/{browser_id}/url | Get current page URL
[**gui_click**](BrowserApi.md#gui_click) | **POST** /browser/{browser_id}/gui_click | Click using selector or screen coordinates
[**history**](BrowserApi.md#history) | **POST** /browser/{browser_id}/history | Execute history action: back, forward, or refresh
[**list_browsers**](BrowserApi.md#list_browsers) | **GET** /browser/list | List all active browser instances
[**mouse**](BrowserApi.md#mouse) | **POST** /browser/{browser_id}/mouse | Mouse action: hover or drag
[**navigate_browser**](BrowserApi.md#navigate_browser) | **POST** /browser/{browser_id}/navigate | Navigate to a URL
[**network_logs**](BrowserApi.md#network_logs) | **POST** /browser/{browser_id}/network | Get or clear network logs
[**performance**](BrowserApi.md#performance) | **POST** /browser/{browser_id}/performance | Manage performance: start_trace, stop_trace, metrics, or analyze
[**press_keys**](BrowserApi.md#press_keys) | **POST** /browser/{browser_id}/press_keys | Press keys on an element
[**resize**](BrowserApi.md#resize) | **POST** /browser/{browser_id}/resize | Resize viewport
[**scroll**](BrowserApi.md#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coordinates (absolute) or by delta (relative)
[**select**](BrowserApi.md#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options
[**tabs**](BrowserApi.md#tabs) | **POST** /browser/{browser_id}/tabs | Manage browser tabs: list, new, switch, close, or current
[**take_screenshot**](BrowserApi.md#take_screenshot) | **POST** /browser/{browser_id}/screenshot | Take a screenshot
[**take_snapshot**](BrowserApi.md#take_snapshot) | **POST** /browser/{browser_id}/snapshot | Take DOM/accessibility snapshot
[**type_text**](BrowserApi.md#type_text) | **POST** /browser/{browser_id}/type | Type text into an element
[**upload_file**](BrowserApi.md#upload_file) | **POST** /browser/{browser_id}/upload_file | Upload a file
[**wait_element**](BrowserApi.md#wait_element) | **POST** /browser/{browser_id}/wait_element | Wait for element to become visible or hidden
[**what_is_visible**](BrowserApi.md#what_is_visible) | **GET** /browser/{browser_id}/what_is_visible | Analyze visible page content using AI


# **check_element**
> SuccessResponse check_element(browser_id, payload)

Check if element exists or is visible

### Example


```python
import airbrowser_client
from airbrowser_client.models.check_element_request import CheckElementRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.CheckElementRequest() # CheckElementRequest | 

    try:
        # Check if element exists or is visible
        api_response = api_instance.check_element(browser_id, payload)
        print("The response of BrowserApi->check_element:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->check_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**CheckElementRequest**](CheckElementRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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

# **click**
> ActionResult click(browser_id, payload)

Click element

Use if_visible=true to only click if visible.

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
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
    api_instance = airbrowser_client.BrowserApi(api_client)
    browser_id = 'browser_id_example' # str | Unique browser identifier
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
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**ClickRequest**](ClickRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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

# **close_all_browsers**
> BaseResponse close_all_browsers()

Close all active browser instances

### Example


```python
import airbrowser_client
from airbrowser_client.models.base_response import BaseResponse
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

    try:
        # Close all active browser instances
        api_response = api_instance.close_all_browsers()
        print("The response of BrowserApi->close_all_browsers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->close_all_browsers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BaseResponse**](BaseResponse.md)

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

# **close_browser**
> BaseResponse close_browser(browser_id)

Close a browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.models.base_response import BaseResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Close a browser instance
        api_response = api_instance.close_browser(browser_id)
        print("The response of BrowserApi->close_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->close_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**BaseResponse**](BaseResponse.md)

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
> LogsResponse console_logs(browser_id, payload)

Get or clear console logs

### Example


```python
import airbrowser_client
from airbrowser_client.models.console_logs_request import ConsoleLogsRequest
from airbrowser_client.models.logs_response import LogsResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.ConsoleLogsRequest() # ConsoleLogsRequest | 

    try:
        # Get or clear console logs
        api_response = api_instance.console_logs(browser_id, payload)
        print("The response of BrowserApi->console_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->console_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**ConsoleLogsRequest**](ConsoleLogsRequest.md)|  | 

### Return type

[**LogsResponse**](LogsResponse.md)

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
> BrowserCreated create_browser(payload)

Create a new browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.models.browser_config import BrowserConfig
from airbrowser_client.models.browser_created import BrowserCreated
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
    payload = airbrowser_client.BrowserConfig() # BrowserConfig | 

    try:
        # Create a new browser instance
        api_response = api_instance.create_browser(payload)
        print("The response of BrowserApi->create_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->create_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**BrowserConfig**](BrowserConfig.md)|  | 

### Return type

[**BrowserCreated**](BrowserCreated.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**400** | Bad request |  -  |
**200** | Browser created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_browser**
> BaseResponse delete_browser(browser_id)

Close and remove a browser instance

### Example


```python
import airbrowser_client
from airbrowser_client.models.base_response import BaseResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Close and remove a browser instance
        api_response = api_instance.delete_browser(browser_id)
        print("The response of BrowserApi->delete_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->delete_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**BaseResponse**](BaseResponse.md)

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

# **detect_coordinates**
> DetectCoordinatesResult detect_coordinates(browser_id, payload)

Detect element coordinates using AI vision

### Example


```python
import airbrowser_client
from airbrowser_client.models.detect_coordinates_request import DetectCoordinatesRequest
from airbrowser_client.models.detect_coordinates_result import DetectCoordinatesResult
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.DetectCoordinatesRequest() # DetectCoordinatesRequest | 

    try:
        # Detect element coordinates using AI vision
        api_response = api_instance.detect_coordinates(browser_id, payload)
        print("The response of BrowserApi->detect_coordinates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->detect_coordinates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**DetectCoordinatesRequest**](DetectCoordinatesRequest.md)|  | 

### Return type

[**DetectCoordinatesResult**](DetectCoordinatesResult.md)

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
> SuccessResponse dialog(browser_id, payload)

Manage browser dialogs: get, accept, or dismiss

### Example


```python
import airbrowser_client
from airbrowser_client.models.combined_dialog_request import CombinedDialogRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.CombinedDialogRequest() # CombinedDialogRequest | 

    try:
        # Manage browser dialogs: get, accept, or dismiss
        api_response = api_instance.dialog(browser_id, payload)
        print("The response of BrowserApi->dialog:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->dialog: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**CombinedDialogRequest**](CombinedDialogRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> SuccessResponse emulate(browser_id, payload)

Manage device emulation: set, clear, or list_devices

### Example


```python
import airbrowser_client
from airbrowser_client.models.combined_emulate_request import CombinedEmulateRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.CombinedEmulateRequest() # CombinedEmulateRequest | 

    try:
        # Manage device emulation: set, clear, or list_devices
        api_response = api_instance.emulate(browser_id, payload)
        print("The response of BrowserApi->emulate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->emulate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**CombinedEmulateRequest**](CombinedEmulateRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ExecuteResponse execute_script(browser_id, payload)

Execute JavaScript

### Example


```python
import airbrowser_client
from airbrowser_client.models.execute_request import ExecuteRequest
from airbrowser_client.models.execute_response import ExecuteResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.ExecuteRequest() # ExecuteRequest | 

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
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**ExecuteRequest**](ExecuteRequest.md)|  | 

### Return type

[**ExecuteResponse**](ExecuteResponse.md)

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
> SuccessResponse fill_form(browser_id, payload)

Fill multiple form fields

### Example


```python
import airbrowser_client
from airbrowser_client.models.fill_form_request import FillFormRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
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
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**FillFormRequest**](FillFormRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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

# **get_browser**
> BrowserInfoResponse get_browser(browser_id)

Get browser instance details

### Example


```python
import airbrowser_client
from airbrowser_client.models.browser_info_response import BrowserInfoResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Get browser instance details
        api_response = api_instance.get_browser(browser_id)
        print("The response of BrowserApi->get_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**BrowserInfoResponse**](BrowserInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**404** | Browser not found |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_browser_status**
> BrowserInfoResponse get_browser_status(browser_id)

Get browser status

### Example


```python
import airbrowser_client
from airbrowser_client.models.browser_info_response import BrowserInfoResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Get browser status
        api_response = api_instance.get_browser_status(browser_id)
        print("The response of BrowserApi->get_browser_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_browser_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**BrowserInfoResponse**](BrowserInfoResponse.md)

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

# **get_content**
> ContentResponse get_content(browser_id)

Get page HTML content

### Example


```python
import airbrowser_client
from airbrowser_client.models.content_response import ContentResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Get page HTML content
        api_response = api_instance.get_content(browser_id)
        print("The response of BrowserApi->get_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**ContentResponse**](ContentResponse.md)

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
> AttributeResponse get_element_data(browser_id, payload)

Get element text, attribute, or property

### Example


```python
import airbrowser_client
from airbrowser_client.models.attribute_response import AttributeResponse
from airbrowser_client.models.element_data_request import ElementDataRequest
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.ElementDataRequest() # ElementDataRequest | 

    try:
        # Get element text, attribute, or property
        api_response = api_instance.get_element_data(browser_id, payload)
        print("The response of BrowserApi->get_element_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_element_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**ElementDataRequest**](ElementDataRequest.md)|  | 

### Return type

[**AttributeResponse**](AttributeResponse.md)

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

# **get_pool_status**
> PoolStatusResponse get_pool_status()

Get browser pool status

### Example


```python
import airbrowser_client
from airbrowser_client.models.pool_status_response import PoolStatusResponse
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

    try:
        # Get browser pool status
        api_response = api_instance.get_pool_status()
        print("The response of BrowserApi->get_pool_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_pool_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PoolStatusResponse**](PoolStatusResponse.md)

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
> UrlResponse get_url(browser_id)

Get current page URL

### Example


```python
import airbrowser_client
from airbrowser_client.models.url_response import UrlResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Get current page URL
        api_response = api_instance.get_url(browser_id)
        print("The response of BrowserApi->get_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->get_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**UrlResponse**](UrlResponse.md)

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
> ActionResult gui_click(browser_id, payload)

Click using selector or screen coordinates

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
from airbrowser_client.models.combined_gui_click_request import CombinedGuiClickRequest
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.CombinedGuiClickRequest() # CombinedGuiClickRequest | 

    try:
        # Click using selector or screen coordinates
        api_response = api_instance.gui_click(browser_id, payload)
        print("The response of BrowserApi->gui_click:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->gui_click: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**CombinedGuiClickRequest**](CombinedGuiClickRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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
> ActionResult history(browser_id, payload)

Execute history action: back, forward, or refresh

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.HistoryRequest() # HistoryRequest | 

    try:
        # Execute history action: back, forward, or refresh
        api_response = api_instance.history(browser_id, payload)
        print("The response of BrowserApi->history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**HistoryRequest**](HistoryRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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

# **list_browsers**
> BrowserList list_browsers()

List all active browser instances

### Example


```python
import airbrowser_client
from airbrowser_client.models.browser_list import BrowserList
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

    try:
        # List all active browser instances
        api_response = api_instance.list_browsers()
        print("The response of BrowserApi->list_browsers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->list_browsers: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BrowserList**](BrowserList.md)

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

# **mouse**
> SuccessResponse mouse(browser_id, payload)

Mouse action: hover or drag

### Example


```python
import airbrowser_client
from airbrowser_client.models.mouse_request import MouseRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.MouseRequest() # MouseRequest | 

    try:
        # Mouse action: hover or drag
        api_response = api_instance.mouse(browser_id, payload)
        print("The response of BrowserApi->mouse:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->mouse: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**MouseRequest**](MouseRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ActionResult navigate_browser(browser_id, payload)

Navigate to a URL

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
from airbrowser_client.models.navigate_request import NavigateRequest
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.NavigateRequest() # NavigateRequest | 

    try:
        # Navigate to a URL
        api_response = api_instance.navigate_browser(browser_id, payload)
        print("The response of BrowserApi->navigate_browser:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->navigate_browser: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**NavigateRequest**](NavigateRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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
> LogsResponse network_logs(browser_id, payload)

Get or clear network logs

### Example


```python
import airbrowser_client
from airbrowser_client.models.logs_response import LogsResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.NetworkLogsRequest() # NetworkLogsRequest | 

    try:
        # Get or clear network logs
        api_response = api_instance.network_logs(browser_id, payload)
        print("The response of BrowserApi->network_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->network_logs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**NetworkLogsRequest**](NetworkLogsRequest.md)|  | 

### Return type

[**LogsResponse**](LogsResponse.md)

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
> SuccessResponse performance(browser_id, payload)

Manage performance: start_trace, stop_trace, metrics, or analyze

### Example


```python
import airbrowser_client
from airbrowser_client.models.performance_request import PerformanceRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.PerformanceRequest() # PerformanceRequest | 

    try:
        # Manage performance: start_trace, stop_trace, metrics, or analyze
        api_response = api_instance.performance(browser_id, payload)
        print("The response of BrowserApi->performance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->performance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**PerformanceRequest**](PerformanceRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ActionResult press_keys(browser_id, payload)

Press keys on an element

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.PressKeysRequest() # PressKeysRequest | 

    try:
        # Press keys on an element
        api_response = api_instance.press_keys(browser_id, payload)
        print("The response of BrowserApi->press_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->press_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**PressKeysRequest**](PressKeysRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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
> SuccessResponse resize(browser_id, payload)

Resize viewport

### Example


```python
import airbrowser_client
from airbrowser_client.models.resize_request import ResizeRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
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
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**ResizeRequest**](ResizeRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> SuccessResponse scroll(browser_id, payload)

Scroll to element/coordinates (absolute) or by delta (relative)

### Example


```python
import airbrowser_client
from airbrowser_client.models.combined_scroll_request import CombinedScrollRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.CombinedScrollRequest() # CombinedScrollRequest | 

    try:
        # Scroll to element/coordinates (absolute) or by delta (relative)
        api_response = api_instance.scroll(browser_id, payload)
        print("The response of BrowserApi->scroll:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->scroll: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**CombinedScrollRequest**](CombinedScrollRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> SuccessResponse select(browser_id, payload)

Select dropdown: select option or get options

### Example


```python
import airbrowser_client
from airbrowser_client.models.select_request import SelectRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
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
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**SelectRequest**](SelectRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> SuccessResponse tabs(browser_id, payload)

Manage browser tabs: list, new, switch, close, or current

### Example


```python
import airbrowser_client
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.TabsRequest() # TabsRequest | 

    try:
        # Manage browser tabs: list, new, switch, close, or current
        api_response = api_instance.tabs(browser_id, payload)
        print("The response of BrowserApi->tabs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->tabs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**TabsRequest**](TabsRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ScreenshotResponse take_screenshot(browser_id)

Take a screenshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.screenshot_response import ScreenshotResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Take a screenshot
        api_response = api_instance.take_screenshot(browser_id)
        print("The response of BrowserApi->take_screenshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->take_screenshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**ScreenshotResponse**](ScreenshotResponse.md)

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

# **take_snapshot**
> SuccessResponse take_snapshot(browser_id, payload)

Take DOM/accessibility snapshot

### Example


```python
import airbrowser_client
from airbrowser_client.models.snapshot_request import SnapshotRequest
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.SnapshotRequest() # SnapshotRequest | 

    try:
        # Take DOM/accessibility snapshot
        api_response = api_instance.take_snapshot(browser_id, payload)
        print("The response of BrowserApi->take_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->take_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**SnapshotRequest**](SnapshotRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ActionResult type_text(browser_id, payload)

Type text into an element

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
from airbrowser_client.models.type_request import TypeRequest
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.TypeRequest() # TypeRequest | 

    try:
        # Type text into an element
        api_response = api_instance.type_text(browser_id, payload)
        print("The response of BrowserApi->type_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->type_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**TypeRequest**](TypeRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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
> SuccessResponse upload_file(browser_id, payload)

Upload a file

### Example


```python
import airbrowser_client
from airbrowser_client.models.success_response import SuccessResponse
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.UploadFileRequest() # UploadFileRequest | 

    try:
        # Upload a file
        api_response = api_instance.upload_file(browser_id, payload)
        print("The response of BrowserApi->upload_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->upload_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**UploadFileRequest**](UploadFileRequest.md)|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

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
> ActionResult wait_element(browser_id, payload)

Wait for element to become visible or hidden

### Example


```python
import airbrowser_client
from airbrowser_client.models.action_result import ActionResult
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
    browser_id = 'browser_id_example' # str | Unique browser identifier
    payload = airbrowser_client.WaitElementRequest() # WaitElementRequest | 

    try:
        # Wait for element to become visible or hidden
        api_response = api_instance.wait_element(browser_id, payload)
        print("The response of BrowserApi->wait_element:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->wait_element: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 
 **payload** | [**WaitElementRequest**](WaitElementRequest.md)|  | 

### Return type

[**ActionResult**](ActionResult.md)

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
> WhatIsVisibleResult what_is_visible(browser_id)

Analyze visible page content using AI

### Example


```python
import airbrowser_client
from airbrowser_client.models.what_is_visible_result import WhatIsVisibleResult
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
    browser_id = 'browser_id_example' # str | Unique browser identifier

    try:
        # Analyze visible page content using AI
        api_response = api_instance.what_is_visible(browser_id)
        print("The response of BrowserApi->what_is_visible:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BrowserApi->what_is_visible: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **browser_id** | **str**| Unique browser identifier | 

### Return type

[**WhatIsVisibleResult**](WhatIsVisibleResult.md)

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

