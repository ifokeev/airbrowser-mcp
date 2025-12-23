# UploadFileRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | File input selector | 
**file_path** | **str** | Path to file to upload | 
**by** | **str** | Selector type (css, id, name, xpath) | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.upload_file_request import UploadFileRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UploadFileRequest from a JSON string
upload_file_request_instance = UploadFileRequest.from_json(json)
# print the JSON string representation of the object
print(UploadFileRequest.to_json())

# convert the object into a dict
upload_file_request_dict = upload_file_request_instance.to_dict()
# create an instance of UploadFileRequest from a dict
upload_file_request_from_dict = UploadFileRequest.from_dict(upload_file_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


