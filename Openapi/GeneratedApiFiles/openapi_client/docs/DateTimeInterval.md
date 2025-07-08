# DateTimeInterval

A datetime interval where fromIncluding is included and the interval is up until toExcluding.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_including** | **datetime** | From and including this timestamp. | [optional] 
**to_excluding** | **datetime** | To but excluding this timestamp. | [optional] 

## Example

```python
from openapi_client.models.date_time_interval import DateTimeInterval

# TODO update the JSON string below
json = "{}"
# create an instance of DateTimeInterval from a JSON string
date_time_interval_instance = DateTimeInterval.from_json(json)
# print the JSON string representation of the object
print(DateTimeInterval.to_json())

# convert the object into a dict
date_time_interval_dict = date_time_interval_instance.to_dict()
# create an instance of DateTimeInterval from a dict
date_time_interval_from_dict = DateTimeInterval.from_dict(date_time_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


