# NavigateBrowserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | url | 
**timeout** | **int** | timeout | [optional] 

## Example

```python
from airbrowser_client.models.navigate_browser_request import NavigateBrowserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NavigateBrowserRequest from a JSON string
navigate_browser_request_instance = NavigateBrowserRequest.from_json(json)
# print the JSON string representation of the object
print(NavigateBrowserRequest.to_json())

# convert the object into a dict
navigate_browser_request_dict = navigate_browser_request_instance.to_dict()
# create an instance of NavigateBrowserRequest from a dict
navigate_browser_request_from_dict = NavigateBrowserRequest.from_dict(navigate_browser_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


