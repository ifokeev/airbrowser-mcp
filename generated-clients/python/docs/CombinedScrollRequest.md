# CombinedScrollRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector to scroll to | [optional] 
**by** | **str** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**x** | **int** | X coordinate to scroll to (absolute) | [optional] 
**y** | **int** | Y coordinate to scroll to (absolute) | [optional] 
**delta_x** | **int** | Horizontal scroll amount (relative) | [optional] 
**delta_y** | **int** | Vertical scroll amount (relative) | [optional] 
**behavior** | **str** | Scroll behavior: smooth or instant | [optional] [default to 'smooth']

## Example

```python
from airbrowser_client.models.combined_scroll_request import CombinedScrollRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CombinedScrollRequest from a JSON string
combined_scroll_request_instance = CombinedScrollRequest.from_json(json)
# print the JSON string representation of the object
print(CombinedScrollRequest.to_json())

# convert the object into a dict
combined_scroll_request_dict = combined_scroll_request_instance.to_dict()
# create an instance of CombinedScrollRequest from a dict
combined_scroll_request_from_dict = CombinedScrollRequest.from_dict(combined_scroll_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


