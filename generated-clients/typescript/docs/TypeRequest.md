# TypeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type: css, id, name, xpath | [optional] [default to 'css']
**text** | **string** | Text to type | [default to undefined]
**timeout** | **number** | Timeout in seconds | [optional] [default to undefined]

## Example

```typescript
import { TypeRequest } from 'airbrowser-client';

const instance: TypeRequest = {
    selector,
    by,
    text,
    timeout,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
