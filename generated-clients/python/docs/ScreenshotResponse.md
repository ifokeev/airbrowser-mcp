# ScreenshotResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | [**ScreenshotData**](ScreenshotData.md) | Screenshot data | [optional] 

## Example

```python
from airbrowser_client.models.screenshot_response import ScreenshotResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ScreenshotResponse from a JSON string
screenshot_response_instance = ScreenshotResponse.from_json(json)
# print the JSON string representation of the object
print(ScreenshotResponse.to_json())

# convert the object into a dict
screenshot_response_dict = screenshot_response_instance.to_dict()
# create an instance of ScreenshotResponse from a dict
screenshot_response_from_dict = ScreenshotResponse.from_dict(screenshot_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


