# ConsoleLogsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**limit** | **int** | limit | [optional] 

## Example

```python
from airbrowser_client.models.console_logs_request import ConsoleLogsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConsoleLogsRequest from a JSON string
console_logs_request_instance = ConsoleLogsRequest.from_json(json)
# print the JSON string representation of the object
print(ConsoleLogsRequest.to_json())

# convert the object into a dict
console_logs_request_dict = console_logs_request_instance.to_dict()
# create an instance of ConsoleLogsRequest from a dict
console_logs_request_from_dict = ConsoleLogsRequest.from_dict(console_logs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


