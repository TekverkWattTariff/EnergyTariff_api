# FixedPrice

Prices and information for the fixed price component of the tariff.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | A short human readable name. | [optional] 
**description** | **str** | A longer explanatory text. | [optional] 
**cost_function** | **str** | A pseudo code function that describes how to calculate the cost for a set of price components. Usage examples at https://someexamples. | [optional] 
**components** | [**List[FixedPriceComponent]**](FixedPriceComponent.md) |  | [optional] 

## Example

```python
from openapi_client.models.fixed_price import FixedPrice

# TODO update the JSON string below
json = "{}"
# create an instance of FixedPrice from a JSON string
fixed_price_instance = FixedPrice.from_json(json)
# print the JSON string representation of the object
print(FixedPrice.to_json())

# convert the object into a dict
fixed_price_dict = fixed_price_instance.to_dict()
# create an instance of FixedPrice from a dict
fixed_price_from_dict = FixedPrice.from_dict(fixed_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


