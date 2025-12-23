# FillFormRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**List[FormField]**](FormField.md) | Fields to fill | 
**by** | **str** | Selector type (css, id, name, xpath) | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.fill_form_request import FillFormRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FillFormRequest from a JSON string
fill_form_request_instance = FillFormRequest.from_json(json)
# print the JSON string representation of the object
print(FillFormRequest.to_json())

# convert the object into a dict
fill_form_request_dict = fill_form_request_instance.to_dict()
# create an instance of FillFormRequest from a dict
fill_form_request_from_dict = FillFormRequest.from_dict(fill_form_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


