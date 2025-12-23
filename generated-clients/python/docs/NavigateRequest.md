# NavigateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | URL to navigate to | 
**timeout** | **int** | Navigation timeout in seconds | [optional] 

## Example

```python
from airbrowser_client.models.navigate_request import NavigateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of NavigateRequest from a JSON string
navigate_request_instance = NavigateRequest.from_json(json)
# print the JSON string representation of the object
print(NavigateRequest.to_json())

# convert the object into a dict
navigate_request_dict = navigate_request_instance.to_dict()
# create an instance of NavigateRequest from a dict
navigate_request_from_dict = NavigateRequest.from_dict(navigate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


