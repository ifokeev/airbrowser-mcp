# CreateBrowserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uc** | **bool** | uc | [optional] [default to True]
**proxy** | **str** | proxy | [optional] 
**window_size** | **List[int]** | window_size | [optional] 
**user_agent** | **str** | user_agent | [optional] 
**disable_gpu** | **bool** | disable_gpu | [optional] [default to False]
**disable_images** | **bool** | disable_images | [optional] [default to False]
**disable_javascript** | **bool** | disable_javascript | [optional] [default to False]
**extensions** | **List[str]** | extensions | [optional] 
**custom_args** | **List[str]** | custom_args | [optional] 
**profile_name** | **str** | profile_name | [optional] 

## Example

```python
from airbrowser_client.models.create_browser_request import CreateBrowserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBrowserRequest from a JSON string
create_browser_request_instance = CreateBrowserRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBrowserRequest.to_json())

# convert the object into a dict
create_browser_request_dict = create_browser_request_instance.to_dict()
# create an instance of CreateBrowserRequest from a dict
create_browser_request_from_dict = CreateBrowserRequest.from_dict(create_browser_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


