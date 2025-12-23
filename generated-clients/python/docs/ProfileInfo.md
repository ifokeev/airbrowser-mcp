# ProfileInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Profile name | [optional] 
**path** | **str** | Profile storage path | [optional] 
**size_mb** | **float** | Profile size in MB | [optional] 
**last_used** | **str** | Last used timestamp (ISO format) | [optional] 
**in_use** | **bool** | Whether profile is currently in use by a browser | [optional] 

## Example

```python
from airbrowser_client.models.profile_info import ProfileInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ProfileInfo from a JSON string
profile_info_instance = ProfileInfo.from_json(json)
# print the JSON string representation of the object
print(ProfileInfo.to_json())

# convert the object into a dict
profile_info_dict = profile_info_instance.to_dict()
# create an instance of ProfileInfo from a dict
profile_info_from_dict = ProfileInfo.from_dict(profile_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


