# SelectRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selector** | **string** | Select element selector | [default to undefined]
**by** | **string** | Selector type (css, id, name, xpath) | [optional] [default to 'css']
**action** | **string** | Action: select or options | [optional] [default to ActionEnum_Select]
**value** | **string** | Option value to select | [optional] [default to undefined]
**text** | **string** | Option text to select | [optional] [default to undefined]
**index** | **number** | Option index to select | [optional] [default to undefined]

## Example

```typescript
import { SelectRequest } from 'airbrowser-client';

const instance: SelectRequest = {
    selector,
    by,
    action,
    value,
    text,
    index,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
