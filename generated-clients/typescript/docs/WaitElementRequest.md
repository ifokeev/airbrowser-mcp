# WaitElementRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**until** | **string** | Wait until: visible or hidden | [default to undefined]
**timeout** | **number** | Timeout in seconds | [optional] [default to undefined]

## Example

```typescript
import { WaitElementRequest } from 'airbrowser-client';

const instance: WaitElementRequest = {
    selector,
    by,
    until,
    timeout,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
