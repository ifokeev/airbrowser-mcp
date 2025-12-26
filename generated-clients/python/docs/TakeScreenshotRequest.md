# TakeScreenshotRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_page** | **bool** | full_page | [optional] [default to False]

## Example

```python
from airbrowser_client.models.take_screenshot_request import TakeScreenshotRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TakeScreenshotRequest from a JSON string
take_screenshot_request_instance = TakeScreenshotRequest.from_json(json)
# print the JSON string representation of the object
print(TakeScreenshotRequest.to_json())

# convert the object into a dict
take_screenshot_request_dict = take_screenshot_request_instance.to_dict()
# create an instance of TakeScreenshotRequest from a dict
take_screenshot_request_from_dict = TakeScreenshotRequest.from_dict(take_screenshot_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


