# PoolStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | **object** | Pool status information | [optional] 

## Example

```python
from airbrowser_client.models.pool_status_response import PoolStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PoolStatusResponse from a JSON string
pool_status_response_instance = PoolStatusResponse.from_json(json)
# print the JSON string representation of the object
print(PoolStatusResponse.to_json())

# convert the object into a dict
pool_status_response_dict = pool_status_response_instance.to_dict()
# create an instance of PoolStatusResponse from a dict
pool_status_response_from_dict = PoolStatusResponse.from_dict(pool_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


