# ClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector | [default to undefined]
**by** | **string** | Selector type: css, id, name, xpath | [optional] [default to 'css']
**timeout** | **number** | Timeout in seconds | [optional] [default to undefined]
**if_visible** | **boolean** | Only click if element is visible | [optional] [default to false]

## Example

```typescript
import { ClickRequest } from 'airbrowser-client';

const instance: ClickRequest = {
    selector,
    by,
    timeout,
    if_visible,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
