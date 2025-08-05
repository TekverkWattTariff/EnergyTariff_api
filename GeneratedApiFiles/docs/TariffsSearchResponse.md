# TariffsSearchResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tariffs** | [**List[Tariff]**](Tariff.md) |  | [optional] 
**mappings** | [**List[TariffMapping]**](TariffMapping.md) |  | [optional] 

## Example

```python
from openapi_client.models.tariffs_search_response import TariffsSearchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TariffsSearchResponse from a JSON string
tariffs_search_response_instance = TariffsSearchResponse.from_json(json)
# print the JSON string representation of the object
print(TariffsSearchResponse.to_json())

# convert the object into a dict
tariffs_search_response_dict = tariffs_search_response_instance.to_dict()
# create an instance of TariffsSearchResponse from a dict
tariffs_search_response_from_dict = TariffsSearchResponse.from_dict(tariffs_search_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


