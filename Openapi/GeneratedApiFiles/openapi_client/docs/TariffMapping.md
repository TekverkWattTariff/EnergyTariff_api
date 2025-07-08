# TariffMapping


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tariff_id** | **str** | Globally unique identifier | [optional] 
**metering_point_ids** | **List[str]** |  | [optional] 

## Example

```python
from openapi_client.models.tariff_mapping import TariffMapping

# TODO update the JSON string below
json = "{}"
# create an instance of TariffMapping from a JSON string
tariff_mapping_instance = TariffMapping.from_json(json)
# print the JSON string representation of the object
print(TariffMapping.to_json())

# convert the object into a dict
tariff_mapping_dict = tariff_mapping_instance.to_dict()
# create an instance of TariffMapping from a dict
tariff_mapping_from_dict = TariffMapping.from_dict(tariff_mapping_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


