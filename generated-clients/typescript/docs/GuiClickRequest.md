# GuiClickRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Element selector (CSS or XPath) | [optional] [default to undefined]
**x** | **number** | Screen X coordinate (coordinate mode) | [optional] [default to undefined]
**y** | **number** | Screen Y coordinate (coordinate mode) | [optional] [default to undefined]
**timeframe** | **number** | Mouse move duration (seconds) | [optional] [default to undefined]
**fx** | **number** | Relative X (0..1) within element to click | [optional] [default to undefined]
**fy** | **number** | Relative Y (0..1) within element to click | [optional] [default to undefined]
**pre_click_validate** | **string** | Pre-click validation mode | [optional] [default to PreClickValidateEnum_Off]
**auto_snap** | **string** | Auto-snap mode for nearby targets | [optional] [default to AutoSnapEnum_Off]
**snap_radius** | **number** | Maximum snap radius in CSS pixels | [optional] [default to undefined]
**post_click_feedback** | **string** | Post-click feedback mode | [optional] [default to PostClickFeedbackEnum_None]
**post_click_timeout_ms** | **number** | Post-click observation timeout in milliseconds | [optional] [default to undefined]
**return_content** | **boolean** | Include truncated content in post-click feedback | [optional] [default to false]
**content_limit_chars** | **number** | Maximum returned content length | [optional] [default to undefined]
**include_debug** | **boolean** | Include smart-click debug diagnostics | [optional] [default to false]

## Example

```typescript
import { GuiClickRequest } from 'airbrowser-client';

const instance: GuiClickRequest = {
    selector,
    x,
    y,
    timeframe,
    fx,
    fy,
    pre_click_validate,
    auto_snap,
    snap_radius,
    post_click_feedback,
    post_click_timeout_ms,
    return_content,
    content_limit_chars,
    include_debug,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
