# CombinedScrollRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector to scroll to | [optional] [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**x** | **number** | X coordinate to scroll to (absolute) | [optional] [default to undefined]
**y** | **number** | Y coordinate to scroll to (absolute) | [optional] [default to undefined]
**delta_x** | **number** | Horizontal scroll amount (relative) | [optional] [default to undefined]
**delta_y** | **number** | Vertical scroll amount (relative) | [optional] [default to undefined]
**behavior** | **string** | Scroll behavior: smooth or instant | [optional] [default to 'smooth']

## Example

```typescript
import { CombinedScrollRequest } from 'airbrowser-client';

const instance: CombinedScrollRequest = {
    selector,
    by,
    x,
    y,
    delta_x,
    delta_y,
    behavior,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
