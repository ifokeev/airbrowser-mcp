# CombinedGuiClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector (for selector mode) | [optional] 
**x** | **float** | Screen X coordinate (for coordinate mode) | [optional] 
**y** | **float** | Screen Y coordinate (for coordinate mode) | [optional] 
**timeframe** | **float** | Mouse move duration (seconds) | [optional] 
**fx** | **float** | Relative X (0..1) within element to click | [optional] 
**fy** | **float** | Relative Y (0..1) within element to click | [optional] 

## Example

```python
from airbrowser_client.models.combined_gui_click_request import CombinedGuiClickRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CombinedGuiClickRequest from a JSON string
combined_gui_click_request_instance = CombinedGuiClickRequest.from_json(json)
# print the JSON string representation of the object
print(CombinedGuiClickRequest.to_json())

# convert the object into a dict
combined_gui_click_request_dict = combined_gui_click_request_instance.to_dict()
# create an instance of CombinedGuiClickRequest from a dict
combined_gui_click_request_from_dict = CombinedGuiClickRequest.from_dict(combined_gui_click_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


