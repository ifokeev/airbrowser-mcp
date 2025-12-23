# BrowserConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profile_name** | **str** | Profile name for persistent data. Omit for fresh session. | [optional] 
**proxy** | **str** | Proxy server URL | [optional] 
**user_agent** | **str** | Custom user agent string | [optional] 
**window_size** | **List[int]** | Browser window size [width, height] | [optional] 
**disable_gpu** | **bool** | Disable GPU acceleration | [optional] [default to False]
**disable_images** | **bool** | Disable image loading | [optional] [default to False]
**disable_javascript** | **bool** | Disable JavaScript | [optional] [default to False]
**extensions** | **List[str]** | Chrome extension paths | [optional] 
**custom_args** | **List[str]** | Custom Chrome arguments | [optional] 

## Example

```python
from airbrowser_client.models.browser_config import BrowserConfig

# TODO update the JSON string below
json = "{}"
# create an instance of BrowserConfig from a JSON string
browser_config_instance = BrowserConfig.from_json(json)
# print the JSON string representation of the object
print(BrowserConfig.to_json())

# convert the object into a dict
browser_config_dict = browser_config_instance.to_dict()
# create an instance of BrowserConfig from a dict
browser_config_from_dict = BrowserConfig.from_dict(browser_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


