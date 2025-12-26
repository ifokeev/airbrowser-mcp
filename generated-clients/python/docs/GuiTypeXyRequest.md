# GuiTypeXyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**x** | **float** | x | 
**y** | **float** | y | 
**text** | **str** | text | 
**timeframe** | **float** | timeframe | [optional] 

## Example

```python
from airbrowser_client.models.gui_type_xy_request import GuiTypeXyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuiTypeXyRequest from a JSON string
gui_type_xy_request_instance = GuiTypeXyRequest.from_json(json)
# print the JSON string representation of the object
print(GuiTypeXyRequest.to_json())

# convert the object into a dict
gui_type_xy_request_dict = gui_type_xy_request_instance.to_dict()
# create an instance of GuiTypeXyRequest from a dict
gui_type_xy_request_from_dict = GuiTypeXyRequest.from_dict(gui_type_xy_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


