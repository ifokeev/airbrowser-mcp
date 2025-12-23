# BrowserCreationData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**browser_id** | **str** | Unique browser identifier | 
**config** | **object** | Browser configuration used | [optional] 

## Example

```python
from airbrowser_client.models.browser_creation_data import BrowserCreationData

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserCreationData from a JSON string
browser_creation_data_instance = BrowserCreationData.from_json(json)
# print the JSON string representation of the object
print(BrowserCreationData.to_json())

# convert the object into a dict
browser_creation_data_dict = browser_creation_data_instance.to_dict()
# create an instance of BrowserCreationData from a dict
browser_creation_data_from_dict = BrowserCreationData.from_dict(browser_creation_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


