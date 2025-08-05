# RecurringPeriod

A short period of time that recurs several times during a season or other long time period.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reference** | **str** | Reference to be used to identify this recurring period in a function. | [optional] [default to 'main']
**frequency** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 
**active_periods** | [**List[ActivePeriod]**](ActivePeriod.md) |  | [optional] 

## Example

```python
from openapi_client.models.recurring_period import RecurringPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of RecurringPeriod from a JSON string
recurring_period_instance = RecurringPeriod.from_json(json)
# print the JSON string representation of the object
print(RecurringPeriod.to_json())

# convert the object into a dict
recurring_period_dict = recurring_period_instance.to_dict()
# create an instance of RecurringPeriod from a dict
recurring_period_from_dict = RecurringPeriod.from_dict(recurring_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


