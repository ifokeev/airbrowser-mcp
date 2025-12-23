# ElementDataRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**type** | **string** | Data type: text, attribute, or property | [default to undefined]
**name** | **string** | Attribute/property name (required for attribute/property) | [optional] [default to undefined]

## Example

```typescript
import { ElementDataRequest } from 'airbrowser-client';

const instance: ElementDataRequest = {
    selector,
    by,
    type,
    name,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
