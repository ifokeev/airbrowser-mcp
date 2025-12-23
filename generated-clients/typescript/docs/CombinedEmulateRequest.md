# CombinedEmulateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **string** | Emulation action: set, clear, or list_devices | [optional] [default to ActionEnum_Set]
**device** | **string** | Device preset name (e.g., iPhone 14, iPad) | [optional] [default to undefined]
**width** | **number** | Custom viewport width | [optional] [default to undefined]
**height** | **number** | Custom viewport height | [optional] [default to undefined]
**device_scale_factor** | **number** | Device pixel ratio | [optional] [default to undefined]
**mobile** | **boolean** | Enable touch events | [optional] [default to undefined]
**user_agent** | **string** | Custom user agent | [optional] [default to undefined]

## Example

```typescript
import { CombinedEmulateRequest } from 'airbrowser-client';

const instance: CombinedEmulateRequest = {
    action,
    device,
    width,
    height,
    device_scale_factor,
    mobile,
    user_agent,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
