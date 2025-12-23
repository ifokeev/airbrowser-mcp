# PerformanceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **string** | Performance action: start_trace, stop_trace, metrics, or analyze | [default to undefined]
**categories** | **string** | Comma-separated trace categories (for start_trace) | [optional] [default to undefined]

## Example

```typescript
import { PerformanceRequest } from 'airbrowser-client';

const instance: PerformanceRequest = {
    action,
    categories,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
