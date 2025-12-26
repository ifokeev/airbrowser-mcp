# GuiPressKeysXyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **float** | x | 
**y** | **float** | y | 
**keys** | **str** | keys | 
**timeframe** | **float** | timeframe | [optional] 

## Example

```python
from airbrowser_client.models.gui_press_keys_xy_request import GuiPressKeysXyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuiPressKeysXyRequest from a JSON string
gui_press_keys_xy_request_instance = GuiPressKeysXyRequest.from_json(json)
# print the JSON string representation of the object
print(GuiPressKeysXyRequest.to_json())

# convert the object into a dict
gui_press_keys_xy_request_dict = gui_press_keys_xy_request_instance.to_dict()
# create an instance of GuiPressKeysXyRequest from a dict
gui_press_keys_xy_request_from_dict = GuiPressKeysXyRequest.from_dict(gui_press_keys_xy_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


