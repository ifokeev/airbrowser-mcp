# PoolScaled


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ScaleData**](ScaleData.md) | Scale result | [optional] 
**message** | **str** | Status message | 
**success** | **bool** | Operation success | 
**timestamp** | **float** | Unix timestamp | 

## Example

```python
from airbrowser_client.models.pool_scaled import PoolScaled

# TODO update the JSON string below
json = "{}"
# create an instance of PoolScaled from a JSON string
pool_scaled_instance = PoolScaled.from_json(json)
# print the JSON string representation of the object
print(PoolScaled.to_json())

# convert the object into a dict
pool_scaled_dict = pool_scaled_instance.to_dict()
# create an instance of PoolScaled from a dict
pool_scaled_from_dict = PoolScaled.from_dict(pool_scaled_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


