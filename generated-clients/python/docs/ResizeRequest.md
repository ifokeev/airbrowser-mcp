# ResizeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**width** | **int** | Viewport width | 
**height** | **int** | Viewport height | 

## Example

```python
from airbrowser_client.models.resize_request import ResizeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ResizeRequest from a JSON string
resize_request_instance = ResizeRequest.from_json(json)
# print the JSON string representation of the object
print(ResizeRequest.to_json())

# convert the object into a dict
resize_request_dict = resize_request_instance.to_dict()
# create an instance of ResizeRequest from a dict
resize_request_from_dict = ResizeRequest.from_dict(resize_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


