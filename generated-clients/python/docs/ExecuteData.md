# ExecuteData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **object** | Script execution result | [optional] 

## Example

```python
from airbrowser_client.models.execute_data import ExecuteData

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteData from a JSON string
execute_data_instance = ExecuteData.from_json(json)
# print the JSON string representation of the object
print(ExecuteData.to_json())

# convert the object into a dict
execute_data_dict = execute_data_instance.to_dict()
# create an instance of ExecuteData from a dict
execute_data_from_dict = ExecuteData.from_dict(execute_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


