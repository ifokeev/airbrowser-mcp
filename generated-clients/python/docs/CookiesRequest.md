# CookiesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | action | 
**cookie** | **object** | cookie | [optional] 
**name** | **str** | name | [optional] 
**domain** | **str** | domain | [optional] 

## Example

```python
from airbrowser_client.models.cookies_request import CookiesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CookiesRequest from a JSON string
cookies_request_instance = CookiesRequest.from_json(json)
# print the JSON string representation of the object
print(CookiesRequest.to_json())

# convert the object into a dict
cookies_request_dict = cookies_request_instance.to_dict()
# create an instance of CookiesRequest from a dict
cookies_request_from_dict = CookiesRequest.from_dict(cookies_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


