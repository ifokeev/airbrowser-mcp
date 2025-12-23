# UploadFileRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | File input selector | [default to undefined]
**file_path** | **string** | Path to file to upload | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']

## Example

```typescript
import { UploadFileRequest } from 'airbrowser-client';

const instance: UploadFileRequest = {
    selector,
    file_path,
    by,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
