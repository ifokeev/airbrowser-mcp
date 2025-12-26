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
*BrowserApi* | [**browsers**](docs/BrowserApi.md#browsers) | **POST** /browser/browsers | Admin: list all, get info, or close all browsers
*BrowserApi* | [**checkElement**](docs/BrowserApi.md#checkelement) | **GET** /browser/{browser_id}/check_element | Check if element exists or is visible
*BrowserApi* | [**click**](docs/BrowserApi.md#click) | **POST** /browser/{browser_id}/click | Click element
*BrowserApi* | [**closeBrowser**](docs/BrowserApi.md#closebrowser) | **DELETE** /browser/{browser_id}/close_browser | Close browser instance
*BrowserApi* | [**consoleLogs**](docs/BrowserApi.md#consolelogs) | **POST** /browser/{browser_id}/console_logs | Console logs: get or clear
*BrowserApi* | [**createBrowser**](docs/BrowserApi.md#createbrowser) | **POST** /browser/create_browser | Create browser instance with optional persistent profile
*BrowserApi* | [**detectCoordinates**](docs/BrowserApi.md#detectcoordinates) | **POST** /browser/{browser_id}/detect_coordinates | Detect element coordinates using vision
*BrowserApi* | [**dialog**](docs/BrowserApi.md#dialog) | **POST** /browser/{browser_id}/dialog | Dialogs: get, accept, dismiss
*BrowserApi* | [**emulate**](docs/BrowserApi.md#emulate) | **POST** /browser/{browser_id}/emulate | Emulation: set, clear, list_devices
*BrowserApi* | [**executeScript**](docs/BrowserApi.md#executescript) | **POST** /browser/{browser_id}/execute_script | Execute JavaScript
*BrowserApi* | [**fillForm**](docs/BrowserApi.md#fillform) | **POST** /browser/{browser_id}/fill_form | Fill multiple form fields
*BrowserApi* | [**getContent**](docs/BrowserApi.md#getcontent) | **GET** /browser/{browser_id}/get_content | Get page HTML
*BrowserApi* | [**getElementData**](docs/BrowserApi.md#getelementdata) | **GET** /browser/{browser_id}/get_element_data | Get element text, attribute, or property
*BrowserApi* | [**getUrl**](docs/BrowserApi.md#geturl) | **GET** /browser/{browser_id}/get_url | Get current URL
*BrowserApi* | [**guiClick**](docs/BrowserApi.md#guiclick) | **POST** /browser/{browser_id}/gui_click | GUI click by selector or coordinates
*BrowserApi* | [**guiHoverXy**](docs/BrowserApi.md#guihoverxy) | **POST** /browser/{browser_id}/gui_hover_xy | GUI hover at coordinates
*BrowserApi* | [**guiPressKeysXy**](docs/BrowserApi.md#guipresskeysxy) | **POST** /browser/{browser_id}/gui_press_keys_xy | Press keys at coordinates (click to focus, then send keys)
*BrowserApi* | [**guiTypeXy**](docs/BrowserApi.md#guitypexy) | **POST** /browser/{browser_id}/gui_type_xy | GUI type at coordinates - clicks then types text
*BrowserApi* | [**history**](docs/BrowserApi.md#history) | **POST** /browser/{browser_id}/history | History: back, forward, or refresh
*BrowserApi* | [**mouse**](docs/BrowserApi.md#mouse) | **POST** /browser/{browser_id}/mouse | Mouse: hover or drag
*BrowserApi* | [**navigateBrowser**](docs/BrowserApi.md#navigatebrowser) | **POST** /browser/{browser_id}/navigate | Navigate to URL
*BrowserApi* | [**networkLogs**](docs/BrowserApi.md#networklogs) | **POST** /browser/{browser_id}/network_logs | Network logs: get or clear
*BrowserApi* | [**performance**](docs/BrowserApi.md#performance) | **POST** /browser/{browser_id}/performance | Performance: start_trace, stop_trace, metrics, analyze
*BrowserApi* | [**pressKeys**](docs/BrowserApi.md#presskeys) | **POST** /browser/{browser_id}/press_keys | Press keyboard keys
*BrowserApi* | [**resize**](docs/BrowserApi.md#resize) | **POST** /browser/{browser_id}/resize | Resize viewport
*BrowserApi* | [**scroll**](docs/BrowserApi.md#scroll) | **POST** /browser/{browser_id}/scroll | Scroll to element/coords or by delta
*BrowserApi* | [**select**](docs/BrowserApi.md#select) | **POST** /browser/{browser_id}/select | Select dropdown: select option or get options
*BrowserApi* | [**snapshot**](docs/BrowserApi.md#snapshot) | **POST** /browser/{browser_id}/snapshot | DOM or accessibility snapshot
*BrowserApi* | [**tabs**](docs/BrowserApi.md#tabs) | **POST** /browser/{browser_id}/tabs | Tabs: list, new, switch, close, current
*BrowserApi* | [**takeScreenshot**](docs/BrowserApi.md#takescreenshot) | **POST** /browser/{browser_id}/screenshot | Take screenshot
*BrowserApi* | [**typeText**](docs/BrowserApi.md#typetext) | **POST** /browser/{browser_id}/type | Type text into element
*BrowserApi* | [**uploadFile**](docs/BrowserApi.md#uploadfile) | **POST** /browser/{browser_id}/upload_file | Upload file to input
*BrowserApi* | [**waitElement**](docs/BrowserApi.md#waitelement) | **POST** /browser/{browser_id}/wait_element | Wait for element to be visible or hidden
*BrowserApi* | [**whatIsVisible**](docs/BrowserApi.md#whatisvisible) | **POST** /browser/{browser_id}/what_is_visible | AI page analysis - what\&#39;s visible
*HealthApi* | [**healthCheck**](docs/HealthApi.md#healthcheck) | **GET** /health/ | Check the health status of the browser pool
*HealthApi* | [**prometheusMetrics**](docs/HealthApi.md#prometheusmetrics) | **GET** /health/metrics | Get Prometheus-style metrics for monitoring
*PoolApi* | [**scalePool**](docs/PoolApi.md#scalepool) | **POST** /pool/scale | Scale the browser pool to a new maximum size
*PoolApi* | [**shutdownServer**](docs/PoolApi.md#shutdownserver) | **POST** /pool/shutdown | Gracefully shutdown the browser pool server
*ProfilesApi* | [**createProfile**](docs/ProfilesApi.md#createprofile) | **POST** /profiles/ | Create a new browser profile
*ProfilesApi* | [**deleteProfile**](docs/ProfilesApi.md#deleteprofile) | **DELETE** /profiles/{profile_name} | Delete a browser profile
*ProfilesApi* | [**getProfile**](docs/ProfilesApi.md#getprofile) | **GET** /profiles/{profile_name} | Get profile information
*ProfilesApi* | [**listProfiles**](docs/ProfilesApi.md#listprofiles) | **GET** /profiles/ | List all browser profiles


### Documentation For Models

 - [BaseResponse](docs/BaseResponse.md)
 - [BrowsersRequest](docs/BrowsersRequest.md)
 - [ClickRequest](docs/ClickRequest.md)
 - [ConsoleLogsRequest](docs/ConsoleLogsRequest.md)
 - [CreateBrowserRequest](docs/CreateBrowserRequest.md)
 - [CreateProfileRequest](docs/CreateProfileRequest.md)
 - [DetectCoordinatesRequest](docs/DetectCoordinatesRequest.md)
 - [DialogRequest](docs/DialogRequest.md)
 - [EmulateRequest](docs/EmulateRequest.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [ExecuteScriptRequest](docs/ExecuteScriptRequest.md)
 - [FillFormRequest](docs/FillFormRequest.md)
 - [GenericResponse](docs/GenericResponse.md)
 - [GuiClickRequest](docs/GuiClickRequest.md)
 - [GuiHoverXyRequest](docs/GuiHoverXyRequest.md)
 - [GuiPressKeysXyRequest](docs/GuiPressKeysXyRequest.md)
 - [GuiTypeXyRequest](docs/GuiTypeXyRequest.md)
 - [HealthStatus](docs/HealthStatus.md)
 - [HistoryRequest](docs/HistoryRequest.md)
 - [MouseRequest](docs/MouseRequest.md)
 - [NavigateBrowserRequest](docs/NavigateBrowserRequest.md)
 - [NetworkLogsRequest](docs/NetworkLogsRequest.md)
 - [PerformanceRequest](docs/PerformanceRequest.md)
 - [PoolScaled](docs/PoolScaled.md)
 - [PressKeysRequest](docs/PressKeysRequest.md)
 - [ProfileInfo](docs/ProfileInfo.md)
 - [ProfileListData](docs/ProfileListData.md)
 - [ProfileListResponse](docs/ProfileListResponse.md)
 - [ProfileResponse](docs/ProfileResponse.md)
 - [ResizeRequest](docs/ResizeRequest.md)
 - [ScaleData](docs/ScaleData.md)
 - [ScalePool](docs/ScalePool.md)
 - [ScrollRequest](docs/ScrollRequest.md)
 - [SelectRequest](docs/SelectRequest.md)
 - [SnapshotRequest](docs/SnapshotRequest.md)
 - [TabsRequest](docs/TabsRequest.md)
 - [TakeScreenshotRequest](docs/TakeScreenshotRequest.md)
 - [TypeTextRequest](docs/TypeTextRequest.md)
 - [UploadFileRequest](docs/UploadFileRequest.md)
 - [WaitElementRequest](docs/WaitElementRequest.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.

