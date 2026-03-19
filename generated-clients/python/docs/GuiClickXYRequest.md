# GuiClickXYRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **float** | Screen X coordinate |
**y** | **float** | Screen Y coordinate |
**timeframe** | **float** | Mouse move duration (seconds) | [optional]
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
from airbrowser_client.models.gui_click_xy_request import GuiClickXYRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuiClickXYRequest from a JSON string
gui_click_xy_request_instance = GuiClickXYRequest.from_json(json)
# print the JSON string representation of the object
print(GuiClickXYRequest.to_json())

# convert the object into a dict
gui_click_xy_request_dict = gui_click_xy_request_instance.to_dict()
# create an instance of GuiClickXYRequest from a dict
gui_click_xy_request_from_dict = GuiClickXYRequest.from_dict(gui_click_xy_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
