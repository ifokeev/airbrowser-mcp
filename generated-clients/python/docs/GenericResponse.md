# GenericResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **object** | Response data | [optional] 
**message** | **str** | Response message | [optional] 
**success** | **bool** | Whether the operation succeeded | [optional] 

## Example

```python
from airbrowser_client.models.generic_response import GenericResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenericResponse from a JSON string
generic_response_instance = GenericResponse.from_json(json)
# print the JSON string representation of the object
print(GenericResponse.to_json())

# convert the object into a dict
generic_response_dict = generic_response_instance.to_dict()
# create an instance of GenericResponse from a dict
generic_response_from_dict = GenericResponse.from_dict(generic_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


