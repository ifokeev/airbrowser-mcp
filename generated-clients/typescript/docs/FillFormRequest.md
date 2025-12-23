# FillFormRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**Array&lt;FormField&gt;**](FormField.md) | Fields to fill | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']

## Example

```typescript
import { FillFormRequest } from 'airbrowser-client';

const instance: FillFormRequest = {
    fields,
    by,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
