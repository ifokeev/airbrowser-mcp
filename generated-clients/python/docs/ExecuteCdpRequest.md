# ExecuteCdpRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | method | 
**params** | **object** | params | [optional] 

## Example

```python
from airbrowser_client.models.execute_cdp_request import ExecuteCdpRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteCdpRequest from a JSON string
execute_cdp_request_instance = ExecuteCdpRequest.from_json(json)
# print the JSON string representation of the object
print(ExecuteCdpRequest.to_json())

# convert the object into a dict
execute_cdp_request_dict = execute_cdp_request_instance.to_dict()
# create an instance of ExecuteCdpRequest from a dict
execute_cdp_request_from_dict = ExecuteCdpRequest.from_dict(execute_cdp_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


