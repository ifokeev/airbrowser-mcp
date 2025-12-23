# BrowserConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profile_name** | **string** | Profile name for persistent data. Omit for fresh session. | [optional] [default to undefined]
**proxy** | **string** | Proxy server URL | [optional] [default to undefined]
**user_agent** | **string** | Custom user agent string | [optional] [default to undefined]
**window_size** | **Array&lt;number&gt;** | Browser window size [width, height] | [optional] [default to undefined]
**disable_gpu** | **boolean** | Disable GPU acceleration | [optional] [default to false]
**disable_images** | **boolean** | Disable image loading | [optional] [default to false]
**disable_javascript** | **boolean** | Disable JavaScript | [optional] [default to false]
**extensions** | **Array&lt;string&gt;** | Chrome extension paths | [optional] [default to undefined]
**custom_args** | **Array&lt;string&gt;** | Custom Chrome arguments | [optional] [default to undefined]

## Example

```typescript
import { BrowserConfig } from 'airbrowser-client';

const instance: BrowserConfig = {
    profile_name,
    proxy,
    user_agent,
    window_size,
    disable_gpu,
    disable_images,
    disable_javascript,
    extensions,
    custom_args,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
