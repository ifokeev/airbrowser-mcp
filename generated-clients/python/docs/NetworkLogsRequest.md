# NetworkLogsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**limit** | **int** | limit | [optional] 

## Example

```python
from airbrowser_client.models.network_logs_request import NetworkLogsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NetworkLogsRequest from a JSON string
network_logs_request_instance = NetworkLogsRequest.from_json(json)
# print the JSON string representation of the object
print(NetworkLogsRequest.to_json())

# convert the object into a dict
network_logs_request_dict = network_logs_request_instance.to_dict()
# create an instance of NetworkLogsRequest from a dict
network_logs_request_from_dict = NetworkLogsRequest.from_dict(network_logs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


