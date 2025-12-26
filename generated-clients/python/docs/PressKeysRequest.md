# PressKeysRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | 
**keys** | **str** | keys | 
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.press_keys_request import PressKeysRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PressKeysRequest from a JSON string
press_keys_request_instance = PressKeysRequest.from_json(json)
# print the JSON string representation of the object
print(PressKeysRequest.to_json())

# convert the object into a dict
press_keys_request_dict = press_keys_request_instance.to_dict()
# create an instance of PressKeysRequest from a dict
press_keys_request_from_dict = PressKeysRequest.from_dict(press_keys_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


