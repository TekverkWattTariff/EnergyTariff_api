# CalendarPatternReferences

A collection of calendar patterns that defines which days and/or dates to use for an active period.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**include** | **List[str]** | A list of calendar patterns to be included in the active period. | [optional] 
**exclude** | **List[str]** | A list of calendar patterns to be excluded from an active period. | [optional] 

## Example

```python
from openapi_client.models.calendar_pattern_references import CalendarPatternReferences

# TODO update the JSON string below
json = "{}"
# create an instance of CalendarPatternReferences from a JSON string
calendar_pattern_references_instance = CalendarPatternReferences.from_json(json)
# print the JSON string representation of the object
print(CalendarPatternReferences.to_json())

# convert the object into a dict
calendar_pattern_references_dict = calendar_pattern_references_instance.to_dict()
# create an instance of CalendarPatternReferences from a dict
calendar_pattern_references_from_dict = CalendarPatternReferences.from_dict(calendar_pattern_references_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


