# DetectCoordinatesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | Natural language description of element to find |
**fx** | **float** | Relative X (0..1) within the detected element | [optional]
**fy** | **float** | Relative Y (0..1) within the detected element | [optional]
**model** | **str** | Optional vision model override for this request | [optional]
**hit_test** | **str** | Detect-time validation mode | [optional] [default to 'off']
**auto_snap** | **str** | Auto-snap mode for nearby targets | [optional] [default to 'off']
**snap_radius** | **float** | Maximum snap radius in CSS pixels | [optional]
**include_debug** | **bool** | Include smart-targeting debug details | [optional] [default to False]

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
