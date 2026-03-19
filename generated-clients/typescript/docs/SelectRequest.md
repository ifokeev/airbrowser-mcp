# SelectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | selector | [default to undefined]
**action** | **string** | action | [optional] [default to ActionEnum_Select]
**value** | **string** | value | [optional] [default to undefined]
**text** | **string** | text | [optional] [default to undefined]
**index** | **number** | index | [optional] [default to undefined]
**by** | **string** | by | [optional] [default to 'css']

## Example

```typescript
import { SelectRequest } from 'airbrowser-client';

const instance: SelectRequest = {
    selector,
    action,
    value,
    text,
    index,
    by,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
