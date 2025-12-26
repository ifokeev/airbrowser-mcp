# WaitElementRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | 
**until** | **str** | until | 
**timeout** | **int** | timeout | [optional] 
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.wait_element_request import WaitElementRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WaitElementRequest from a JSON string
wait_element_request_instance = WaitElementRequest.from_json(json)
# print the JSON string representation of the object
print(WaitElementRequest.to_json())

# convert the object into a dict
wait_element_request_dict = wait_element_request_instance.to_dict()
# create an instance of WaitElementRequest from a dict
wait_element_request_from_dict = WaitElementRequest.from_dict(wait_element_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


