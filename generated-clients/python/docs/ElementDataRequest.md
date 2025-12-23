# ElementDataRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector | 
**by** | **str** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**type** | **str** | Data type: text, attribute, or property | 
**name** | **str** | Attribute/property name (required for attribute/property) | [optional] 

## Example

```python
from airbrowser_client.models.element_data_request import ElementDataRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ElementDataRequest from a JSON string
element_data_request_instance = ElementDataRequest.from_json(json)
# print the JSON string representation of the object
print(ElementDataRequest.to_json())

# convert the object into a dict
element_data_request_dict = element_data_request_instance.to_dict()
# create an instance of ElementDataRequest from a dict
element_data_request_from_dict = ElementDataRequest.from_dict(element_data_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


