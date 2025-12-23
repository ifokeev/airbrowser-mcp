# AttributeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | [optional] 
**message** | **str** | Status message | [optional] 
**timestamp** | **float** | Unix timestamp | [optional] 
**data** | **object** | Attribute/property data | [optional] 

## Example

```python
from airbrowser_client.models.attribute_response import AttributeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeResponse from a JSON string
attribute_response_instance = AttributeResponse.from_json(json)
# print the JSON string representation of the object
print(AttributeResponse.to_json())

# convert the object into a dict
attribute_response_dict = attribute_response_instance.to_dict()
# create an instance of AttributeResponse from a dict
attribute_response_from_dict = AttributeResponse.from_dict(attribute_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


