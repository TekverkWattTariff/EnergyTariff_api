# PricePeriod

A consecutive time period with one price.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**valid_period** | [**DateTimeInterval**](DateTimeInterval.md) | The time period during this price is valid. | [optional] 
**price** | [**Price**](Price.md) |  | [optional] 

## Example

```python
from openapi_client.models.price_period import PricePeriod

# TODO update the JSON string below
json = "{}"
# create an instance of PricePeriod from a JSON string
price_period_instance = PricePeriod.from_json(json)
# print the JSON string representation of the object
print(PricePeriod.to_json())

# convert the object into a dict
price_period_dict = price_period_instance.to_dict()
# create an instance of PricePeriod from a dict
price_period_from_dict = PricePeriod.from_dict(price_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


