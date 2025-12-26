# ScrollRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | [optional] 
**x** | **int** | x | [optional] 
**y** | **int** | y | [optional] 
**delta_x** | **int** | delta_x | [optional] 
**delta_y** | **int** | delta_y | [optional] 
**behavior** | **str** | behavior | [optional] [default to 'smooth']
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.scroll_request import ScrollRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScrollRequest from a JSON string
scroll_request_instance = ScrollRequest.from_json(json)
# print the JSON string representation of the object
print(ScrollRequest.to_json())

# convert the object into a dict
scroll_request_dict = scroll_request_instance.to_dict()
# create an instance of ScrollRequest from a dict
scroll_request_from_dict = ScrollRequest.from_dict(scroll_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


