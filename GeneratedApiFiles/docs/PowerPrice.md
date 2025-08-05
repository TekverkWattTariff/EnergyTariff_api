# PowerPrice

Prices with parameters that defines power peak identification and price calculation for the power component of the tariff.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | A short human readable name. | [optional] 
**description** | **str** | A longer explanatory text. | [optional] 
**cost_function** | **str** | A pseudo code function that describes how to calculate the cost for a set of price components. Usage examples at https://someexamples. | [optional] 
**unit** | **str** | The unit of a measurement or price calculation. | [optional] 
**components** | [**List[PowerPriceComponent]**](PowerPriceComponent.md) |  | [optional] 

## Example

```python
from openapi_client.models.power_price import PowerPrice

# TODO update the JSON string below
json = "{}"
# create an instance of PowerPrice from a JSON string
power_price_instance = PowerPrice.from_json(json)
# print the JSON string representation of the object
print(PowerPrice.to_json())

# convert the object into a dict
power_price_dict = power_price_instance.to_dict()
# create an instance of PowerPrice from a dict
power_price_from_dict = PowerPrice.from_dict(power_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


