# FixedPriceComponent

A time period in which price details are defined. Price components can be overlapping in time to define the full price for one time period.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | A short human readable name. | [optional] 
**description** | **str** | A longer explanatory text. | [optional] 
**type** | **str** | Type describes if the price component is a publicly available price or customer specific. | [optional] [default to 'fixed']
**reference** | **str** | Reference to be used to identify this recurring price period in the cost function. | [optional] [default to 'main']
**valid_period** | [**DateInterval**](DateInterval.md) |  | [optional] 
**price** | [**Price**](Price.md) |  | [optional] 
**priced_period** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 

## Example

```python
from openapi_client.models.fixed_price_component import FixedPriceComponent

# TODO update the JSON string below
json = "{}"
# create an instance of FixedPriceComponent from a JSON string
fixed_price_component_instance = FixedPriceComponent.from_json(json)
# print the JSON string representation of the object
print(FixedPriceComponent.to_json())

# convert the object into a dict
fixed_price_component_dict = fixed_price_component_instance.to_dict()
# create an instance of FixedPriceComponent from a dict
fixed_price_component_from_dict = FixedPriceComponent.from_dict(fixed_price_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


