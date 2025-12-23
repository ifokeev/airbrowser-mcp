# PressKeysRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type: css, id, name, xpath | [optional] [default to 'css']
**keys** | **string** | Keys to press | [default to undefined]

## Example

```typescript
import { PressKeysRequest } from 'airbrowser-client';

const instance: PressKeysRequest = {
    selector,
    by,
    keys,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
