# CreateBrowserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uc** | **boolean** | uc | [optional] [default to true]
**proxy** | **string** | proxy | [optional] [default to undefined]
**window_size** | **Array&lt;number&gt;** | window_size | [optional] [default to undefined]
**user_agent** | **string** | user_agent | [optional] [default to undefined]
**disable_gpu** | **boolean** | disable_gpu | [optional] [default to false]
**disable_images** | **boolean** | disable_images | [optional] [default to false]
**disable_javascript** | **boolean** | disable_javascript | [optional] [default to false]
**extensions** | **Array&lt;string&gt;** | extensions | [optional] [default to undefined]
**custom_args** | **Array&lt;string&gt;** | custom_args | [optional] [default to undefined]
**profile_name** | **string** | profile_name | [optional] [default to undefined]

## Example

```typescript
import { CreateBrowserRequest } from 'airbrowser-client';

const instance: CreateBrowserRequest = {
    uc,
    proxy,
    window_size,
    user_agent,
    disable_gpu,
    disable_images,
    disable_javascript,
    extensions,
    custom_args,
    profile_name,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
