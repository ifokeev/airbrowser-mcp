# ProfilesApi

All URIs are relative to */api/v1*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createProfile**](#createprofile) | **POST** /profiles/ | Create a new browser profile|
|[**deleteProfile**](#deleteprofile) | **DELETE** /profiles/{profile_name} | Delete a browser profile|
|[**getProfile**](#getprofile) | **GET** /profiles/{profile_name} | Get profile information|
|[**listProfiles**](#listprofiles) | **GET** /profiles/ | List all browser profiles|

# **createProfile**
> ProfileResponse createProfile(payload)


### Example

```typescript
import {
    ProfilesApi,
    Configuration,
    CreateProfileRequest
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new ProfilesApi(configuration);

let payload: CreateProfileRequest; //

const { status, data } = await apiInstance.createProfile(
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **CreateProfileRequest**|  | |


### Return type

**ProfileResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**400** | Bad request |  -  |
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteProfile**
> deleteProfile()


### Example

```typescript
import {
    ProfilesApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new ProfilesApi(configuration);

let profileName: string; //Profile name (default to undefined)

const { status, data } = await apiInstance.deleteProfile(
    profileName
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **profileName** | [**string**] | Profile name | defaults to undefined|


### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**404** | Profile not found |  -  |
|**400** | Profile in use |  -  |
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProfile**
> ProfileResponse getProfile()


### Example

```typescript
import {
    ProfilesApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new ProfilesApi(configuration);

let profileName: string; //Profile name (default to undefined)

const { status, data } = await apiInstance.getProfile(
    profileName
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **profileName** | [**string**] | Profile name | defaults to undefined|


### Return type

**ProfileResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**404** | Profile not found |  -  |
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **listProfiles**
> ProfileListResponse listProfiles()


### Example

```typescript
import {
    ProfilesApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new ProfilesApi(configuration);

const { status, data } = await apiInstance.listProfiles();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**ProfileListResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

