# ExecuteScriptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**script** | **str** | script | 

## Example

```python
from airbrowser_client.models.execute_script_request import ExecuteScriptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteScriptRequest from a JSON string
execute_script_request_instance = ExecuteScriptRequest.from_json(json)
# print the JSON string representation of the object
print(ExecuteScriptRequest.to_json())

# convert the object into a dict
execute_script_request_dict = execute_script_request_instance.to_dict()
# create an instance of ExecuteScriptRequest from a dict
execute_script_request_from_dict = ExecuteScriptRequest.from_dict(execute_script_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


