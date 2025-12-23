# ExecuteRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**script** | **str** | JavaScript code to execute | 
**timeout** | **int** | Timeout in seconds | [optional] 

## Example

```python
from airbrowser_client.models.execute_request import ExecuteRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteRequest from a JSON string
execute_request_instance = ExecuteRequest.from_json(json)
# print the JSON string representation of the object
print(ExecuteRequest.to_json())

# convert the object into a dict
execute_request_dict = execute_request_instance.to_dict()
# create an instance of ExecuteRequest from a dict
execute_request_from_dict = ExecuteRequest.from_dict(execute_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


