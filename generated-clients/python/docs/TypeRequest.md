# TypeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | Element selector | 
**by** | **str** | Selector type: css, id, name, xpath | [optional] [default to 'css']
**text** | **str** | Text to type | 
**timeout** | **int** | Timeout in seconds | [optional] 

## Example

```python
from airbrowser_client.models.type_request import TypeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TypeRequest from a JSON string
type_request_instance = TypeRequest.from_json(json)
# print the JSON string representation of the object
print(TypeRequest.to_json())

# convert the object into a dict
type_request_dict = type_request_instance.to_dict()
# create an instance of TypeRequest from a dict
type_request_from_dict = TypeRequest.from_dict(type_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


