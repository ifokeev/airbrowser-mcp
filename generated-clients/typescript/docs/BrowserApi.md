# BrowserApi

All URIs are relative to */api/v1*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**browsers**](#browsers) | **POST** /browser/browsers | Admin: list all, get info, or close all browsers|
|[**checkElement**](#checkelement) | **GET** /browser/{browser_id}/check_element | Check if element exists or is visible|
|[**click**](#click) | **POST** /browser/{browser_id}/click | Click element|
|[**closeBrowser**](#closebrowser) | **DELETE** /browser/{browser_id}/close_browser | Close browser instance|
|[**consoleLogs**](#consolelogs) | **POST** /browser/{browser_id}/console_logs | Console logs: get or clear|
|[**createBrowser**](#createbrowser) | **POST** /browser/create_browser | Create browser instance with optional persistent profile|
|[**detectCoordinates**](#detectcoordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using vision|
|[**dialog**](#dialog) | **POST** /browser/{browser_id}/dialog | Dialogs: get, accept, dismiss|
|[**emulate**](#emulate) | **POST** /browser/{browser_id}/emulate | Emulation: set, clear, list_devices|
|[**executeScript**](#executescript) | **POST** /browser/{browser_id}/execute_script | Execute JavaScript|
|[**fillForm**](#fillform) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields|
|[**getCdpEndpoint**](#getcdpendpoint) | **GET** /browser/{browser_id}/get_cdp_endpoint | Get Chrome DevTools Protocol WebSocket URL for direct CDP access|
|[**getContent**](#getcontent) | **GET** /browser/{browser_id}/get_content | Get page HTML|
|[**getElementData**](#getelementdata) | **GET** /browser/{browser_id}/get_element_data | Get element text, attribute, or property|
|[**getUrl**](#geturl) | **GET** /browser/{browser_id}/get_url | Get current URL|
|[**guiClick**](#guiclick) | **POST** /browser/{browser_id}/gui_click | GUI click by selector or coordinates|
|[**guiHoverXy**](#guihoverxy) | **POST** /browser/{browser_id}/gui_hover_xy | GUI hover at coordinates|
|[**guiPressKeysXy**](#guipresskeysxy) | **POST** /browser/{browser_id}/gui_press_keys_xy | Press keys at coordinates (click to focus, then send keys)|
|[**guiTypeXy**](#guitypexy) | **POST** /browser/{browser_id}/gui_type_xy | GUI type at coordinates - clicks then types text|
|[**history**](#history) | **POST** /browser/{browser_id}/history | History: back, forward, or refresh|
|[**mouse**](#mouse) | **POST** /browser/{browser_id}/mouse | Mouse: hover or drag|
|[**navigateBrowser**](#navigatebrowser) | **POST** /browser/{browser_id}/navigate | Navigate to URL|
|[**networkLogs**](#networklogs) | **POST** /browser/{browser_id}/network_logs | Network logs: get or clear|
|[**performance**](#performance) | **POST** /browser/{browser_id}/performance | Performance: start_trace, stop_trace, metrics, analyze|
|[**pressKeys**](#presskeys) | **POST** /browser/{browser_id}/press_keys | Press keyboard keys|
|[**resize**](#resize) | **POST** /browser/{browser_id}/resize | Resize viewport|
|[**scroll**](#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coords or by delta|
|[**select**](#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options|
|[**snapshot**](#snapshot) | **POST** /browser/{browser_id}/snapshot | DOM or accessibility snapshot|
|[**tabs**](#tabs) | **POST** /browser/{browser_id}/tabs | Tabs: list, new, switch, close, current|
|[**takeScreenshot**](#takescreenshot) | **POST** /browser/{browser_id}/screenshot | Take screenshot|
|[**typeText**](#typetext) | **POST** /browser/{browser_id}/type | Type text into element|
|[**uploadFile**](#uploadfile) | **POST** /browser/{browser_id}/upload_file | Upload file to input|
|[**waitElement**](#waitelement) | **POST** /browser/{browser_id}/wait_element | Wait for element to be visible or hidden|
|[**whatIsVisible**](#whatisvisible) | **POST** /browser/{browser_id}/what_is_visible | AI page analysis - what\&#39;s visible|

# **browsers**
> GenericResponse browsers(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    BrowsersRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let payload: BrowsersRequest; //

const { status, data } = await apiInstance.browsers(
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **BrowsersRequest**|  | |


### Return type

**GenericResponse**

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

# **checkElement**
> GenericResponse checkElement()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let selector: string; //selector (default to undefined)
let check: string; //check (default to undefined)
let by: string; //by (optional) (default to undefined)

const { status, data } = await apiInstance.checkElement(
    browserId,
    selector,
    check,
    by
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|
| **selector** | [**string**] | selector | defaults to undefined|
| **check** | [**string**] | check | defaults to undefined|
| **by** | [**string**] | by | (optional) defaults to undefined|


### Return type

**GenericResponse**

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

# **click**
> GenericResponse click(payload)

Use if_visible=True to only click if visible.

### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ClickRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **closeBrowser**
> GenericResponse closeBrowser()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)

const { status, data } = await apiInstance.closeBrowser(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse consoleLogs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ConsoleLogsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse createBrowser(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    CreateBrowserRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let payload: CreateBrowserRequest; //

const { status, data } = await apiInstance.createBrowser(
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CreateBrowserRequest**|  | |


### Return type

**GenericResponse**

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

# **detectCoordinates**
> GenericResponse detectCoordinates(payload)

Args:     browser_id: Browser instance identifier     prompt: Natural language description of element to find     fx: Fractional x offset for click point (0.0=left, 0.5=center, 1.0=right).         If None, auto-bias is applied for wide elements (0.25 for aspect ratio > 10).     fy: Fractional y offset for click point (0.0=top, 0.5=center, 1.0=bottom).

### Example

```typescript
import {
    BrowserApi,
    Configuration,
    DetectCoordinatesRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse dialog(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    DialogRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: DialogRequest; //

const { status, data } = await apiInstance.dialog(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **DialogRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse emulate(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    EmulateRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: EmulateRequest; //

const { status, data } = await apiInstance.emulate(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **EmulateRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse executeScript(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ExecuteScriptRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: ExecuteScriptRequest; //

const { status, data } = await apiInstance.executeScript(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ExecuteScriptRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse fillForm(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    FillFormRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **getCdpEndpoint**
> GenericResponse getCdpEndpoint()

Returns the WebSocket URL that external tools (Playwright, Puppeteer, etc.) can use to connect directly to Chrome\'s DevTools Protocol for advanced automation like network interception, performance profiling, or custom CDP commands.  The returned URL format: ws://host:port/devtools/browser/{guid}  Note: The URL uses the container\'s internal address. For external access, ensure the CDP port is exposed and use the appropriate host address.

### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)

const { status, data } = await apiInstance.getCdpEndpoint(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse getContent()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)

const { status, data } = await apiInstance.getContent(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse getElementData()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let selector: string; //selector (default to undefined)
let dataType: string; //data_type (default to undefined)
let name: string; //name (optional) (default to undefined)
let by: string; //by (optional) (default to undefined)

const { status, data } = await apiInstance.getElementData(
    browserId,
    selector,
    dataType,
    name,
    by
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|
| **selector** | [**string**] | selector | defaults to undefined|
| **dataType** | [**string**] | data_type | defaults to undefined|
| **name** | [**string**] | name | (optional) defaults to undefined|
| **by** | [**string**] | by | (optional) defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse getUrl()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)

const { status, data } = await apiInstance.getUrl(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse guiClick(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    GuiClickRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: GuiClickRequest; //

const { status, data } = await apiInstance.guiClick(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **GuiClickRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **guiHoverXy**
> GenericResponse guiHoverXy(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    GuiHoverXyRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: GuiHoverXyRequest; //

const { status, data } = await apiInstance.guiHoverXy(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **GuiHoverXyRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **guiPressKeysXy**
> GenericResponse guiPressKeysXy(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    GuiPressKeysXyRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: GuiPressKeysXyRequest; //

const { status, data } = await apiInstance.guiPressKeysXy(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **GuiPressKeysXyRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **guiTypeXy**
> GenericResponse guiTypeXy(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    GuiTypeXyRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: GuiTypeXyRequest; //

const { status, data } = await apiInstance.guiTypeXy(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **GuiTypeXyRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse history(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    HistoryRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **mouse**
> GenericResponse mouse(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    MouseRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse navigateBrowser(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    NavigateBrowserRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: NavigateBrowserRequest; //

const { status, data } = await apiInstance.navigateBrowser(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **NavigateBrowserRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse networkLogs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    NetworkLogsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse performance(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    PerformanceRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse pressKeys(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    PressKeysRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse resize(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ResizeRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse scroll(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    ScrollRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: ScrollRequest; //

const { status, data } = await apiInstance.scroll(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ScrollRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse select(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    SelectRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

# **snapshot**
> GenericResponse snapshot(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    SnapshotRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: SnapshotRequest; //

const { status, data } = await apiInstance.snapshot(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **SnapshotRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse tabs(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    TabsRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse takeScreenshot(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    TakeScreenshotRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: TakeScreenshotRequest; //

const { status, data } = await apiInstance.takeScreenshot(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **TakeScreenshotRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse typeText(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    TypeTextRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
let payload: TypeTextRequest; //

const { status, data } = await apiInstance.typeText(
    browserId,
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **TypeTextRequest**|  | |
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse uploadFile(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    UploadFileRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse waitElement(payload)


### Example

```typescript
import {
    BrowserApi,
    Configuration,
    WaitElementRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)
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
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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
> GenericResponse whatIsVisible()


### Example

```typescript
import {
    BrowserApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new BrowserApi(configuration);

let browserId: string; // (default to undefined)

const { status, data } = await apiInstance.whatIsVisible(
    browserId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **browserId** | [**string**] |  | defaults to undefined|


### Return type

**GenericResponse**

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

