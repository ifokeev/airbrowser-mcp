# HealthStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pool** | **object** | Pool status information | [optional] [default to undefined]
**status** | **string** | Health status | [optional] [default to undefined]
**timestamp** | **number** | Unix timestamp | [optional] [default to undefined]
**version** | **string** | Server version | [optional] [default to undefined]
**vision_enabled** | **boolean** | Whether AI vision tools are available | [optional] [default to undefined]

## Example

```typescript
import { HealthStatus } from 'airbrowser-client';

const instance: HealthStatus = {
    pool,
    status,
    timestamp,
    version,
    vision_enabled,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
