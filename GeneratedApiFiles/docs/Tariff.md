# Tariff

Information about the tariff that are static and does not change during at least a month.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Globally unique identifier | [optional] 
**name** | **str** | Descriptive short name of the grid tariff. | [optional] 
**description** | **str** | Detailed description of the grid tariff. | [optional] 
**product** | **str** | Name of the grid company product, for grid company internal use. | [optional] 
**company_name** | **str** | Name of the grid company. | [optional] 
**company_org_no** | **str** | Organization number of the grid company. | [optional] 
**direction** | **str** | Indicates if this is a tariff for consumption or production. Valid values are \&quot;consumption\&quot; and \&quot;production\&quot;. | [optional] [default to 'consumption']
**time_zone** | **str** | Time zone for all time values in this tariff. From the IANA Time Zone Database (e.g., &#39;Europe/Stockholm&#39;). | [optional] 
**last_updated** | **datetime** | The time of when the prices were last updated on the server side. No need to get prices if you already fetched the latest ones? Ex. 2021-11-05T00:00:00+01:00 | [optional] 
**valid_period** | [**DateInterval**](DateInterval.md) |  | [optional] 
**billing_period** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 
**fixed_price** | [**FixedPrice**](FixedPrice.md) |  | [optional] 
**energy_price** | [**EnergyPrice**](EnergyPrice.md) |  | [optional] 
**power_price** | [**PowerPrice**](PowerPrice.md) |  | [optional] 

## Example

```python
from openapi_client.models.tariff import Tariff

# TODO update the JSON string below
json = "{}"
# create an instance of Tariff from a JSON string
tariff_instance = Tariff.from_json(json)
# print the JSON string representation of the object
print(Tariff.to_json())

# convert the object into a dict
tariff_dict = tariff_instance.to_dict()
# create an instance of Tariff from a dict
tariff_from_dict = Tariff.from_dict(tariff_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


