# GuiClickData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | Legacy inner status | [optional]
**success** | **bool** | Legacy inner success flag | [optional]
**message** | **str** | Legacy inner message | [optional]
**x** | **float** | Requested or resolved screen X coordinate | [optional]
**y** | **float** | Requested or resolved screen Y coordinate | [optional]
**outcome_status** | **str** | Machine-readable click outcome status | [optional]
**reason** | **str** | Machine-readable click reason code | [optional]
**reason_detail** | **str** | Human-readable reason detail | [optional]
**precheck** | **object** | Pre-click validation details | [optional]
**execution** | **object** | Click execution details | [optional]
**postcheck** | **object** | Post-click feedback details | [optional]
**recommended_next_action** | **str** | Suggested next action for callers | [optional]
**debug** | **object** | Optional smart-click debug details | [optional]

## Example

```python
from airbrowser_client.models.gui_click_data import GuiClickData

# TODO update the JSON string below
json = "{}"
# create an instance of GuiClickData from a JSON string
gui_click_data_instance = GuiClickData.from_json(json)
# print the JSON string representation of the object
print(GuiClickData.to_json())

# convert the object into a dict
gui_click_data_dict = gui_click_data_instance.to_dict()
# create an instance of GuiClickData from a dict
gui_click_data_from_dict = GuiClickData.from_dict(gui_click_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
