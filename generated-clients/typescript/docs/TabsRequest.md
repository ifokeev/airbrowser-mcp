# TabsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **string** | Tab action: list, new, switch, close, or current | [default to undefined]
**url** | **string** | URL for new tab (for \&#39;new\&#39; action) | [optional] [default to undefined]
**index** | **number** | Tab index (for \&#39;switch\&#39; or \&#39;close\&#39; actions) | [optional] [default to undefined]
**handle** | **string** | Tab handle (for \&#39;switch\&#39; or \&#39;close\&#39; actions) | [optional] [default to undefined]

## Example

```typescript
import { TabsRequest } from 'airbrowser-client';

const instance: TabsRequest = {
    action,
    url,
    index,
    handle,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
