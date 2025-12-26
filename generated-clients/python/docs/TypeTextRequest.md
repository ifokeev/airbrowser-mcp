# TypeTextRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | 
**text** | **str** | text | 
**timeout** | **int** | timeout | [optional] 
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.type_text_request import TypeTextRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TypeTextRequest from a JSON string
type_text_request_instance = TypeTextRequest.from_json(json)
# print the JSON string representation of the object
print(TypeTextRequest.to_json())

# convert the object into a dict
type_text_request_dict = type_text_request_instance.to_dict()
# create an instance of TypeTextRequest from a dict
type_text_request_from_dict = TypeTextRequest.from_dict(type_text_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


