# ScalePool


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_size** | **int** | New maximum number of browsers | 

## Example

```python
from airbrowser_client.models.scale_pool import ScalePool

# TODO update the JSON string below
json = "{}"
# create an instance of ScalePool from a JSON string
scale_pool_instance = ScalePool.from_json(json)
# print the JSON string representation of the object
print(ScalePool.to_json())

# convert the object into a dict
scale_pool_dict = scale_pool_instance.to_dict()
# create an instance of ScalePool from a dict
scale_pool_from_dict = ScalePool.from_dict(scale_pool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


