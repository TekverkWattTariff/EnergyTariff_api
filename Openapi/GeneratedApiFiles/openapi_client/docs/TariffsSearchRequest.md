# TariffsSearchRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metering_point_ids** | **List[str]** | List of MPIDs you are the registered owner of as a private person or your company has e legal reason to request in a customer/provider relationship. | [optional] 

## Example

```python
from openapi_client.models.tariffs_search_request import TariffsSearchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TariffsSearchRequest from a JSON string
tariffs_search_request_instance = TariffsSearchRequest.from_json(json)
# print the JSON string representation of the object
print(TariffsSearchRequest.to_json())

# convert the object into a dict
tariffs_search_request_dict = tariffs_search_request_instance.to_dict()
# create an instance of TariffsSearchRequest from a dict
tariffs_search_request_from_dict = TariffsSearchRequest.from_dict(tariffs_search_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


