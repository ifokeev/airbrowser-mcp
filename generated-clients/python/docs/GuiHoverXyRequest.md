# GuiHoverXyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **float** | x | 
**y** | **float** | y | 
**timeframe** | **float** | timeframe | [optional] 

## Example

```python
from airbrowser_client.models.gui_hover_xy_request import GuiHoverXyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuiHoverXyRequest from a JSON string
gui_hover_xy_request_instance = GuiHoverXyRequest.from_json(json)
# print the JSON string representation of the object
print(GuiHoverXyRequest.to_json())

# convert the object into a dict
gui_hover_xy_request_dict = gui_hover_xy_request_instance.to_dict()
# create an instance of GuiHoverXyRequest from a dict
gui_hover_xy_request_from_dict = GuiHoverXyRequest.from_dict(gui_hover_xy_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


