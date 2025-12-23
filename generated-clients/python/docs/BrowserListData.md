# BrowserListData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**browsers** | **List[object]** | List of active browsers | [optional] 
**count** | **int** | Total browser count | [optional] 

## Example

```python
from airbrowser_client.models.browser_list_data import BrowserListData

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserListData from a JSON string
browser_list_data_instance = BrowserListData.from_json(json)
# print the JSON string representation of the object
print(BrowserListData.to_json())

# convert the object into a dict
browser_list_data_dict = browser_list_data_instance.to_dict()
# create an instance of BrowserListData from a dict
browser_list_data_from_dict = BrowserListData.from_dict(browser_list_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


