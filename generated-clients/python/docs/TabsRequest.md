# TabsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**url** | **str** | url | [optional] 
**index** | **int** | index | [optional] 
**handle** | **str** | handle | [optional] 

## Example

```python
from airbrowser_client.models.tabs_request import TabsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TabsRequest from a JSON string
tabs_request_instance = TabsRequest.from_json(json)
# print the JSON string representation of the object
print(TabsRequest.to_json())

# convert the object into a dict
tabs_request_dict = tabs_request_instance.to_dict()
# create an instance of TabsRequest from a dict
tabs_request_from_dict = TabsRequest.from_dict(tabs_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


