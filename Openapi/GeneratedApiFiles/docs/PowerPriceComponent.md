# PowerPriceComponent

A time period in which pricing and power peak identification details are defined. Price components can be overlapping in time to define the full price for one time period.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | A short human readable name. | [optional] 
**description** | **str** | A longer explanatory text. | [optional] 
**type** | **str** |  | [optional] [default to 'peak']
**reference** | **str** | Reference to be used to identify this recurring price period in the cost function. | [optional] [default to 'main']
**price** | [**Price**](Price.md) |  | [optional] 
**valid_period** | [**DateInterval**](DateInterval.md) |  | [optional] 
**peak_identification_settings** | [**PeakIdentificationSettings**](PeakIdentificationSettings.md) |  | [optional] 
**recurring_periods** | [**List[RecurringPeriod]**](RecurringPeriod.md) |  | [optional] 

## Example

```python
from openapi_client.models.power_price_component import PowerPriceComponent

# TODO update the JSON string below
json = "{}"
# create an instance of PowerPriceComponent from a JSON string
power_price_component_instance = PowerPriceComponent.from_json(json)
# print the JSON string representation of the object
print(PowerPriceComponent.to_json())

# convert the object into a dict
power_price_component_dict = power_price_component_instance.to_dict()
# create an instance of PowerPriceComponent from a dict
power_price_component_from_dict = PowerPriceComponent.from_dict(power_price_component_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


