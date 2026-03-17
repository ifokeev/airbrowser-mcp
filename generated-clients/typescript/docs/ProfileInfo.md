# ProfileInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**in_use** | **boolean** | Whether profile is currently in use by a browser | [optional] [default to undefined]
**last_used** | **string** | Last used timestamp (ISO format) | [optional] [default to undefined]
**name** | **string** | Profile name | [optional] [default to undefined]
**path** | **string** | Profile storage path | [optional] [default to undefined]
**size_mb** | **number** | Profile size in MB | [optional] [default to undefined]

## Example

```typescript
import { ProfileInfo } from 'airbrowser-client';

const instance: ProfileInfo = {
    in_use,
    last_used,
    name,
    path,
    size_mb,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
