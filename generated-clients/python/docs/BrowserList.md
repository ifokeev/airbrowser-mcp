# BrowserList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | [**BrowserListData**](BrowserListData.md) | Browser list data | [optional] 

## Example

```python
from airbrowser_client.models.browser_list import BrowserList

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserList from a JSON string
browser_list_instance = BrowserList.from_json(json)
# print the JSON string representation of the object
print(BrowserList.to_json())

# convert the object into a dict
browser_list_dict = browser_list_instance.to_dict()
# create an instance of BrowserList from a dict
browser_list_from_dict = BrowserList.from_dict(browser_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


