# CalendarPattern

A pattern of calendar events.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**frequency** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 
**days** | **List[int]** |  | [optional] 
**dates** | **List[date]** |  | [optional] 

## Example

```python
from openapi_client.models.calendar_pattern import CalendarPattern

# TODO update the JSON string below
json = "{}"
# create an instance of CalendarPattern from a JSON string
calendar_pattern_instance = CalendarPattern.from_json(json)
# print the JSON string representation of the object
print(CalendarPattern.to_json())

# convert the object into a dict
calendar_pattern_dict = calendar_pattern_instance.to_dict()
# create an instance of CalendarPattern from a dict
calendar_pattern_from_dict = CalendarPattern.from_dict(calendar_pattern_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


