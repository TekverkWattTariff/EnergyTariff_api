# DateInterval

A date interval to define a validity period for an object.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_including** | **date** | From and including this date. | [optional] 
**to_excluding** | **date** | To but excluding this date. | [optional] 

## Example

```python
from openapi_client.models.date_interval import DateInterval

# TODO update the JSON string below
json = "{}"
# create an instance of DateInterval from a JSON string
date_interval_instance = DateInterval.from_json(json)
# print the JSON string representation of the object
print(DateInterval.to_json())

# convert the object into a dict
date_interval_dict = date_interval_instance.to_dict()
# create an instance of DateInterval from a dict
date_interval_from_dict = DateInterval.from_dict(date_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


