# PerformanceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Performance action: start_trace, stop_trace, metrics, or analyze | 
**categories** | **str** | Comma-separated trace categories (for start_trace) | [optional] 

## Example

```python
from airbrowser_client.models.performance_request import PerformanceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PerformanceRequest from a JSON string
performance_request_instance = PerformanceRequest.from_json(json)
# print the JSON string representation of the object
print(PerformanceRequest.to_json())

# convert the object into a dict
performance_request_dict = performance_request_instance.to_dict()
# create an instance of PerformanceRequest from a dict
performance_request_from_dict = PerformanceRequest.from_dict(performance_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


