# DetectCoordinatesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **string** | Natural language description of element to find | [default to undefined]
**fx** | **number** | Relative X (0..1) within the detected element | [optional] [default to undefined]
**fy** | **number** | Relative Y (0..1) within the detected element | [optional] [default to undefined]
**model** | **string** | Optional vision model override for this request | [optional] [default to undefined]
**hit_test** | **string** | Detect-time validation mode | [optional] [default to HitTestEnum_Off]
**auto_snap** | **string** | Auto-snap mode for nearby targets | [optional] [default to AutoSnapEnum_Off]
**snap_radius** | **number** | Maximum snap radius in CSS pixels | [optional] [default to undefined]
**include_debug** | **boolean** | Include smart-targeting debug details | [optional] [default to false]

## Example

```typescript
import { DetectCoordinatesRequest } from 'airbrowser-client';

const instance: DetectCoordinatesRequest = {
    prompt,
    fx,
    fy,
    model,
    hit_test,
    auto_snap,
    snap_radius,
    include_debug,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
