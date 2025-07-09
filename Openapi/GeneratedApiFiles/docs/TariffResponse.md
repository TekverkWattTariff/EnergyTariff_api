# TariffResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tariff** | [**Tariff**](Tariff.md) |  | [optional] 

## Example

```python
from openapi_client.models.tariff_response import TariffResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TariffResponse from a JSON string
tariff_response_instance = TariffResponse.from_json(json)
# print the JSON string representation of the object
print(TariffResponse.to_json())

# convert the object into a dict
tariff_response_dict = tariff_response_instance.to_dict()
# create an instance of TariffResponse from a dict
tariff_response_from_dict = TariffResponse.from_dict(tariff_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


