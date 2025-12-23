# WhatIsVisibleResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **boolean** | Operation success | [optional] [default to undefined]
**message** | **string** | Success message | [optional] [default to undefined]
**timestamp** | **number** | Unix timestamp | [optional] [default to undefined]
**analysis** | **string** | Comprehensive page state analysis | [optional] [default to undefined]
**model** | **string** | AI model used for analysis | [optional] [default to undefined]
**screenshot_url** | **string** | URL to the screenshot | [optional] [default to undefined]
**screenshot_path** | **string** | Path to the screenshot file | [optional] [default to undefined]
**error** | **string** | Error message if failed | [optional] [default to undefined]

## Example

```typescript
import { WhatIsVisibleResult } from 'airbrowser-client';

const instance: WhatIsVisibleResult = {
    success,
    message,
    timestamp,
    analysis,
    model,
    screenshot_url,
    screenshot_path,
    error,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
