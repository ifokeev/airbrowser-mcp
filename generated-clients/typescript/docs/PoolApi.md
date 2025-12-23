# PoolApi

All URIs are relative to */api/v1*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**scalePool**](#scalepool) | **POST** /pool/scale | Scale the browser pool to a new maximum size|
|[**shutdownServer**](#shutdownserver) | **POST** /pool/shutdown | Gracefully shutdown the browser pool server|

# **scalePool**
> PoolScaled scalePool(payload)


### Example

```typescript
import {
    PoolApi,
    Configuration,
    ScalePool
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new PoolApi(configuration);

let payload: ScalePool; //

const { status, data } = await apiInstance.scalePool(
    payload
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **payload** | **ScalePool**|  | |


### Return type

**PoolScaled**

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

# **shutdownServer**
> BaseResponse shutdownServer()


### Example

```typescript
import {
    PoolApi,
    Configuration
} from 'airbrowser-client';

const configuration = new Configuration();
const apiInstance = new PoolApi(configuration);

const { status, data } = await apiInstance.shutdownServer();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**BaseResponse**

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

