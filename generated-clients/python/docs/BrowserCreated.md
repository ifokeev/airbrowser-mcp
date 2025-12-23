# BrowserCreated


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | [**BrowserCreationData**](BrowserCreationData.md) | Browser creation data | [optional] 

## Example

```python
from airbrowser_client.models.browser_created import BrowserCreated

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserCreated from a JSON string
browser_created_instance = BrowserCreated.from_json(json)
# print the JSON string representation of the object
print(BrowserCreated.to_json())

# convert the object into a dict
browser_created_dict = browser_created_instance.to_dict()
# create an instance of BrowserCreated from a dict
browser_created_from_dict = BrowserCreated.from_dict(browser_created_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


