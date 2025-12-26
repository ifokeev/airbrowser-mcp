# MouseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**selector** | **str** | selector | [optional] 
**source** | **str** | source | [optional] 
**target** | **str** | target | [optional] 
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.mouse_request import MouseRequest

# TODO update the JSON string below
json = "{}"
# create an instance of MouseRequest from a JSON string
mouse_request_instance = MouseRequest.from_json(json)
# print the JSON string representation of the object
print(MouseRequest.to_json())

# convert the object into a dict
mouse_request_dict = mouse_request_instance.to_dict()
# create an instance of MouseRequest from a dict
mouse_request_from_dict = MouseRequest.from_dict(mouse_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


