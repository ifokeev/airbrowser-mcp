# ActionResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | **object** | Action result data | [optional] 

## Example

```python
from airbrowser_client.models.action_result import ActionResult

# TODO update the JSON string below
json = "{}"
# create an instance of ActionResult from a JSON string
action_result_instance = ActionResult.from_json(json)
# print the JSON string representation of the object
print(ActionResult.to_json())

# convert the object into a dict
action_result_dict = action_result_instance.to_dict()
# create an instance of ActionResult from a dict
action_result_from_dict = ActionResult.from_dict(action_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


