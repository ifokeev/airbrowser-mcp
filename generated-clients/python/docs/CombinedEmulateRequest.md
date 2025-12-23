# CombinedEmulateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Emulation action: set, clear, or list_devices | [optional] [default to 'set']
**device** | **str** | Device preset name (e.g., iPhone 14, iPad) | [optional] 
**width** | **int** | Custom viewport width | [optional] 
**height** | **int** | Custom viewport height | [optional] 
**device_scale_factor** | **float** | Device pixel ratio | [optional] 
**mobile** | **bool** | Enable touch events | [optional] 
**user_agent** | **str** | Custom user agent | [optional] 

## Example

```python
from airbrowser_client.models.combined_emulate_request import CombinedEmulateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CombinedEmulateRequest from a JSON string
combined_emulate_request_instance = CombinedEmulateRequest.from_json(json)
# print the JSON string representation of the object
print(CombinedEmulateRequest.to_json())

# convert the object into a dict
combined_emulate_request_dict = combined_emulate_request_instance.to_dict()
# create an instance of CombinedEmulateRequest from a dict
combined_emulate_request_from_dict = CombinedEmulateRequest.from_dict(combined_emulate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


