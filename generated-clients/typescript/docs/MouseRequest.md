# MouseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **string** | Action: hover or drag | [default to undefined]
**selector** | **string** | Element selector (for hover) | [optional] [default to undefined]
**source** | **string** | Source selector (for drag) | [optional] [default to undefined]
**target** | **string** | Target selector (for drag) | [optional] [default to undefined]
**by** | **string** | Selector type: css, id, name, xpath | [optional] [default to 'css']

## Example

```typescript
import { MouseRequest } from 'airbrowser-client';

const instance: MouseRequest = {
    action,
    selector,
    source,
    target,
    by,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
