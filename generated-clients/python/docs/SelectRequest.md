# SelectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **str** | selector | 
**action** | **str** | action | [optional] [default to 'select']
**value** | **str** | value | [optional] 
**text** | **str** | text | [optional] 
**index** | **int** | index | [optional] 
**by** | **str** | by | [optional] [default to 'css']

## Example

```python
from airbrowser_client.models.select_request import SelectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SelectRequest from a JSON string
select_request_instance = SelectRequest.from_json(json)
# print the JSON string representation of the object
print(SelectRequest.to_json())

# convert the object into a dict
select_request_dict = select_request_instance.to_dict()
# create an instance of SelectRequest from a dict
select_request_from_dict = SelectRequest.from_dict(select_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


