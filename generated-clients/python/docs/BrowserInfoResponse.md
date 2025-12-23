# BrowserInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | **object** | Browser information | [optional] 

## Example

```python
from airbrowser_client.models.browser_info_response import BrowserInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserInfoResponse from a JSON string
browser_info_response_instance = BrowserInfoResponse.from_json(json)
# print the JSON string representation of the object
print(BrowserInfoResponse.to_json())

# convert the object into a dict
browser_info_response_dict = browser_info_response_instance.to_dict()
# create an instance of BrowserInfoResponse from a dict
browser_info_response_from_dict = BrowserInfoResponse.from_dict(browser_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


