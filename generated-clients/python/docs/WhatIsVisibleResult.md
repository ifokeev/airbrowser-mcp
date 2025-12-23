# WhatIsVisibleResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | [optional] 
**message** | **str** | Success message | [optional] 
**timestamp** | **float** | Unix timestamp | [optional] 
**analysis** | **str** | Comprehensive page state analysis | [optional] 
**model** | **str** | AI model used for analysis | [optional] 
**screenshot_url** | **str** | URL to the screenshot | [optional] 
**screenshot_path** | **str** | Path to the screenshot file | [optional] 
**error** | **str** | Error message if failed | [optional] 

## Example

```python
from airbrowser_client.models.what_is_visible_result import WhatIsVisibleResult

# TODO update the JSON string below
json = "{}"
# create an instance of WhatIsVisibleResult from a JSON string
what_is_visible_result_instance = WhatIsVisibleResult.from_json(json)
# print the JSON string representation of the object
print(WhatIsVisibleResult.to_json())

# convert the object into a dict
what_is_visible_result_dict = what_is_visible_result_instance.to_dict()
# create an instance of WhatIsVisibleResult from a dict
what_is_visible_result_from_dict = WhatIsVisibleResult.from_dict(what_is_visible_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


