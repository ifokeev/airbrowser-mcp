# airbrowser_client.ProfilesApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_profile**](ProfilesApi.md#create_profile) | **POST** /profiles/ | Create a new browser profile
[**delete_profile**](ProfilesApi.md#delete_profile) | **DELETE** /profiles/{profile_name} | Delete a browser profile
[**get_profile**](ProfilesApi.md#get_profile) | **GET** /profiles/{profile_name} | Get profile information
[**list_profiles**](ProfilesApi.md#list_profiles) | **GET** /profiles/ | List all browser profiles


# **create_profile**
> ProfileResponse create_profile(payload)

Create a new browser profile

### Example


```python
import airbrowser_client
from airbrowser_client.models.create_profile_request import CreateProfileRequest
from airbrowser_client.models.profile_response import ProfileResponse
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.ProfilesApi(api_client)
    payload = airbrowser_client.CreateProfileRequest() # CreateProfileRequest | 

    try:
        # Create a new browser profile
        api_response = api_instance.create_profile(payload)
        print("The response of ProfilesApi->create_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->create_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**CreateProfileRequest**](CreateProfileRequest.md)|  | 

### Return type

[**ProfileResponse**](ProfileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**400** | Bad request |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_profile**
> delete_profile(profile_name)

Delete a browser profile

### Example


```python
import airbrowser_client
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.ProfilesApi(api_client)
    profile_name = 'profile_name_example' # str | Profile name

    try:
        # Delete a browser profile
        api_instance.delete_profile(profile_name)
    except Exception as e:
        print("Exception when calling ProfilesApi->delete_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_name** | **str**| Profile name | 

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
**404** | Profile not found |  -  |
**400** | Profile in use |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile**
> ProfileResponse get_profile(profile_name)

Get profile information

### Example


```python
import airbrowser_client
from airbrowser_client.models.profile_response import ProfileResponse
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.ProfilesApi(api_client)
    profile_name = 'profile_name_example' # str | Profile name

    try:
        # Get profile information
        api_response = api_instance.get_profile(profile_name)
        print("The response of ProfilesApi->get_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->get_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_name** | **str**| Profile name | 

### Return type

[**ProfileResponse**](ProfileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**404** | Profile not found |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_profiles**
> ProfileListResponse list_profiles()

List all browser profiles

### Example


```python
import airbrowser_client
from airbrowser_client.models.profile_list_response import ProfileListResponse
from airbrowser_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = airbrowser_client.Configuration(
    host = "/api/v1"
)


# Enter a context with an instance of the API client
with airbrowser_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = airbrowser_client.ProfilesApi(api_client)

    try:
        # List all browser profiles
        api_response = api_instance.list_profiles()
        print("The response of ProfilesApi->list_profiles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfilesApi->list_profiles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ProfileListResponse**](ProfileListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

