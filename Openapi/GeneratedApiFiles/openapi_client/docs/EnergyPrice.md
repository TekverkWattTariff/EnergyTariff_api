# EnergyPrice

Prices and information for the energy price component of the tariff.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | A short human readable name. | [optional] 
**description** | **str** | A longer explanatory text. | [optional] 
**cost_function** | **str** | A pseudo code function that describes how to calculate the cost for a set of price components. Usage examples at https://someexamples. | [optional] 
**unit** | **str** | The unit of a measurement or price calculation. | [optional] 
**components** | [**List[EnergyPriceComponent]**](EnergyPriceComponent.md) |  | [optional] 

## Example

```python
from openapi_client.models.energy_price import EnergyPrice

# TODO update the JSON string below
json = "{}"
# create an instance of EnergyPrice from a JSON string
energy_price_instance = EnergyPrice.from_json(json)
# print the JSON string representation of the object
print(EnergyPrice.to_json())

# convert the object into a dict
energy_price_dict = energy_price_instance.to_dict()
# create an instance of EnergyPrice from a dict
energy_price_from_dict = EnergyPrice.from_dict(energy_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


