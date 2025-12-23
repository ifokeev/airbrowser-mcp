# HistoryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | History action: back, forward, or refresh | 

## Example

```python
from airbrowser_client.models.history_request import HistoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of HistoryRequest from a JSON string
history_request_instance = HistoryRequest.from_json(json)
# print the JSON string representation of the object
print(HistoryRequest.to_json())

# convert the object into a dict
history_request_dict = history_request_instance.to_dict()
# create an instance of HistoryRequest from a dict
history_request_from_dict = HistoryRequest.from_dict(history_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


