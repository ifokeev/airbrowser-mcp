# GuiClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fx** | **float** | fx | [optional] 
**fy** | **float** | fy | [optional] 
**selector** | **str** | selector | [optional] 
**timeframe** | **float** | timeframe | [optional] 
**x** | **float** | x | [optional] 
**y** | **float** | y | [optional] 

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


