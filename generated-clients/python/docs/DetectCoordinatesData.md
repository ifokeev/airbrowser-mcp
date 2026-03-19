# DetectCoordinatesData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | Element description used | [optional]
**bounding_box** | **object** | Element bounding box {x, y, width, height} | [optional]
**click_point** | **object** | Recommended click point {x, y} | [optional]
**confidence** | **float** | Detection confidence (0.0-1.0) | [optional]
**outcome_status** | **str** | Machine-readable detect outcome status | [optional]
**reason** | **str** | Machine-readable detect reason code | [optional]
**reason_detail** | **str** | Human-readable reason detail | [optional]
**resolved_target** | **object** | Resolved target details after validation or snapping | [optional]
**resolved_click_point** | **object** | Validated or snapped click point {x, y} | [optional]
**snap_result** | **object** | Details about any snap candidate that was applied | [optional]
**recommended_next_action** | **str** | Suggested next action for callers | [optional]
**screenshot_url** | **str** | URL to the screenshot | [optional]
**image_size** | **object** | Original screenshot dimensions | [optional]
**transform_info** | **object** | Coordinate transform metadata | [optional]
**debug** | **object** | Optional smart-targeting debug details | [optional]

## Example

```python
from airbrowser_client.models.detect_coordinates_data import DetectCoordinatesData

# TODO update the JSON string below
json = "{}"
# create an instance of DetectCoordinatesData from a JSON string
detect_coordinates_data_instance = DetectCoordinatesData.from_json(json)
# print the JSON string representation of the object
print(DetectCoordinatesData.to_json())

# convert the object into a dict
detect_coordinates_data_dict = detect_coordinates_data_instance.to_dict()
# create an instance of DetectCoordinatesData from a dict
detect_coordinates_data_from_dict = DetectCoordinatesData.from_dict(detect_coordinates_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
