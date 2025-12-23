# DetectCoordinatesResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **boolean** | Operation success | [optional] [default to undefined]
**message** | **string** | Success message | [optional] [default to undefined]
**timestamp** | **number** | Unix timestamp | [optional] [default to undefined]
**prompt** | **string** | Element description used | [optional] [default to undefined]
**coordinates** | **object** | Full coordinate information | [optional] [default to undefined]
**bounding_box** | **object** | Element bounding box {x, y, width, height} | [optional] [default to undefined]
**click_point** | **object** | Recommended click point {x, y} | [optional] [default to undefined]
**screenshot_path** | **string** | Path to screenshot analyzed | [optional] [default to undefined]
**model_used** | **string** | Vision model used for detection | [optional] [default to undefined]
**confidence** | **number** | Detection confidence (0.0-1.0) | [optional] [default to undefined]
**models_tried** | **Array&lt;string&gt;** | Models attempted if detection failed | [optional] [default to undefined]
**data** | **object** | Additional result data | [optional] [default to undefined]
**error** | **string** | Error message if failed | [optional] [default to undefined]

## Example

```typescript
import { DetectCoordinatesResult } from 'airbrowser-client';

const instance: DetectCoordinatesResult = {
    success,
    message,
    timestamp,
    prompt,
    coordinates,
    bounding_box,
    click_point,
    screenshot_path,
    model_used,
    confidence,
    models_tried,
    data,
    error,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
