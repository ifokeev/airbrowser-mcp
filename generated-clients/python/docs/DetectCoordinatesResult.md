# DetectCoordinatesResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | [optional] 
**message** | **str** | Success message | [optional] 
**timestamp** | **float** | Unix timestamp | [optional] 
**prompt** | **str** | Element description used | [optional] 
**coordinates** | **object** | Full coordinate information | [optional] 
**bounding_box** | **object** | Element bounding box {x, y, width, height} | [optional] 
**click_point** | **object** | Recommended click point {x, y} | [optional] 
**screenshot_path** | **str** | Path to screenshot analyzed | [optional] 
**model_used** | **str** | Vision model used for detection | [optional] 
**confidence** | **float** | Detection confidence (0.0-1.0) | [optional] 
**models_tried** | **List[str]** | Models attempted if detection failed | [optional] 
**data** | **object** | Additional result data | [optional] 
**error** | **str** | Error message if failed | [optional] 

## Example

```python
from airbrowser_client.models.detect_coordinates_result import DetectCoordinatesResult

# TODO update the JSON string below
json = "{}"
# create an instance of DetectCoordinatesResult from a JSON string
detect_coordinates_result_instance = DetectCoordinatesResult.from_json(json)
# print the JSON string representation of the object
print(DetectCoordinatesResult.to_json())

# convert the object into a dict
detect_coordinates_result_dict = detect_coordinates_result_instance.to_dict()
# create an instance of DetectCoordinatesResult from a dict
detect_coordinates_result_from_dict = DetectCoordinatesResult.from_dict(detect_coordinates_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


