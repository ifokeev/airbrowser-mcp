## airbrowser-client@1.0.0

This generator creates TypeScript/JavaScript client that utilizes [axios](https://github.com/axios/axios). The generated Node module can be used in the following environments:

Environment
* Node.js
* Webpack
* Browserify

Language level
* ES5 - you must have a Promises/A+ library installed
* ES6

Module system
* CommonJS
* ES6 module system

It can be used in both TypeScript and JavaScript. In TypeScript, the definition will be automatically resolved via `package.json`. ([Reference](https://www.typescriptlang.org/docs/handbook/declaration-files/consumption.html))

### Building

To build and compile the typescript sources to javascript use:
```
npm install
npm run build
```

### Publishing

First build the package then run `npm publish`

### Consuming

navigate to the folder of your consuming project and run one of the following commands.

_published:_

```
npm install airbrowser-client@1.0.0 --save
```

_unPublished (not recommended):_

```
npm install PATH_TO_GENERATED_PACKAGE --save
```

### Documentation for API Endpoints

All URIs are relative to */api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*BrowserApi* | [**checkElement**](docs/BrowserApi.md#checkelement) | **POST** /browser/{browser_id}/check_element | Check if element exists or is visible
*BrowserApi* | [**click**](docs/BrowserApi.md#click) | **POST** /browser/{browser_id}/click | Click element
*BrowserApi* | [**closeAllBrowsers**](docs/BrowserApi.md#closeallbrowsers) | **POST** /browser/close_all | Close all active browser instances
*BrowserApi* | [**closeBrowser**](docs/BrowserApi.md#closebrowser) | **POST** /browser/{browser_id}/close | Close a browser instance
*BrowserApi* | [**consoleLogs**](docs/BrowserApi.md#consolelogs) | **POST** /browser/{browser_id}/console | Get or clear console logs
*BrowserApi* | [**createBrowser**](docs/BrowserApi.md#createbrowser) | **POST** /browser/create | Create a new browser instance
*BrowserApi* | [**deleteBrowser**](docs/BrowserApi.md#deletebrowser) | **DELETE** /browser/{browser_id} | Close and remove a browser instance
*BrowserApi* | [**detectCoordinates**](docs/BrowserApi.md#detectcoordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using AI vision
*BrowserApi* | [**dialog**](docs/BrowserApi.md#dialog) | **POST** /browser/{browser_id}/dialog | Manage browser dialogs: get, accept, or dismiss
*BrowserApi* | [**emulate**](docs/BrowserApi.md#emulate) | **POST** /browser/{browser_id}/emulate | Manage device emulation: set, clear, or list_devices
*BrowserApi* | [**executeScript**](docs/BrowserApi.md#executescript) | **POST** /browser/{browser_id}/execute | Execute JavaScript
*BrowserApi* | [**fillForm**](docs/BrowserApi.md#fillform) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields
*BrowserApi* | [**getBrowser**](docs/BrowserApi.md#getbrowser) | **GET** /browser/{browser_id} | Get browser instance details
*BrowserApi* | [**getBrowserStatus**](docs/BrowserApi.md#getbrowserstatus) | **GET** /browser/{browser_id}/status | Get browser status
*BrowserApi* | [**getContent**](docs/BrowserApi.md#getcontent) | **GET** /browser/{browser_id}/content | Get page HTML content
*BrowserApi* | [**getElementData**](docs/BrowserApi.md#getelementdata) | **POST** /browser/{browser_id}/element_data | Get element text, attribute, or property
*BrowserApi* | [**getPoolStatus**](docs/BrowserApi.md#getpoolstatus) | **GET** /browser/pool/status | Get browser pool status
*BrowserApi* | [**getUrl**](docs/BrowserApi.md#geturl) | **GET** /browser/{browser_id}/url | Get current page URL
*BrowserApi* | [**guiClick**](docs/BrowserApi.md#guiclick) | **POST** /browser/{browser_id}/gui_click | Click using selector or screen coordinates
*BrowserApi* | [**history**](docs/BrowserApi.md#history) | **POST** /browser/{browser_id}/history | Execute history action: back, forward, or refresh
*BrowserApi* | [**listBrowsers**](docs/BrowserApi.md#listbrowsers) | **GET** /browser/list | List all active browser instances
*BrowserApi* | [**mouse**](docs/BrowserApi.md#mouse) | **POST** /browser/{browser_id}/mouse | Mouse action: hover or drag
*BrowserApi* | [**navigateBrowser**](docs/BrowserApi.md#navigatebrowser) | **POST** /browser/{browser_id}/navigate | Navigate to a URL
*BrowserApi* | [**networkLogs**](docs/BrowserApi.md#networklogs) | **POST** /browser/{browser_id}/network | Get or clear network logs
*BrowserApi* | [**performance**](docs/BrowserApi.md#performance) | **POST** /browser/{browser_id}/performance | Manage performance: start_trace, stop_trace, metrics, or analyze
*BrowserApi* | [**pressKeys**](docs/BrowserApi.md#presskeys) | **POST** /browser/{browser_id}/press_keys | Press keys on an element
*BrowserApi* | [**resize**](docs/BrowserApi.md#resize) | **POST** /browser/{browser_id}/resize | Resize viewport
*BrowserApi* | [**scroll**](docs/BrowserApi.md#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coordinates (absolute) or by delta (relative)
*BrowserApi* | [**select**](docs/BrowserApi.md#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options
*BrowserApi* | [**tabs**](docs/BrowserApi.md#tabs) | **POST** /browser/{browser_id}/tabs | Manage browser tabs: list, new, switch, close, or current
*BrowserApi* | [**takeScreenshot**](docs/BrowserApi.md#takescreenshot) | **POST** /browser/{browser_id}/screenshot | Take a screenshot
*BrowserApi* | [**takeSnapshot**](docs/BrowserApi.md#takesnapshot) | **POST** /browser/{browser_id}/snapshot | Take DOM/accessibility snapshot
*BrowserApi* | [**typeText**](docs/BrowserApi.md#typetext) | **POST** /browser/{browser_id}/type | Type text into an element
*BrowserApi* | [**uploadFile**](docs/BrowserApi.md#uploadfile) | **POST** /browser/{browser_id}/upload_file | Upload a file
*BrowserApi* | [**waitElement**](docs/BrowserApi.md#waitelement) | **POST** /browser/{browser_id}/wait_element | Wait for element to become visible or hidden
*BrowserApi* | [**whatIsVisible**](docs/BrowserApi.md#whatisvisible) | **GET** /browser/{browser_id}/what_is_visible | Analyze visible page content using AI
*HealthApi* | [**healthCheck**](docs/HealthApi.md#healthcheck) | **GET** /health/ | Check the health status of the browser pool
*HealthApi* | [**prometheusMetrics**](docs/HealthApi.md#prometheusmetrics) | **GET** /health/metrics | Get Prometheus-style metrics for monitoring
*PoolApi* | [**scalePool**](docs/PoolApi.md#scalepool) | **POST** /pool/scale | Scale the browser pool to a new maximum size
*PoolApi* | [**shutdownServer**](docs/PoolApi.md#shutdownserver) | **POST** /pool/shutdown | Gracefully shutdown the browser pool server
*ProfilesApi* | [**createProfile**](docs/ProfilesApi.md#createprofile) | **POST** /profiles/ | Create a new browser profile
*ProfilesApi* | [**deleteProfile**](docs/ProfilesApi.md#deleteprofile) | **DELETE** /profiles/{profile_name} | Delete a browser profile
*ProfilesApi* | [**getProfile**](docs/ProfilesApi.md#getprofile) | **GET** /profiles/{profile_name} | Get profile information
*ProfilesApi* | [**listProfiles**](docs/ProfilesApi.md#listprofiles) | **GET** /profiles/ | List all browser profiles


### Documentation For Models

 - [ActionResult](docs/ActionResult.md)
 - [AttributeResponse](docs/AttributeResponse.md)
 - [BaseResponse](docs/BaseResponse.md)
 - [BrowserConfig](docs/BrowserConfig.md)
 - [BrowserCreated](docs/BrowserCreated.md)
 - [BrowserCreationData](docs/BrowserCreationData.md)
 - [BrowserInfoResponse](docs/BrowserInfoResponse.md)
 - [BrowserList](docs/BrowserList.md)
 - [BrowserListData](docs/BrowserListData.md)
 - [CheckElementRequest](docs/CheckElementRequest.md)
 - [ClickRequest](docs/ClickRequest.md)
 - [CombinedDialogRequest](docs/CombinedDialogRequest.md)
 - [CombinedEmulateRequest](docs/CombinedEmulateRequest.md)
 - [CombinedGuiClickRequest](docs/CombinedGuiClickRequest.md)
 - [CombinedScrollRequest](docs/CombinedScrollRequest.md)
 - [ConsoleLogsRequest](docs/ConsoleLogsRequest.md)
 - [ContentData](docs/ContentData.md)
 - [ContentResponse](docs/ContentResponse.md)
 - [CreateProfileRequest](docs/CreateProfileRequest.md)
 - [DetectCoordinatesRequest](docs/DetectCoordinatesRequest.md)
 - [DetectCoordinatesResult](docs/DetectCoordinatesResult.md)
 - [ElementDataRequest](docs/ElementDataRequest.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [ExecuteData](docs/ExecuteData.md)
 - [ExecuteRequest](docs/ExecuteRequest.md)
 - [ExecuteResponse](docs/ExecuteResponse.md)
 - [FillFormRequest](docs/FillFormRequest.md)
 - [FormField](docs/FormField.md)
 - [HealthStatus](docs/HealthStatus.md)
 - [HistoryRequest](docs/HistoryRequest.md)
 - [LogsResponse](docs/LogsResponse.md)
 - [MouseRequest](docs/MouseRequest.md)
 - [NavigateRequest](docs/NavigateRequest.md)
 - [NetworkLogsRequest](docs/NetworkLogsRequest.md)
 - [PerformanceRequest](docs/PerformanceRequest.md)
 - [PoolScaled](docs/PoolScaled.md)
 - [PoolStatusResponse](docs/PoolStatusResponse.md)
 - [PressKeysRequest](docs/PressKeysRequest.md)
 - [ProfileInfo](docs/ProfileInfo.md)
 - [ProfileListData](docs/ProfileListData.md)
 - [ProfileListResponse](docs/ProfileListResponse.md)
 - [ProfileResponse](docs/ProfileResponse.md)
 - [ResizeRequest](docs/ResizeRequest.md)
 - [ScaleData](docs/ScaleData.md)
 - [ScalePool](docs/ScalePool.md)
 - [ScreenshotData](docs/ScreenshotData.md)
 - [ScreenshotResponse](docs/ScreenshotResponse.md)
 - [SelectRequest](docs/SelectRequest.md)
 - [SnapshotRequest](docs/SnapshotRequest.md)
 - [SuccessResponse](docs/SuccessResponse.md)
 - [TabsRequest](docs/TabsRequest.md)
 - [TypeRequest](docs/TypeRequest.md)
 - [UploadFileRequest](docs/UploadFileRequest.md)
 - [UrlData](docs/UrlData.md)
 - [UrlResponse](docs/UrlResponse.md)
 - [WaitElementRequest](docs/WaitElementRequest.md)
 - [WhatIsVisibleResult](docs/WhatIsVisibleResult.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.

