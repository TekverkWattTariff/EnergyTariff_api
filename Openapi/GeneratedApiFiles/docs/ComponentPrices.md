# ComponentPrices

Time differentiated prices for a price component.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**component_id** | **str** | Globally unique identifier | [optional] 
**prices** | [**List[PricePeriod]**](PricePeriod.md) |  | [optional] 

## Example

```python
from openapi_client.models.component_prices import ComponentPrices

# TODO update the JSON string below
json = "{}"
# create an instance of ComponentPrices from a JSON string
component_prices_instance = ComponentPrices.from_json(json)
# print the JSON string representation of the object
print(ComponentPrices.to_json())

# convert the object into a dict
component_prices_dict = component_prices_instance.to_dict()
# create an instance of ComponentPrices from a dict
component_prices_from_dict = ComponentPrices.from_dict(component_prices_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


