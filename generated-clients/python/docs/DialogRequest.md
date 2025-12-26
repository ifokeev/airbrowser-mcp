# DialogRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**text** | **str** | text | [optional] 

## Example

```python
from airbrowser_client.models.dialog_request import DialogRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DialogRequest from a JSON string
dialog_request_instance = DialogRequest.from_json(json)
# print the JSON string representation of the object
print(DialogRequest.to_json())

# convert the object into a dict
dialog_request_dict = dialog_request_instance.to_dict()
# create an instance of DialogRequest from a dict
dialog_request_from_dict = DialogRequest.from_dict(dialog_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


