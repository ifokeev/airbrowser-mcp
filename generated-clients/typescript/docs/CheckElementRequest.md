# CheckElementRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**check** | **string** | Check type: exists or visible | [default to undefined]

## Example

```typescript
import { CheckElementRequest } from 'airbrowser-client';

const instance: CheckElementRequest = {
    selector,
    by,
    check,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
