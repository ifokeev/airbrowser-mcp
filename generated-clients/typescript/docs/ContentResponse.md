# ContentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **boolean** | Operation success | [default to undefined]
**message** | **string** | Status message | [default to undefined]
**timestamp** | **number** | Unix timestamp | [default to undefined]
**data** | [**ContentData**](ContentData.md) | Page content data | [optional] [default to undefined]

## Example

```typescript
import { ContentResponse } from 'airbrowser-client';

const instance: ContentResponse = {
    success,
    message,
    timestamp,
    data,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
