# airbrowser_client.PoolApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**scale_pool**](PoolApi.md#scale_pool) | **POST** /pool/scale | Scale the browser pool to a new maximum size
[**shutdown_server**](PoolApi.md#shutdown_server) | **POST** /pool/shutdown | Gracefully shutdown the browser pool server


# **scale_pool**
> PoolScaled scale_pool(payload)

Scale the browser pool to a new maximum size

### Example


```python
import airbrowser_client
from airbrowser_client.models.pool_scaled import PoolScaled
from airbrowser_client.models.scale_pool import ScalePool
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
    api_instance = airbrowser_client.PoolApi(api_client)
    payload = airbrowser_client.ScalePool() # ScalePool | 

    try:
        # Scale the browser pool to a new maximum size
        api_response = api_instance.scale_pool(payload)
        print("The response of PoolApi->scale_pool:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PoolApi->scale_pool: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**ScalePool**](ScalePool.md)|  | 

### Return type

[**PoolScaled**](PoolScaled.md)

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

# **shutdown_server**
> BaseResponse shutdown_server()

Gracefully shutdown the browser pool server

### Example


```python
import airbrowser_client
from airbrowser_client.models.base_response import BaseResponse
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
    api_instance = airbrowser_client.PoolApi(api_client)

    try:
        # Gracefully shutdown the browser pool server
        api_response = api_instance.shutdown_server()
        print("The response of PoolApi->shutdown_server:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PoolApi->shutdown_server: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BaseResponse**](BaseResponse.md)

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

