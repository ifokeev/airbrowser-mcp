# UrlData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Current URL | [optional] 

## Example

```python
from airbrowser_client.models.url_data import UrlData

# TODO update the JSON string below
json = "{}"
# create an instance of UrlData from a JSON string
url_data_instance = UrlData.from_json(json)
# print the JSON string representation of the object
print(UrlData.to_json())

# convert the object into a dict
url_data_dict = url_data_instance.to_dict()
# create an instance of UrlData from a dict
url_data_from_dict = UrlData.from_dict(url_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


