# EmulateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | [optional] [default to 'set']
**device** | **str** | device | [optional] 
**width** | **int** | width | [optional] 
**height** | **int** | height | [optional] 
**device_scale_factor** | **float** | device_scale_factor | [optional] 
**mobile** | **bool** | mobile | [optional] 
**user_agent** | **str** | user_agent | [optional] 

## Example

```python
from airbrowser_client.models.emulate_request import EmulateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EmulateRequest from a JSON string
emulate_request_instance = EmulateRequest.from_json(json)
# print the JSON string representation of the object
print(EmulateRequest.to_json())

# convert the object into a dict
emulate_request_dict = emulate_request_instance.to_dict()
# create an instance of EmulateRequest from a dict
emulate_request_from_dict = EmulateRequest.from_dict(emulate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


