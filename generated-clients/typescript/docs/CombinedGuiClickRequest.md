# CombinedGuiClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector (for selector mode) | [optional] [default to undefined]
**x** | **number** | Screen X coordinate (for coordinate mode) | [optional] [default to undefined]
**y** | **number** | Screen Y coordinate (for coordinate mode) | [optional] [default to undefined]
**timeframe** | **number** | Mouse move duration (seconds) | [optional] [default to undefined]
**fx** | **number** | Relative X (0..1) within element to click | [optional] [default to undefined]
**fy** | **number** | Relative Y (0..1) within element to click | [optional] [default to undefined]

## Example

```typescript
import { CombinedGuiClickRequest } from 'airbrowser-client';

const instance: CombinedGuiClickRequest = {
    selector,
    x,
    y,
    timeframe,
    fx,
    fy,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
