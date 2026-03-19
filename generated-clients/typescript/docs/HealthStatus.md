# HealthStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **string** | Health status | [optional] [default to undefined]
**version** | **string** | Server version | [optional] [default to undefined]
**vision_enabled** | **boolean** | Whether AI vision tools are available | [optional] [default to undefined]
**pool** | **object** | Pool status information | [optional] [default to undefined]
**timestamp** | **number** | Unix timestamp | [optional] [default to undefined]

## Example

```typescript
import { HealthStatus } from 'airbrowser-client';

const instance: HealthStatus = {
    status,
    version,
    vision_enabled,
    pool,
    timestamp,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
