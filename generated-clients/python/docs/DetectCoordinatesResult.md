# DetectCoordinatesResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | [optional]
**message** | **str** | Success message | [optional]
**data** | [**DetectCoordinatesData**](DetectCoordinatesData.md) | Detect response payload | [optional]

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
