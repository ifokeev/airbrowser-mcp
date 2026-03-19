# DetectCoordinatesData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **string** | Element description used | [optional] [default to undefined]
**bounding_box** | **object** | Element bounding box {x, y, width, height} | [optional] [default to undefined]
**click_point** | **object** | Recommended click point {x, y} | [optional] [default to undefined]
**confidence** | **number** | Detection confidence (0.0-1.0) | [optional] [default to undefined]
**outcome_status** | **string** | Machine-readable detect outcome status | [optional] [default to undefined]
**reason** | **string** | Machine-readable detect reason code | [optional] [default to undefined]
**reason_detail** | **string** | Human-readable reason detail | [optional] [default to undefined]
**resolved_target** | **object** | Resolved target details after validation or snapping | [optional] [default to undefined]
**resolved_click_point** | **object** | Validated or snapped click point {x, y} | [optional] [default to undefined]
**snap_result** | **object** | Details about any snap candidate that was applied | [optional] [default to undefined]
**recommended_next_action** | **string** | Suggested next action for callers | [optional] [default to undefined]
**screenshot_url** | **string** | URL to the screenshot | [optional] [default to undefined]
**image_size** | **object** | Original screenshot dimensions | [optional] [default to undefined]
**transform_info** | **object** | Coordinate transform metadata | [optional] [default to undefined]
**debug** | **object** | Optional smart-targeting debug details | [optional] [default to undefined]

## Example

```typescript
import { DetectCoordinatesData } from 'airbrowser-client';

const instance: DetectCoordinatesData = {
    prompt,
    bounding_box,
    click_point,
    confidence,
    outcome_status,
    reason,
    reason_detail,
    resolved_target,
    resolved_click_point,
    snap_result,
    recommended_next_action,
    screenshot_url,
    image_size,
    transform_info,
    debug,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
