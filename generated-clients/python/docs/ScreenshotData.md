# ScreenshotData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**screenshot_url** | **str** | URL to screenshot | [optional] 
**screenshot_path** | **str** | Path to screenshot file | [optional] 

## Example

```python
from airbrowser_client.models.screenshot_data import ScreenshotData

# TODO update the JSON string below
json = "{}"
# create an instance of ScreenshotData from a JSON string
screenshot_data_instance = ScreenshotData.from_json(json)
# print the JSON string representation of the object
print(ScreenshotData.to_json())

# convert the object into a dict
screenshot_data_dict = screenshot_data_instance.to_dict()
# create an instance of ScreenshotData from a dict
screenshot_data_from_dict = ScreenshotData.from_dict(screenshot_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


