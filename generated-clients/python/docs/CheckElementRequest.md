# CheckElementRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector | 
**by** | **str** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**check** | **str** | Check type: exists or visible | 

## Example

```python
from airbrowser_client.models.check_element_request import CheckElementRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CheckElementRequest from a JSON string
check_element_request_instance = CheckElementRequest.from_json(json)
# print the JSON string representation of the object
print(CheckElementRequest.to_json())

# convert the object into a dict
check_element_request_dict = check_element_request_instance.to_dict()
# create an instance of CheckElementRequest from a dict
check_element_request_from_dict = CheckElementRequest.from_dict(check_element_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


