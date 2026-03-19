# GuiClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector (CSS or XPath) | [optional]
**x** | **float** | Screen X coordinate (coordinate mode) | [optional]
**y** | **float** | Screen Y coordinate (coordinate mode) | [optional]
**timeframe** | **float** | Mouse move duration (seconds) | [optional]
**fx** | **float** | Relative X (0..1) within element to click | [optional]
**fy** | **float** | Relative Y (0..1) within element to click | [optional]
**pre_click_validate** | **str** | Pre-click validation mode | [optional] [default to 'off']
**auto_snap** | **str** | Auto-snap mode for nearby targets | [optional] [default to 'off']
**snap_radius** | **float** | Maximum snap radius in CSS pixels | [optional]
**post_click_feedback** | **str** | Post-click feedback mode | [optional] [default to 'none']
**post_click_timeout_ms** | **int** | Post-click observation timeout in milliseconds | [optional]
**return_content** | **bool** | Include truncated content in post-click feedback | [optional] [default to False]
**content_limit_chars** | **int** | Maximum returned content length | [optional]
**include_debug** | **bool** | Include smart-click debug diagnostics | [optional] [default to False]

## Example

```python
from airbrowser_client.models.gui_click_request import GuiClickRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuiClickRequest from a JSON string
gui_click_request_instance = GuiClickRequest.from_json(json)
# print the JSON string representation of the object
print(GuiClickRequest.to_json())

# convert the object into a dict
gui_click_request_dict = gui_click_request_instance.to_dict()
# create an instance of GuiClickRequest from a dict
gui_click_request_from_dict = GuiClickRequest.from_dict(gui_click_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
