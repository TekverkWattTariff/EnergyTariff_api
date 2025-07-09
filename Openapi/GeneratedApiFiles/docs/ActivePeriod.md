# ActivePeriod

A time interval where \"fromIncluding\" is included and the interval is up to, but excluding \"toExcluding\".

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_including** | **str** | From and including this timestamp. | [optional] 
**to_excluding** | **str** | To but excluding this timestamp. | [optional] 
**calendar_pattern_references** | [**CalendarPatternReferences**](CalendarPatternReferences.md) |  | [optional] 

## Example

```python
from openapi_client.models.active_period import ActivePeriod

# TODO update the JSON string below
json = "{}"
# create an instance of ActivePeriod from a JSON string
active_period_instance = ActivePeriod.from_json(json)
# print the JSON string representation of the object
print(ActivePeriod.to_json())

# convert the object into a dict
active_period_dict = active_period_instance.to_dict()
# create an instance of ActivePeriod from a dict
active_period_from_dict = ActivePeriod.from_dict(active_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


