# ClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | 
**timeout** | **int** | timeout | [optional] 
**by** | **str** | by | [optional] [default to 'css']
**if_visible** | **bool** | if_visible | [optional] [default to False]

## Example

```python
from airbrowser_client.models.click_request import ClickRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClickRequest from a JSON string
click_request_instance = ClickRequest.from_json(json)
# print the JSON string representation of the object
print(ClickRequest.to_json())

# convert the object into a dict
click_request_dict = click_request_instance.to_dict()
# create an instance of ClickRequest from a dict
click_request_from_dict = ClickRequest.from_dict(click_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


