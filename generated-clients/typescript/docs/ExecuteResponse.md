# ExecuteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **boolean** | Operation success | [default to undefined]
**message** | **string** | Status message | [default to undefined]
**timestamp** | **number** | Unix timestamp | [default to undefined]
**data** | [**ExecuteData**](ExecuteData.md) | Execution result | [optional] [default to undefined]

## Example

```typescript
import { ExecuteResponse } from 'airbrowser-client';

const instance: ExecuteResponse = {
    success,
    message,
    timestamp,
    data,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
