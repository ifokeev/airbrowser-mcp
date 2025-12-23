# UrlResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** | Operation success | 
**message** | **str** | Status message | 
**timestamp** | **float** | Unix timestamp | 
**data** | [**UrlData**](UrlData.md) | URL data | [optional] 

## Example

```python
from airbrowser_client.models.url_response import UrlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UrlResponse from a JSON string
url_response_instance = UrlResponse.from_json(json)
# print the JSON string representation of the object
print(UrlResponse.to_json())

# convert the object into a dict
url_response_dict = url_response_instance.to_dict()
# create an instance of UrlResponse from a dict
url_response_from_dict = UrlResponse.from_dict(url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


