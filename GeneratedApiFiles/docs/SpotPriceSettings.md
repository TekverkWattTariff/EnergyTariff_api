# SpotPriceSettings

Settings for a spot price relative pricing component.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**multiplier** | **float** | A number used to multiply the electricity markets spot price to get a price for this price component. | [optional] 
**currency** | **str** | The currency for all related prices. | [optional] 

## Example

```python
from openapi_client.models.spot_price_settings import SpotPriceSettings

# TODO update the JSON string below
json = "{}"
# create an instance of SpotPriceSettings from a JSON string
spot_price_settings_instance = SpotPriceSettings.from_json(json)
# print the JSON string representation of the object
print(SpotPriceSettings.to_json())

# convert the object into a dict
spot_price_settings_dict = spot_price_settings_instance.to_dict()
# create an instance of SpotPriceSettings from a dict
spot_price_settings_from_dict = SpotPriceSettings.from_dict(spot_price_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


