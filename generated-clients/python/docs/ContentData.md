# ContentData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**html** | **str** | Page HTML content | [optional] 
**title** | **str** | Page title | [optional] 
**url** | **str** | Current URL | [optional] 

## Example

```python
from airbrowser_client.models.content_data import ContentData

# TODO update the JSON string below
json = "{}"
# create an instance of ContentData from a JSON string
content_data_instance = ContentData.from_json(json)
# print the JSON string representation of the object
print(ContentData.to_json())

# convert the object into a dict
content_data_dict = content_data_instance.to_dict()
# create an instance of ContentData from a dict
content_data_from_dict = ContentData.from_dict(content_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


