# TabsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Tab action: list, new, switch, close, or current | 
**url** | **str** | URL for new tab (for &#39;new&#39; action) | [optional] 
**index** | **int** | Tab index (for &#39;switch&#39; or &#39;close&#39; actions) | [optional] 
**handle** | **str** | Tab handle (for &#39;switch&#39; or &#39;close&#39; actions) | [optional] 

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


