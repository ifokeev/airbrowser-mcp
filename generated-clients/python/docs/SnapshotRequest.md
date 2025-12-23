# SnapshotRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Snapshot type: dom or accessibility | [optional] [default to 'dom']

## Example

```python
from airbrowser_client.models.snapshot_request import SnapshotRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SnapshotRequest from a JSON string
snapshot_request_instance = SnapshotRequest.from_json(json)
# print the JSON string representation of the object
print(SnapshotRequest.to_json())

# convert the object into a dict
snapshot_request_dict = snapshot_request_instance.to_dict()
# create an instance of SnapshotRequest from a dict
snapshot_request_from_dict = SnapshotRequest.from_dict(snapshot_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


