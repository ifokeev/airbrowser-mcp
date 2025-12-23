# LogsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | **object** | Log entries | [optional] 

## Example

```python
from airbrowser_client.models.logs_response import LogsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LogsResponse from a JSON string
logs_response_instance = LogsResponse.from_json(json)
# print the JSON string representation of the object
print(LogsResponse.to_json())

# convert the object into a dict
logs_response_dict = logs_response_instance.to_dict()
# create an instance of LogsResponse from a dict
logs_response_from_dict = LogsResponse.from_dict(logs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


