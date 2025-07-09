# openapi_client.TariffApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_tariff_by_id**](TariffApi.md#get_tariff_by_id) | **GET** /{v}/tariffs/{id} | Returns the tariff for the provided id.
[**get_tariffs**](TariffApi.md#get_tariffs) | **GET** /{v}/tariffs | Returns a collection of publicly available tariffs for the DSO without any customer data.
[**search_tariffs**](TariffApi.md#search_tariffs) | **POST** /{v}/tariffs/search | Returns a collection of tariffs based on the search criteria and a mapping between the tariffs and search parameters.


# **get_tariff_by_id**
> TariffResponse get_tariff_by_id(v, id)

Returns the tariff for the provided id.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import openapi_client
from openapi_client.models.tariff_response import TariffResponse
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
    api_instance = openapi_client.TariffApi(api_client)
    v = 'v0' # str | Version of the API (default to 'v0')
    id = 'id_example' # str | Unique identifier for an object

    try:
        # Returns the tariff for the provided id.
        api_response = api_instance.get_tariff_by_id(v, id)
        print("The response of TariffApi->get_tariff_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TariffApi->get_tariff_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **v** | **str**| Version of the API | [default to &#39;v0&#39;]
 **id** | **str**| Unique identifier for an object | 

### Return type

[**TariffResponse**](TariffResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Response with one tariff. |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tariffs**
> TariffsResponse get_tariffs(v)

Returns a collection of publicly available tariffs for the DSO without any customer data.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import openapi_client
from openapi_client.models.tariffs_response import TariffsResponse
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
    api_instance = openapi_client.TariffApi(api_client)
    v = 'v0' # str | Version of the API (default to 'v0')

    try:
        # Returns a collection of publicly available tariffs for the DSO without any customer data.
        api_response = api_instance.get_tariffs(v)
        print("The response of TariffApi->get_tariffs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TariffApi->get_tariffs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **v** | **str**| Version of the API | [default to &#39;v0&#39;]

### Return type

[**TariffsResponse**](TariffsResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All publicly available tariffs without any customer data. |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_tariffs**
> TariffsSearchResponse search_tariffs(v, tariffs_search_request)

Returns a collection of tariffs based on the search criteria and a mapping between the tariffs and search parameters.

### Example

* Bearer (JWT) Authentication (BearerAuth):

```python
import openapi_client
from openapi_client.models.tariffs_search_request import TariffsSearchRequest
from openapi_client.models.tariffs_search_response import TariffsSearchResponse
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
    api_instance = openapi_client.TariffApi(api_client)
    v = 'v0' # str | Version of the API (default to 'v0')
    tariffs_search_request = openapi_client.TariffsSearchRequest() # TariffsSearchRequest | Tariffs search parameters.

    try:
        # Returns a collection of tariffs based on the search criteria and a mapping between the tariffs and search parameters.
        api_response = api_instance.search_tariffs(v, tariffs_search_request)
        print("The response of TariffApi->search_tariffs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TariffApi->search_tariffs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **v** | **str**| Version of the API | [default to &#39;v0&#39;]
 **tariffs_search_request** | [**TariffsSearchRequest**](TariffsSearchRequest.md)| Tariffs search parameters. | 

### Return type

[**TariffsSearchResponse**](TariffsSearchResponse.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tariffs and mapping between tariff and search parameters. |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

