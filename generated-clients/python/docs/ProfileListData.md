# ProfileListData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profiles** | [**List[ProfileInfo]**](ProfileInfo.md) | List of profiles | [optional] 

## Example

```python
from airbrowser_client.models.profile_list_data import ProfileListData

# TODO update the JSON string below
json = "{}"
# create an instance of ProfileListData from a JSON string
profile_list_data_instance = ProfileListData.from_json(json)
# print the JSON string representation of the object
print(ProfileListData.to_json())

# convert the object into a dict
profile_list_data_dict = profile_list_data_instance.to_dict()
# create an instance of ProfileListData from a dict
profile_list_data_from_dict = ProfileListData.from_dict(profile_list_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


