# GuiClickResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | [optional]
**message** | **str** | Success message | [optional]
**data** | [**GuiClickData**](GuiClickData.md) | GUI click response payload | [optional]

## Example

```python
from airbrowser_client.models.gui_click_result import GuiClickResult

# TODO update the JSON string below
json = "{}"
# create an instance of GuiClickResult from a JSON string
gui_click_result_instance = GuiClickResult.from_json(json)
# print the JSON string representation of the object
print(GuiClickResult.to_json())

# convert the object into a dict
gui_click_result_dict = gui_click_result_instance.to_dict()
# create an instance of GuiClickResult from a dict
gui_click_result_from_dict = GuiClickResult.from_dict(gui_click_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
