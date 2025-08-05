# PeakIdentificationSettings

Settings that defines how to identify a power peak during a billing period.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**peak_function** | **str** | A pseudo code function that describes how to identify a power peak for one power price component. Usage examples at https://someexamples. | [optional] [default to 'peak(main)']
**peak_identification_period** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 
**peak_duration** | **str** | A time duration in the format [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations). Examples: - \&quot;P1D\&quot; for one day - \&quot;P1M\&quot; for one month - \&quot;P2W\&quot; for two weeks - \&quot;P3Y6M4DT12H30M5S\&quot; for a complex duration. | [optional] 
**number_of_peaks_for_average_calculation** | **int** | The number of peaks within a peak pricing period for calculating average peak for that period. | [optional] 

## Example

```python
from openapi_client.models.peak_identification_settings import PeakIdentificationSettings

# TODO update the JSON string below
json = "{}"
# create an instance of PeakIdentificationSettings from a JSON string
peak_identification_settings_instance = PeakIdentificationSettings.from_json(json)
# print the JSON string representation of the object
print(PeakIdentificationSettings.to_json())

# convert the object into a dict
peak_identification_settings_dict = peak_identification_settings_instance.to_dict()
# create an instance of PeakIdentificationSettings from a dict
peak_identification_settings_from_dict = PeakIdentificationSettings.from_dict(peak_identification_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


