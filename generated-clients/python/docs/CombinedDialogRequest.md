# CombinedDialogRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Dialog action: get, accept, or dismiss | 
**text** | **str** | Text to enter for prompt dialogs (for &#39;accept&#39; action) | [optional] 

## Example

```python
from airbrowser_client.models.combined_dialog_request import CombinedDialogRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CombinedDialogRequest from a JSON string
combined_dialog_request_instance = CombinedDialogRequest.from_json(json)
# print the JSON string representation of the object
print(CombinedDialogRequest.to_json())

# convert the object into a dict
combined_dialog_request_dict = combined_dialog_request_instance.to_dict()
# create an instance of CombinedDialogRequest from a dict
combined_dialog_request_from_dict = CombinedDialogRequest.from_dict(combined_dialog_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


