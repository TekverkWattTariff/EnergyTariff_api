# openapi_client.PriceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_prices**](PriceApi.md#get_prices) | **GET** /{v}/prices/{componentId} | Returns prices for a price component for a given timeperiod.


# **get_prices**
> PricesResponse get_prices(v, component_id, duration)

Returns prices for a price component for a given timeperiod.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import openapi_client
from openapi_client.models.prices_response import PricesResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): BearerAuth
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.PriceApi(api_client)
    v = 'v0' # str | Version of the API (default to 'v0')
    component_id = 'component_id_example' # str | A price component id.
    duration = 'duration_example' # str | A duration in time that starts at 00:00 (midnight) of the day when the request is made.

    try:
        # Returns prices for a price component for a given timeperiod.
        api_response = api_instance.get_prices(v, component_id, duration)
        print("The response of PriceApi->get_prices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PriceApi->get_prices: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **v** | **str**| Version of the API | [default to &#39;v0&#39;]
 **component_id** | **str**| A price component id. | 
 **duration** | **str**| A duration in time that starts at 00:00 (midnight) of the day when the request is made. | 

### Return type

[**PricesResponse**](PricesResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The prices for the provided component id and time period. |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

