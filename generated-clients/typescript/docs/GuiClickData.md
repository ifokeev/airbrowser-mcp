# GuiClickData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **string** | Legacy inner status | [optional] [default to undefined]
**success** | **boolean** | Legacy inner success flag | [optional] [default to undefined]
**message** | **string** | Legacy inner message | [optional] [default to undefined]
**x** | **number** | Requested or resolved screen X coordinate | [optional] [default to undefined]
**y** | **number** | Requested or resolved screen Y coordinate | [optional] [default to undefined]
**outcome_status** | **string** | Machine-readable click outcome status | [optional] [default to undefined]
**reason** | **string** | Machine-readable click reason code | [optional] [default to undefined]
**reason_detail** | **string** | Human-readable reason detail | [optional] [default to undefined]
**precheck** | **object** | Pre-click validation details | [optional] [default to undefined]
**execution** | **object** | Click execution details | [optional] [default to undefined]
**postcheck** | **object** | Post-click feedback details | [optional] [default to undefined]
**recommended_next_action** | **string** | Suggested next action for callers | [optional] [default to undefined]
**debug** | **object** | Optional smart-click debug details | [optional] [default to undefined]

## Example

```typescript
import { GuiClickData } from 'airbrowser-client';

const instance: GuiClickData = {
    status,
    success,
    message,
    x,
    y,
    outcome_status,
    reason,
    reason_detail,
    precheck,
    execution,
    postcheck,
    recommended_next_action,
    debug,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
