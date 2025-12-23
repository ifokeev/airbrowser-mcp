# DetectCoordinatesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | Natural language description of element to find | 

## Example

```python
from airbrowser_client.models.detect_coordinates_request import DetectCoordinatesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of DetectCoordinatesRequest from a JSON string
detect_coordinates_request_instance = DetectCoordinatesRequest.from_json(json)
# print the JSON string representation of the object
print(DetectCoordinatesRequest.to_json())

# convert the object into a dict
detect_coordinates_request_dict = detect_coordinates_request_instance.to_dict()
# create an instance of DetectCoordinatesRequest from a dict
detect_coordinates_request_from_dict = DetectCoordinatesRequest.from_dict(detect_coordinates_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


