# TariffsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tariffs** | [**List[Tariff]**](Tariff.md) |  | [optional] 
**calendar_patterns** | [**List[CalendarPattern]**](CalendarPattern.md) |  | [optional] 

## Example

```python
from openapi_client.models.tariffs_response import TariffsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TariffsResponse from a JSON string
tariffs_response_instance = TariffsResponse.from_json(json)
# print the JSON string representation of the object
print(TariffsResponse.to_json())

# convert the object into a dict
tariffs_response_dict = tariffs_response_instance.to_dict()
# create an instance of TariffsResponse from a dict
tariffs_response_from_dict = TariffsResponse.from_dict(tariffs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


