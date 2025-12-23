# BrowserApi

All URIs are relative to */api/v1*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**checkElement**](#checkelement) | **POST** /browser/{browser_id}/check_element | Check if element exists or is visible|
|[**click**](#click) | **POST** /browser/{browser_id}/click | Click element|
|[**closeAllBrowsers**](#closeallbrowsers) | **POST** /browser/close_all | Close all active browser instances|
|[**closeBrowser**](#closebrowser) | **POST** /browser/{browser_id}/close | Close a browser instance|
|[**consoleLogs**](#consolelogs) | **POST** /browser/{browser_id}/console | Get or clear console logs|
|[**createBrowser**](#createbrowser) | **POST** /browser/create | Create a new browser instance|
|[**deleteBrowser**](#deletebrowser) | **DELETE** /browser/{browser_id} | Close and remove a browser instance|
|[**detectCoordinates**](#detectcoordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using AI vision|
|[**dialog**](#dialog) | **POST** /browser/{browser_id}/dialog | Manage browser dialogs: get, accept, or dismiss|
|[**emulate**](#emulate) | **POST** /browser/{browser_id}/emulate | Manage device emulation: set, clear, or list_devices|
|[**executeScript**](#executescript) | **POST** /browser/{browser_id}/execute | Execute JavaScript|
|[**fillForm**](#fillform) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields|
|[**getBrowser**](#getbrowser) | **GET** /browser/{browser_id} | Get browser instance details|
|[**getBrowserStatus**](#getbrowserstatus) | **GET** /browser/{browser_id}/status | Get browser status|
|[**getContent**](#getcontent) | **GET** /browser/{browser_id}/content | Get page HTML content|
|[**getElementData**](#getelementdata) | **POST** /browser/{browser_id}/element_data | Get element text, attribute, or property|
|[**getPoolStatus**](#getpoolstatus) | **GET** /browser/pool/status | Get browser pool status|
|[**getUrl**](#geturl) | **GET** /browser/{browser_id}/url | Get current page URL|
|[**guiClick**](#guiclick) | **POST** /browser/{browser_id}/gui_click | Click using selector or screen coordinates|
|[**history**](#history) | **POST** /browser/{browser_id}/history | Execute history action: back, forward, or refresh|
|[**listBrowsers**](#listbrowsers) | **GET** /browser/list | List all active browser instances|
|[**mouse**](#mouse) | **POST** /browser/{browser_id}/mouse | Mouse action: hover or drag|
|[**navigateBrowser**](#navigatebrowser) | **POST** /browser/{browser_id}/navigate | Navigate to a URL|
|[**networkLogs**](#networklogs) | **POST** /browser/{browser_id}/network | Get or clear network logs|
|[**performance**](#performance) | **POST** /browser/{browser_id}/performance | Manage performance: start_trace, stop_trace, metrics, or analyze|
|[**pressKeys**](#presskeys) | **POST** /browser/{browser_id}/press_keys | Press keys on an element|
|[**resize**](#resize) | **POST** /browser/{browser_id}/resize | Resize viewport|
|[**scroll**](#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coordinates (absolute) or by delta (relative)|
|[**select**](#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options|
|[**tabs**](#tabs) | **POST** /browser/{browser_id}/tabs | Manage browser tabs: list, new, switch, close, or current|
|[**takeScreenshot**](#takescreenshot) | **POST** /browser/{browser_id}/screenshot | Take a screenshot|
|[**takeSnapshot**](#takesnapshot) | **POST** /browser/{browser_id}/snapshot | Take DOM/accessibility snapshot|
|[**typeText**](#typetext) | **POST** /browser/{browser_id}/type | Type text into an element|
|[**uploadFile**](#uploadfile) | **POST** /browser/{browser_id}/upload_file | Upload a file|
|[**waitElement**](#waitelement) | **POST** /browser/{browser_id}/wait_element | Wait for element to become visible or hidden|
|[**whatIsVisible**](#whatisvisible) | **GET** /browser/{browser_id}/what_is_visible | Analyze visible page content using AI|

# **checkElement**
> SuccessResponse checkElement(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CheckElementRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: CheckElementRequest; //

const { status, data } = await apiInstance.checkElement(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CheckElementRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **click**
> ActionResult click(payload)

Use if_visible=true to only click if visible.

### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ClickRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: ClickRequest; //

const { status, data } = await apiInstance.click(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ClickRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **closeAllBrowsers**
> BaseResponse closeAllBrowsers()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

const { status, data } = await apiInstance.closeAllBrowsers();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**BaseResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **closeBrowser**
> BaseResponse closeBrowser()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.closeBrowser(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**BaseResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **consoleLogs**
> LogsResponse consoleLogs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ConsoleLogsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: ConsoleLogsRequest; //

const { status, data } = await apiInstance.consoleLogs(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ConsoleLogsRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**LogsResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createBrowser**
> BrowserCreated createBrowser(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    BrowserConfig
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let payload: BrowserConfig; //

const { status, data } = await apiInstance.createBrowser(
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **BrowserConfig**|  | |


### Return type

**BrowserCreated**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**400** | Bad request |  -  |
|**200** | Browser created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteBrowser**
> BaseResponse deleteBrowser()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.deleteBrowser(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**BaseResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **detectCoordinates**
> DetectCoordinatesResult detectCoordinates(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    DetectCoordinatesRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: DetectCoordinatesRequest; //

const { status, data } = await apiInstance.detectCoordinates(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **DetectCoordinatesRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**DetectCoordinatesResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dialog**
> SuccessResponse dialog(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CombinedDialogRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: CombinedDialogRequest; //

const { status, data } = await apiInstance.dialog(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CombinedDialogRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **emulate**
> SuccessResponse emulate(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CombinedEmulateRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: CombinedEmulateRequest; //

const { status, data } = await apiInstance.emulate(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CombinedEmulateRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **executeScript**
> ExecuteResponse executeScript(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ExecuteRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: ExecuteRequest; //

const { status, data } = await apiInstance.executeScript(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ExecuteRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ExecuteResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fillForm**
> SuccessResponse fillForm(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    FillFormRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: FillFormRequest; //

const { status, data } = await apiInstance.fillForm(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **FillFormRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getBrowser**
> BrowserInfoResponse getBrowser()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.getBrowser(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**BrowserInfoResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**404** | Browser not found |  -  |
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getBrowserStatus**
> BrowserInfoResponse getBrowserStatus()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.getBrowserStatus(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**BrowserInfoResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getContent**
> ContentResponse getContent()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.getContent(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ContentResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getElementData**
> AttributeResponse getElementData(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ElementDataRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: ElementDataRequest; //

const { status, data } = await apiInstance.getElementData(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ElementDataRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**AttributeResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getPoolStatus**
> PoolStatusResponse getPoolStatus()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

const { status, data } = await apiInstance.getPoolStatus();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**PoolStatusResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getUrl**
> UrlResponse getUrl()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.getUrl(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**UrlResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **guiClick**
> ActionResult guiClick(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CombinedGuiClickRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: CombinedGuiClickRequest; //

const { status, data } = await apiInstance.guiClick(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CombinedGuiClickRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **history**
> ActionResult history(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    HistoryRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: HistoryRequest; //

const { status, data } = await apiInstance.history(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **HistoryRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listBrowsers**
> BrowserList listBrowsers()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

const { status, data } = await apiInstance.listBrowsers();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**BrowserList**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mouse**
> SuccessResponse mouse(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    MouseRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: MouseRequest; //

const { status, data } = await apiInstance.mouse(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **MouseRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **navigateBrowser**
> ActionResult navigateBrowser(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    NavigateRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: NavigateRequest; //

const { status, data } = await apiInstance.navigateBrowser(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **NavigateRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **networkLogs**
> LogsResponse networkLogs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    NetworkLogsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: NetworkLogsRequest; //

const { status, data } = await apiInstance.networkLogs(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **NetworkLogsRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**LogsResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **performance**
> SuccessResponse performance(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    PerformanceRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: PerformanceRequest; //

const { status, data } = await apiInstance.performance(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **PerformanceRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pressKeys**
> ActionResult pressKeys(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    PressKeysRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: PressKeysRequest; //

const { status, data } = await apiInstance.pressKeys(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **PressKeysRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resize**
> SuccessResponse resize(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ResizeRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: ResizeRequest; //

const { status, data } = await apiInstance.resize(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ResizeRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scroll**
> SuccessResponse scroll(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CombinedScrollRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: CombinedScrollRequest; //

const { status, data } = await apiInstance.scroll(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CombinedScrollRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **select**
> SuccessResponse select(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    SelectRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: SelectRequest; //

const { status, data } = await apiInstance.select(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **SelectRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tabs**
> SuccessResponse tabs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    TabsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: TabsRequest; //

const { status, data } = await apiInstance.tabs(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **TabsRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **takeScreenshot**
> ScreenshotResponse takeScreenshot()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.takeScreenshot(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ScreenshotResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **takeSnapshot**
> SuccessResponse takeSnapshot(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    SnapshotRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: SnapshotRequest; //

const { status, data } = await apiInstance.takeSnapshot(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **SnapshotRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **typeText**
> ActionResult typeText(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    TypeRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: TypeRequest; //

const { status, data } = await apiInstance.typeText(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **TypeRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **uploadFile**
> SuccessResponse uploadFile(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    UploadFileRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: UploadFileRequest; //

const { status, data } = await apiInstance.uploadFile(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **UploadFileRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **waitElement**
> ActionResult waitElement(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    WaitElementRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)
let payload: WaitElementRequest; //

const { status, data } = await apiInstance.waitElement(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **WaitElementRequest**|  | |
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**ActionResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **whatIsVisible**
> WhatIsVisibleResult whatIsVisible()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; //Unique browser identifier (default to undefined)

const { status, data } = await apiInstance.whatIsVisible(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] | Unique browser identifier | defaults to undefined|


### Return type

**WhatIsVisibleResult**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

