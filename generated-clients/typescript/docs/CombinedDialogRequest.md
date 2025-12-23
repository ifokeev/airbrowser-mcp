# CombinedDialogRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **string** | Dialog action: get, accept, or dismiss | [default to undefined]
**text** | **string** | Text to enter for prompt dialogs (for \&#39;accept\&#39; action) | [optional] [default to undefined]

## Example

```typescript
import { CombinedDialogRequest } from 'airbrowser-client';

const instance: CombinedDialogRequest = {
    action,
    text,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
