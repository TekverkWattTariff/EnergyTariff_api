"""This code initializes the API client and defines functions based on the tariff API"""
import sys
import os
import datetime
import json
from typing import Optional, Union

# Add OpenAPI-generated path for imports
sys.path.append(os.path.abspath("Openapi/GeneratedApiFiles"))

# Import OpenAPI-generated classes
from Openapi.GeneratedApiFiles.openapi_client.api_client import ApiClient
from Openapi.GeneratedApiFiles.openapi_client.configuration import Configuration
from Openapi.GeneratedApiFiles.openapi_client.api import tariff_api
from Openapi.GeneratedApiFiles.openapi_client.exceptions import NotFoundException

class Tariffs:
    """
    Class handling tariff-related operations using the provided tariff API.

    This class allows querying, retrieving, and working with electricity tariff
    information, including prices (fixed, energy, power) and metadata such as
    names, companies, and IDs. It also supports power cost optimization based
    on time intervals and provided kW data.

    Attributes:
        v (str): API version.
        url (str): Base API URL.
        tariff_id (str): Default tariff ID for operations if not explicitly provided.
        api_instance (TariffApi): Initialized API client instance for tariff operations.
        power_data (list): Internal list of power data points used for optimization.
    """
    v = "V0"
    url = None
    tariff_id= None
    api_instance = None
    
    def __init__(self,v,url = None,tariff_id = None) -> None:
        """
        Initializes the Tariffs class with API connection.

        Args:
            v (str): API version.
            url (str): Base URL of the API.
            tariff_id (str, optional): Optional default tariff ID to use.
        """
        self.price = self.Price(self)  # Initialize Price as a subcomponent
        self.v = v
        self.tariff_id = self.set_id(tariff_id)
        if url != None:
            url = url.replace("/v0/tariffs", "")
        self.url = url

        # Create OpenAPI configuration
        config = Configuration(host=url)

        # Initialize API client
        client = ApiClient(configuration=config)
        self.api_instance = tariff_api.TariffApi(api_client=client)
        #print(f"api_instance type: {type(self.api_instance)}") #Debugg
        pass
    
    def set_json_path(self, path: str) -> None:
        """Sets the local JSON file path to be used as fallback or source."""
        self._json_path = path

    def get_json_path(self) -> str:
        """Gets the currently set JSON file path."""
        return self._json_path

    def get_company(self, tariff_id: str) -> str:
        """
        Get the company name associated with a given tariff ID.

        Args:
            tariff_id (str): Tariff ID.

        Returns:
            str: Company name.
        """
        self.chek_id(tariff_id)
        tariff = self.get_tariff(tariff_id)
        return tariff.company_name
    
    def get_companys(self) -> list[str]:
        """
        Get a list of all company names available in the tariff API.

        Returns:
            list[str]: List of company names.
        """
        companys = []
        for tariff in self.get_tariffs():
            companys.append(tariff.company_name)
        return companys

    def get_tariffs(self) -> list:
        """
        Fetch all available tariffs from the live API.

        Returns:
            list: List of tariff objects.
        """
        response = self.api_instance.get_tariffs(self.v)
        #print("DEBUG - API response:", response)
        return response.tariffs

    def get_tariffs_byJson(self, path: str) -> list:
        """
        Fetch tariffs from a local JSON file.

        Args:
            path (str): Path to the JSON file.

        Returns:
            list: List of tariff objects.
        """
        # Check if file exists
        if not os.path.isfile(path):
            print(f"ERROR - File not found at: {path}")
            return []

        try:
            # Open and load the JSON file
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"ERROR - Failed to decode JSON: {e}")
            return []
        except Exception as e:
            print(f"ERROR - Unexpected error while reading file: {e}")
            return []

        # Check if 'tariffs' key exists and is a list
        tariffs = data.get('tariffs', [])
        if not isinstance(tariffs, list):
            print("ERROR - 'tariffs' key missing or not a list in JSON data.")
            return []

        return tariffs

    def get_tariff(self, tariff_id: Optional[str] = None) -> Optional[object]:
        """
        Retrieve a tariff object by ID from the API or JSON fallback.

        Args:
            tariff_id (str, optional): The tariff ID to look up.

        Returns:
            object | None: Tariff object if found, otherwise None.
        """
        tariffs = []
        self.chek_id(tariff_id)
        if self.url:
            # Try to fetch from API if URL is provided
            try:
                tariffs = self.get_tariffs()
            except Exception as e:
                print(f"ERROR - Failed to fetch from API: {e}")
                return None
        else:
            # No URL provided, fall back to JSON file
            path = self.get_json_path()
            if path is None:
                raise Exception("ERROR - No path is sett - use set_json_path to use a json file")
            tariffs = self.get_tariffs_byJson(path)

        for tariff in tariffs:
            tariff_id_value = getattr(tariff, 'id', None) or getattr(tariff, 'tariff_id', None)
            if tariff_id_value == tariff_id:
                return tariff
            
        return None
    
    def get_tariff_byName(self, tariff_name: str, company: str) -> object:
        """
        Retrieve a tariff by its name and company.

        Args:
            tariff_name (str): Name of the tariff.
            company (str): Company name.

        Returns:
            object: Tariff object.
        """
        tariff_id = self.get_id_byName(tariff_name,company)
        response = self.api_instance.get_tariff_by_id(self.v,tariff_id)
        return response.tariff
    
    def get_tariffs_ids(self) -> list[str]:
        """
        Get a list of all tariff IDs from the API.

        Returns:
            list[str]: List of tariff IDs.
        """
        tariffs = self.get_tariffs()
        return [tariff.tariff_id for tariff in tariffs]
    
    def get_tariffs_names(self) -> list[str]:
        """
        Get a list of all tariff names from the API.

        Returns:
            list[str]: List of tariff names.
        """
        names = []
        for tariff in self.get_tariffs():
            names.append(tariff.name)
        return names
    
    def get_id(self, index: int) -> str:
        """
        Get a tariff ID by index in the list of tariffs.

        Args:
            index (int): Index of the tariff.

        Returns:
            str: Tariff ID.

        Raises:
            IndexError: If the index is out of range.
        """
        tariffs = self.get_tariffs()
        if 0 <= index < len(tariffs):
            return tariffs[index].tariff_id
        raise IndexError("Index out of range")
    
    def set_id(self, tariff_id: str) -> None:
        """
        Set the default tariff ID for the instance.

        Args:
            tariff_id (str): Tariff ID to set.
        """
        self.tariff_id = tariff_id
        return

    def chek_id(self, tariff_id: str) -> bool:
        """
        Check if the given tariff ID exists in the API.

        Args:
            tariff_id (str): Tariff ID to check.

        Returns:
            bool: True if found, False otherwise.
        """
        return any(t.tariff_id == tariff_id for t in self.get_tariffs())

    def get_id_byName(self, tariff_name: str, company: str) -> str:
        """
        Find and return the tariff ID by its name and company.

        Args:
            tariff_name (str): Name of the tariff.
            company (str): Name of the company.

        Returns:
            str: Tariff ID.

        Raises:
            ValueError: If the company doesn't exist in the API.
        """
        if company not in self.get_companys():
            raise ValueError(f"Company '{company}' does not exist in the API.")

        index = next(
            (i for i, t in enumerate(self.get_tariffs()) 
                if t.name == tariff_name and t.company_name == company), 
            None
        )
        # Cheks so index isnt None
        if index is None:
            raise ValueError("No matching tariff found for the given name and company.")
        return self.get_id(index)
    
    class Price:
        """
        Class for handling price-related logic, including retrieving time-based
        fixed, energy, and power pricing from tariff definitions.

        Provides utility methods to:
        - Retrieve current price components for a given datetime.
        - Extract individual price types (fixed, energy, power).
        - Support power optimization logic via the Power subclass.
        """
        api_PriceInstant = None
        tariff_id = None

        def __init__(self,parent=None) -> None:
            """
            Initializes the price class with a reference to its parent Tariff instance.

            Args:
                parent (Tariff): Instance of the parent class Tariff.
            """
            if parent != None:
                    self.parent = parent
            else:
                self.parent = Tariffs
            self.power = self.Power(self)  # Initialize Power as a subcomponent
            self.set_id(parent.tariff_id)
            return
        
        def set_id(self, tariff_id: str) -> None:
            """
            Set the default tariff ID for the instance.

            Args:
                tariff_id (str): Tariff ID to set.
            """
            self.tariff_id = tariff_id
            return

        def find_matching_time_period(self, components: list[object], datetime_input: datetime.datetime) -> Optional[object]:
            """
            Find a matching price component for a given datetime.

            Args:
                components (list): List of price components.
                datetime_input (datetime.datetime): The datetime to match against.

            Returns:
                object or None: Matching component or None if not found.
            """
            date_input = datetime_input.date()
            time_input = datetime_input.time()

            for comp in components:
                valid_ok = True
                if hasattr(comp, "valid_period"):
                    valid_from = comp.valid_period.from_including
                    valid_to = comp.valid_period.to_excluding

                    if isinstance(valid_from, str):
                        valid_from = datetime.datetime.strptime(valid_from, "%Y-%m-%d").date()
                    if isinstance(valid_to, str):
                        valid_to = datetime.datetime.strptime(valid_to, "%Y-%m-%d").date()

                    valid_ok = valid_from <= date_input < valid_to

                if not valid_ok:
                    continue

                # If no recurring_periods, component is always active
                if not hasattr(comp, "recurring_periods") or not comp.recurring_periods:
                    return comp

                # Check if the time is within any active recurring periods
                for period in comp.recurring_periods:
                    for active in period.active_periods:
                        from_time = datetime.datetime.strptime(active.from_including, "%H:%M:%S").time()
                        to_time = datetime.datetime.strptime(active.to_excluding, "%H:%M:%S").time()

                        if from_time < to_time:
                            match = from_time <= time_input < to_time
                        else:
                            # Handle overnight periods
                            match = time_input >= from_time or time_input < to_time

                        if match:
                            return comp

            # No matching component found
            return None

        def get_fixed_price(self, tariff_id: str, datetime_input: datetime.datetime) -> list[dict]:
            """
            Get fixed price components valid at a specific datetime.

            Args:
                tariff_id (str): Tariff ID.
                datetime_input (datetime.datetime): Datetime to check.

            Returns:
                list: List of price components.
            """
            self.parent.chek_id(tariff_id)
            tariff = self.parent.get_tariff(tariff_id)
            components = getattr(tariff.fixed_price, "components", [])

            matching_components = []

            for comp in components:
                valid_from = comp.valid_period.from_including
                valid_to = comp.valid_period.to_excluding

                # Convert datetime.date to datetime.datetime if needed
                if isinstance(valid_from, datetime.date) and not isinstance(valid_from, datetime.datetime):
                    valid_from = datetime.datetime(valid_from.year, valid_from.month, valid_from.day)
                if isinstance(valid_to, datetime.date) and not isinstance(valid_to, datetime.datetime):
                    valid_to = datetime.datetime(valid_to.year, valid_to.month, valid_to.day)

                # Check if component is valid for the given datetime
                if valid_from <= datetime_input < valid_to:
                    price = getattr(comp, "price", None)

                    if price is None:
                        price_data = {
                            "priceExVat": 0,
                            "priceIncVat": 0,
                            "currency": "SEK"
                        }
                    else:
                        price_data = {
                            "priceExVat": getattr(price, "price_ex_vat", 0),
                            "priceIncVat": getattr(price, "price_inc_vat", 0),
                            "currency": getattr(price, "currency", "SEK")
                        }

                    component_data = {
                        "id": getattr(comp, "id", ""),
                        "name": getattr(comp, "name", ""),
                        "price": price_data,
                        "pricedPeriod": getattr(comp, "pricedPeriod", "P1M"),
                        "costFunction": getattr(tariff.fixed_price,"costFunction",None)
                    }

                    matching_components.append(component_data)

            return matching_components

        def get_energy_price(self, tariff_id: str, datetime_input: datetime.datetime) -> list[dict]:
            """
            Get energy price components valid at a specific datetime.

            Args:
                tariff_id (str): Tariff ID.
                datetime_input (datetime.datetime): Datetime to check.

            Returns:
                list: List of price components.
            """
            self.parent.chek_id(tariff_id)
            tariff = self.parent.get_tariff(tariff_id)
            components = getattr(tariff.energy_price, "components", [])

            matching_components = []

            for comp in components:
                valid_from = comp.valid_period.from_including
                valid_to = comp.valid_period.to_excluding

                # Convert datetime.date to datetime.datetime if needed
                if isinstance(valid_from, datetime.date) and not isinstance(valid_from, datetime.datetime):
                    valid_from = datetime.datetime(valid_from.year, valid_from.month, valid_from.day)
                if isinstance(valid_to, datetime.date) and not isinstance(valid_to, datetime.datetime):
                    valid_to = datetime.datetime(valid_to.year, valid_to.month, valid_to.day)

                # Check if component is valid for the given datetime
                if valid_from <= datetime_input < valid_to:
                    price = getattr(comp, "price", None)

                    if price is None:
                        price_data = {
                            "priceExVat": 0,
                            "priceIncVat": 0,
                            "currency": "SEK"
                        }
                    else:
                        price_data = {
                            "priceExVat": getattr(price, "price_ex_vat", 0),
                            "priceIncVat": getattr(price, "price_inc_vat", 0),
                            "currency": getattr(price, "currency", "SEK")
                        }

                    component_data = {
                        "id": getattr(comp, "id", ""),
                        "name": getattr(comp, "name", ""),
                        "price": price_data,
                        "pricedPeriod": getattr(comp, "pricedPeriod", "P1M"),
                        "costFunction": getattr(tariff.energy_price,"costFunction",None)
                    }

                    matching_components.append(component_data)

            return matching_components
        
        def get_power_price(self, tariff_id: str, datetime_input: datetime.datetime) -> list[dict]:
            """
            Get power price components valid at a specific datetime.

            Args:
                tariff_id (str): Tariff ID.
                datetime_input (datetime.datetime): Datetime to check.

            Returns:
                list: List of price components.
            """
            self.parent.chek_id(tariff_id)
            tariff = self.parent.get_tariff(tariff_id)
            components = getattr(tariff.power_price, "components", [])

            matching_components = []

            for comp in components:
                valid_from = comp.valid_period.from_including
                valid_to = comp.valid_period.to_excluding

                # Convert datetime.date to datetime.datetime if needed
                if isinstance(valid_from, datetime.date) and not isinstance(valid_from, datetime.datetime):
                    valid_from = datetime.datetime(valid_from.year, valid_from.month, valid_from.day)
                if isinstance(valid_to, datetime.date) and not isinstance(valid_to, datetime.datetime):
                    valid_to = datetime.datetime(valid_to.year, valid_to.month, valid_to.day)

                # Check if component is valid for the given datetime
                if valid_from <= datetime_input < valid_to:
                    price = getattr(comp, "price", None)

                    if price is None:
                        price_data = {
                            "priceExVat": 0,
                            "priceIncVat": 0,
                            "currency": "SEK"
                        }
                    else:
                        price_data = {
                            "priceExVat": getattr(price, "price_ex_vat", 0),
                            "priceIncVat": getattr(price, "price_inc_vat", 0),
                            "currency": getattr(price, "currency", "SEK")
                        }

                    component_data = {
                        "id": getattr(comp, "id", ""),
                        "name": getattr(comp, "name", ""),
                        "price": price_data,
                        "pricedPeriod": getattr(comp, "pricedPeriod", "P1M"),
                        "costFunction": getattr(tariff.power_price,"costFunction",None)
                    }

                    matching_components.append(component_data)
                    #print(f"[DEBUG] Checking power price for {datetime_input}")
                    #print(f"[DEBUG] Matching components: {matching_components}")

            return matching_components

        def get_price(self, tariff_id: str, datetime_input: datetime.datetime) -> dict[str, list[dict]]:
            """
            Get all price components (fixed, energy, power) for a specific datetime.

            Args:
                tariff_id (str): Tariff ID.
                datetime_input (datetime.datetime): Datetime to retrieve prices for.

            Returns:
                dict: Dictionary with fixed, energy, and power price components.
            """
            fixed_price = self.get_fixed_price(tariff_id, datetime_input)
            energy_price = self.get_energy_price(tariff_id, datetime_input)
            power_price = self.get_power_price(tariff_id, datetime_input)

            return {
                "fixed_price": fixed_price,
                "energy_price": energy_price,
                "power_price": power_price
            }

        class Energy:
            """
            Subclass of Price for energy data handling and optimization logic.

            Handles:
            - Storing and processing time-series energy data.
            - Calculating durations and averages.
            - Finding optimal start times for minimizing energy costs.
            """
            tariff_id = None
            energy_data = [{"datetime":None,"kW":None}]
            def __init__(self,parent=None) -> None:
                """
                Initializes the Energy class with a reference to its parent Price instance.

                Args:
                    parent (Price): Instance of the parent class Price.
                """
                if parent != None:
                    self.parent = parent
                else:
                    self.parent = Tariffs.Price
                self.set_id(parent.tariff_id)
                pass

            def set_id(self, tariff_id: str) -> None:
                    """
                    Set the default tariff ID for the instance.

                    Args:
                        tariff_id (str): Tariff ID to set.
                    """
                    self.tariff_id = tariff_id
                    return

            def set_data(self, energy_data_input: Union[dict[str, Union[str, float]], list[dict[str, Union[str, float]]]]) -> list[dict[str, Union[str, float]]]:
                """
                Accepts and stores energy data.

                Supports:
                - A single dictionary with 'datetime' and 'kW' keys
                - A list of such dictionaries
                - A list of (datetime, kW) tuples

                Converts datetime objects to ISO 8601 strings and maintains a sorted list.
                """

                # Normalize input to a list
                if isinstance(energy_data_input, dict):
                    data_points = [energy_data_input]
                elif isinstance(energy_data_input, list):
                    data_points = energy_data_input
                else:
                    raise ValueError("Expected a dict or a list of dicts or tuples")

                cleaned_data = []

                for dp in data_points:
                    if isinstance(dp, dict) and "datetime" in dp and "kW" in dp:
                        # Ensure datetime is ISO string
                        dt_str = (
                            dp["datetime"].isoformat()
                            if isinstance(dp["datetime"], datetime.datetime)
                            else str(dp["datetime"])
                        )
                        cleaned_data.append({"datetime": dt_str, "kW": dp["kW"]})
                    elif isinstance(dp, (tuple, list)) and len(dp) == 2:
                        dt, kW = dp
                        if isinstance(dt, datetime.datetime):
                            cleaned_data.append({"datetime": dt.isoformat(), "energy_data": kW})
                        else:
                            raise ValueError("Tuple must have datetime.datetime as first element")
                    else:
                        raise ValueError("Each data point must be a dict or (datetime, value) tuple")

                # Remove any existing entries that are empty
                #print("Before cleaning:", self.energy_data)  # Debug
                self.energy_data = [p for p in self.energy_data if p["datetime"] is not None]
                #print("After cleaning:", self.energy_data)  # Debug

                # Append new entries
                self.energy_data.extend(cleaned_data)

                # Sort the data by datetime
                self.energy_data.sort(
                    key=lambda x: datetime.datetime.fromisoformat(x["datetime"])
                )
                return self.energy_data

            def get_mean(self,energy_data_input: list[float]) -> float:
                """
                Calculate the mean energy value from a list of values.

                Args:
                    energy_data (list[float]): List of energy values.

                Returns:
                    float: Mean value.
                """
                mean_value = sum(energy_data_input)/len(energy_data_input)
                return mean_value
            
            def get_duration(self, energy_data_input: Optional[list[dict[str, Union[str, float]]]]) -> datetime.timedelta:
                """
                Calculate duration between first and last timestamps in the data.

                Args:
                    data (list): List of data dicts with 'datetime' key.

                Returns:
                    datetime.timedelta: Duration.
                """
                if energy_data_input != None:
                    energy_data = energy_data_input
                else:
                    energy_data = self.energy_data

                if len(energy_data) < 2:
                    raise ValueError("Not enough power data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in energy_data]
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def extract_price_value(self, price_obj: Union[dict, object]) -> float:
                """
                Extract a numeric price from various price object formats.

                Args:
                    price_obj (dict or object): Price container.

                Returns:
                    float: Price value.

                Raises:
                    ValueError: If price cannot be extracted.
                """
                #print(f"In extract_price: {price_obj}") #debug

                # === EARLY EXIT if price_obj is already a price dict ===
                if isinstance(price_obj, dict):
                    if "priceIncVat" in price_obj:
                        return float(price_obj["priceIncVat"])
                    elif "priceExVat" in price_obj:
                        return float(price_obj["priceExVat"])
                    
                # If object with .price attribute that is a dict or object
                try:
                    price_attr = price_obj.price
                    print(price_attr)
                    if isinstance(price_attr, (float, int)):
                        return float(price_attr)
                    elif isinstance(price_attr, dict):
                        if "priceIncVat" in price_attr:
                            return float(price_attr["price_inc_vat"])
                        elif "priceExVat" in price_attr:
                            return float(price_attr["price_ex_vat"])
                except AttributeError:
                    pass

                # If dict with 'price' key that is a dict
                try:
                    price_data = price_obj["price"]
                    print(f"in string try: price_data: {price_data}")
                    if isinstance(price_data, (float, int)):
                        return float(price_data)
                    elif isinstance(price_data, dict):
                        if "price_inc_vat" in price_data:
                            return float(price_data["price_inc_vat"])
                        elif "price_ex_vat" in price_data:
                            return float(price_data["price_ex_vat"])
                except (KeyError, TypeError):
                    pass

                # If price_obj itself is a dict with priceIncVat/priceExVat
                if isinstance(price_obj, dict):
                    if "price_inc_vat" in price_obj:
                        return float(price_obj["price_inc_vat"])
                    elif "price_ex_vat" in price_obj:
                        return float(price_obj["price_ex_vat"])

                raise ValueError("Could not extract numeric price from energy_price object.")

            def extract_price_function(self, price_obj: Union[dict, object]) -> float:
                """
                Extracts a string value of 'costFunction' from an object or dictionary.

                Args:
                    price_obj (object or dict): Container that may hold a 'costFunction'.

                Returns:
                    str: The extracted cost function string.

                Raises:
                    ValueError: If no valid costFunction is found.
                """
                # === EARLY EXIT if price_obj is already a price dict ===
                if isinstance(price_obj, dict) and "costFunction" in price_obj:
                    return price_obj["costFunction"]

                # If object with .costFunction attribute
                try:
                    cost_function = price_obj.costFunction
                    if isinstance(cost_function, str):
                        return cost_function
                except AttributeError:
                    pass

                # If dict with 'costFunction' key nested
                try:
                    cost_data = price_obj["costFunction"]
                    if isinstance(cost_data, str):
                        return cost_data
                    elif isinstance(cost_data, dict) and "costFunction" in cost_data:
                        return cost_data["costFunction"]
                except (KeyError, TypeError):
                    pass

                raise ValueError("Could not extract costFunction from the input object.")

            def get_optimal_start(self, energy_data: Optional[list[float]]) -> datetime.datetime:
                """
                Finds the optimal start time within the next 24h that minimizes
                total energy cost based on provided or stored energy data.

                Args:
                    energy_data (list[dict], optional): List of energy data points.

                Returns:
                    datetime.datetime: Optimal start time.

                Raises:
                    ValueError: If input data is missing or invalid.
                """
                #print(f"in optimal_start. energy_data={energy_data} ")
                if energy_data is None:
                    energy_data = self.energy_data

                if len(energy_data) < 2:
                    raise ValueError("Not enough data points to calculate duration.")

                # Calculate duration from first to last timestamp
                start_time = datetime.datetime.fromisoformat(energy_data[0]["datetime"])
                end_time = datetime.datetime.fromisoformat(energy_data[-1]["datetime"])
                #print(f"start_time={start_time} and end_time={end_time}")
                duration = end_time - start_time
                #print(f"duraiton={duration}")
                hours = int(duration.total_seconds() // 3600)
                #print(f"hours={hours}")

                if hours <= 0:
                    raise ValueError("Duration must be at least one hour.")

                # Use default tariff
                tariff_id = self.tariff_id

                # Loop through potential start times over the next 24 hours
                now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
                latest_start = now + datetime.timedelta(hours=(24 - hours))  # latest valid start
                #print(f"latest_start={type(latest_start)}")

                best_start = None
                lowest_total_price = float("inf")

                check_time = now
                #print(f"{check_time} <= {latest_start}: {check_time <= latest_start}")
                while check_time <= latest_start:
                    total_price = 0
                    for i in range(hours):
                        current_time = check_time + datetime.timedelta(hours=i)

                        try:
                            energy_components = self.parent.get_energy_price(tariff_id,current_time)
                            hour_price = sum(self.extract_price_value(comp["price"]) for comp in energy_components)
                            total_price += hour_price

                        except Exception:
                            total_price = float("inf")
                            break
                    if total_price < lowest_total_price:
                        lowest_total_price = total_price
                        best_start = check_time

                    check_time += datetime.timedelta(hours=1)
                #print(f"total_price={total_price}")
                return best_start
            
            def get_cost(self, now: datetime.datetime, kW: float) -> float:
                """
                Calculates the cost of operating at a specific time with given energy usage.

                Args:
                    now (datetime): The datetime for which to calculate the cost.
                    kW (float): Energy usage in kilowatts.

                Returns:
                    float: Cost of operation at the given time.
                """

                # Ensure 'now' is a datetime object
                if not isinstance(now, datetime.datetime):
                    raise ValueError("'now' must be a datetime object")

                try:
                    # Use the instance's default tariff ID
                    tariff_id = self.tariff_id

                    # Fetch energy price components at the given time
                    energy_components = self.parent.get_energy_price(self.parent,tariff_id, now)

                    # Sum up all price components (e.g., energy, grid fee, taxes, etc.)
                    price_per_kWh = sum(self.extract_price_value(comp["price"]) for comp in energy_components)

                    # Calculate cost as price per kWh multiplied by the power usage (kW)
                    cost = price_per_kWh * kW
                    return cost

                except Exception as e:
                    # If price lookup fails, return infinite cost (or optionally log the error)
                    print(f"Error calculating price at {now}: {e}")
                    return float("inf")

            def get_operation_mean_cost(self, start_time: datetime.datetime, time_duration: Union[str, datetime.timedelta], energy_data: dict) -> float:
                """
                Calculate total cost of operation over a time period using average power usage.

                Args:
                    start_time (datetime.datetime): Start time of the operation.
                    time_duration (str or timedelta): Duration of the operation.
                    power_data (dict): Dictionary with 'peak' key containing list of power values.

                Returns:
                    float: Total cost over the operation period.
                """
                # Use default tariff
                tariff_id = self.tariff_id
                # Calculate mean power usage from the provided power data (e.g., from "peak" values)
                power_mean = self.get_mean(energy_data["kW"])

                # If time_duration is a string, convert it to a timedelta
                if isinstance(time_duration, str):
                    hours, minutes, seconds = map(int, time_duration.split(":"))
                    duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                elif isinstance(time_duration, datetime.timedelta):
                    # If already a timedelta, use as-is
                    duration = time_duration
                else:
                    # Raise an error if time_duration is not of expected types
                    raise ValueError("time_duration must be a string in 'HH:MM:SS' format or a timedelta")
                
                # Set initial time pointer and calculate the end time
                current_time = start_time
                end_time = start_time + duration

                # Start with total cost as 0
                total_price = 0.0

                # Loop through each hour in the interval
                while current_time <= end_time:
                    try:
                        # Retrieve power price components for the current hour
                        energy_components = self.parent.get_energy_price(self.parent,tariff_id,current_time)
                        # Extract and sum price values from all components (e.g., grid cost, tax, etc.)
                        hour_price = sum(self.extract_price_value(comp["price"]) for comp in energy_components)
                        # Multiply hourly price by average power usage to get cost for this hour
                        total_price += hour_price * power_mean

                    except Exception:
                        # If an error occurs (e.g., missing price data), assume operation fails and set cost to infinite
                        total_price = float("inf")
                        break
                    # Advance time by one hour
                    current_time += datetime.timedelta(hours=1)
                # Return total cost for the time interval
                return total_price
            
        class Power:
            """
            Subclass of Price for power data handling and optimization logic.

            Handles:
            - Storing and processing time-series power data.
            - Calculating durations and averages.
            - Finding optimal start times for minimizing power costs.
            """
            tariff_id = None
            power_data = [{"datetime":None,"peak":None}]
            def __init__(self,parent=None) -> None:
                """
                Initializes the Power class with a reference to its parent Price instance.

                Args:
                    parent (Price): Instance of the parent class Price.
                """
                if parent != None:
                    self.parent = parent
                else:
                    self.parent = Tariffs.Price
                self.set_id(parent.tariff_id)
                pass

            def set_id(self, tariff_id: str) -> None:
                    """
                    Set the default tariff ID for the instance.

                    Args:
                        tariff_id (str): Tariff ID to set.
                    """
                    self.tariff_id = tariff_id
                    return

            def set_data(self, power_data_input: Union[dict[str, Union[str, float]], list[dict[str, Union[str, float]]]]) -> list[dict[str, Union[str, float]]]:
                """
                Accepts and stores power data.

                Supports:
                - A single dictionary with 'datetime' and 'kW' keys
                - A list of such dictionaries
                - A list of (datetime, kW) tuples

                Converts datetime objects to ISO 8601 strings and maintains a sorted list.
                """

                # Normalize input to a list
                if isinstance(power_data_input, dict):
                    data_points = [power_data_input]
                elif isinstance(power_data_input, list):
                    data_points = power_data_input
                else:
                    raise ValueError("Expected a dict or a list of dicts or tuples")

                cleaned_data = []

                for dp in data_points:
                    if isinstance(dp, dict) and "datetime" in dp and "kW" in dp:
                        # Ensure datetime is ISO string
                        dt_str = (
                            dp["datetime"].isoformat()
                            if isinstance(dp["datetime"], datetime.datetime)
                            else str(dp["datetime"])
                        )
                        cleaned_data.append({"datetime": dt_str, "kW": dp["kW"]})
                    elif isinstance(dp, (tuple, list)) and len(dp) == 2:
                        dt, kW = dp
                        if isinstance(dt, datetime.datetime):
                            cleaned_data.append({"datetime": dt.isoformat(), "power_data": kW})
                        else:
                            raise ValueError("Tuple must have datetime.datetime as first element")
                    else:
                        raise ValueError("Each data point must be a dict or (datetime, value) tuple")

                # Remove any existing entries that are empty
                #print("Before cleaning:", self.power_data)  # Debug
                self.power_data = [p for p in self.power_data if p["datetime"] is not None]
                #print("After cleaning:", self.power_data)  # Debug

                # Append new entries
                self.power_data.extend(cleaned_data)

                # Sort the data by datetime
                self.power_data.sort(
                    key=lambda x: datetime.datetime.fromisoformat(x["datetime"])
                )
                return self.power_data

            def get_mean(self,power_data: list[float]) -> float:
                """
                Calculate the mean power value from a list of values.

                Args:
                    power_data (list[float]): List of power values.

                Returns:
                    float: Mean value.
                """
                mean_value = sum(power_data)/len(power_data)
                return mean_value
            
            def get_duration(self, power_data_input: Optional[list[dict[str, Union[str, float]]]]) -> datetime.timedelta:
                """
                Calculate duration between first and last timestamps in the data.

                Args:
                    data (list): List of data dicts with 'datetime' key.

                Returns:
                    datetime.timedelta: Duration.
                """

                if power_data_input != None:
                    power_data = power_data_input
                else:
                    power_data = self.power_data

                if len(power_data) < 2:
                    raise ValueError("Not enough power data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in power_data]
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def extract_price_value(self, price_obj: Union[dict, object]) -> float:
                """
                Extract a numeric price from various price object formats.

                Args:
                    price_obj (dict or object): Price container.

                Returns:
                    float: Price value.

                Raises:
                    ValueError: If price cannot be extracted.
                """
                #print(f"In extract_price: {price_obj}") #debug

                # === EARLY EXIT if price_obj is already a price dict ===
                if isinstance(price_obj, dict):
                    if "priceIncVat" in price_obj:
                        return float(price_obj["priceIncVat"])
                    elif "priceExVat" in price_obj:
                        return float(price_obj["priceExVat"])
                    
                # If object with .price attribute that is a dict or object
                try:
                    price_attr = price_obj.price
                    print(price_attr)
                    if isinstance(price_attr, (float, int)):
                        return float(price_attr)
                    elif isinstance(price_attr, dict):
                        if "priceIncVat" in price_attr:
                            return float(price_attr["price_inc_vat"])
                        elif "priceExVat" in price_attr:
                            return float(price_attr["price_ex_vat"])
                except AttributeError:
                    pass

                # If dict with 'price' key that is a dict
                try:
                    price_data = price_obj["price"]
                    print(f"in string try: price_data: {price_data}")
                    if isinstance(price_data, (float, int)):
                        return float(price_data)
                    elif isinstance(price_data, dict):
                        if "price_inc_vat" in price_data:
                            return float(price_data["price_inc_vat"])
                        elif "price_ex_vat" in price_data:
                            return float(price_data["price_ex_vat"])
                except (KeyError, TypeError):
                    pass

                # If price_obj itself is a dict with priceIncVat/priceExVat
                if isinstance(price_obj, dict):
                    if "price_inc_vat" in price_obj:
                        return float(price_obj["price_inc_vat"])
                    elif "price_ex_vat" in price_obj:
                        return float(price_obj["price_ex_vat"])

                raise ValueError("Could not extract numeric price from power_price object.")

            def extract_price_function(self, price_obj: Union[dict, object]) -> float:
                """
                Extracts a string value of 'costFunction' from an object or dictionary.

                Args:
                    price_obj (object or dict): Container that may hold a 'costFunction'.

                Returns:
                    str: The extracted cost function string.

                Raises:
                    ValueError: If no valid costFunction is found.
                """
                # === EARLY EXIT if price_obj is already a price dict ===
                if isinstance(price_obj, dict) and "costFunction" in price_obj:
                    return price_obj["costFunction"]

                # If object with .costFunction attribute
                try:
                    cost_function = price_obj.costFunction
                    if isinstance(cost_function, str):
                        return cost_function
                except AttributeError:
                    pass

                # If dict with 'costFunction' key nested
                try:
                    cost_data = price_obj["costFunction"]
                    if isinstance(cost_data, str):
                        return cost_data
                    elif isinstance(cost_data, dict) and "costFunction" in cost_data:
                        return cost_data["costFunction"]
                except (KeyError, TypeError):
                    pass

                raise ValueError("Could not extract costFunction from the input object.")

            def get_optimal_start(self, power_data: Optional[list[float]]) -> datetime.datetime:
                """
                Finds the optimal start time within the next 24h that minimizes
                total power cost based on provided or stored power data.

                Args:
                    power_data (list[dict], optional): List of power data points.

                Returns:
                    datetime.datetime: Optimal start time.

                Raises:
                    ValueError: If input data is missing or invalid.
                """
                #print(f"in optimal_start. power_data={power_data} ")
                if power_data is None:
                    power_data = self.power_data

                if len(power_data) < 2:
                    raise ValueError("Not enough data points to calculate duration.")

                # Calculate duration from first to last timestamp
                start_time = datetime.datetime.fromisoformat(power_data[0]["datetime"])
                end_time = datetime.datetime.fromisoformat(power_data[-1]["datetime"])
                #print(f"start_time={start_time} and end_time={end_time}")
                duration = end_time - start_time
                #print(f"duraiton={duration}")
                hours = int(duration.total_seconds() // 3600)
                #print(f"hours={hours}")

                if hours <= 0:
                    raise ValueError("Duration must be at least one hour.")

                # Use default tariff
                tariff_id = self.tariff_id

                # Loop through potential start times over the next 24 hours
                now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
                latest_start = now + datetime.timedelta(hours=(24 - hours))  # latest valid start
                #print(f"latest_start={type(latest_start)}")

                best_start = None
                lowest_total_price = float("inf")

                check_time = now
                #print(f"{check_time} <= {latest_start}: {check_time <= latest_start}")
                while check_time <= latest_start:
                    total_price = 0
                    for i in range(hours):
                        current_time = check_time + datetime.timedelta(hours=i)

                        try:
                            power_components = self.parent.get_power_price(tariff_id,current_time)
                            hour_price = sum(self.extract_price_value(comp["price"]) for comp in power_components)
                            total_price += hour_price

                        except Exception:
                            total_price = float("inf")
                            break
                    if total_price < lowest_total_price:
                        lowest_total_price = total_price
                        best_start = check_time

                    check_time += datetime.timedelta(hours=1)
                #print(f"total_price={total_price}")
                return best_start
            
            def get_cost(self, now: datetime.datetime, kW: float) -> float:
                """
                Calculates the cost of operating at a specific time with given power usage.

                Args:
                    now (datetime): The datetime for which to calculate the cost.
                    kW (float): power usage in kilowatts.

                Returns:
                    float: Cost of operation at the given time.
                """

                # Ensure 'now' is a datetime object
                if not isinstance(now, datetime.datetime):
                    raise ValueError("'now' must be a datetime object")

                try:
                    # Use the instance's default tariff ID
                    tariff_id = self.tariff_id

                    # Fetch power price components at the given time
                    power_components = self.parent.get_power_price(self.parent,tariff_id, now)

                    # Sum up all price components (e.g., power, grid fee, taxes, etc.)
                    price_per_kWh = sum(self.extract_price_value(comp["price"]) for comp in power_components)

                    # Calculate cost as price per kWh multiplied by the power usage (kW)
                    cost = price_per_kWh * kW
                    return cost

                except Exception as e:
                    # If price lookup fails, return infinite cost (or optionally log the error)
                    print(f"Error calculating price at {now}: {e}")
                    return float("inf")

            def get_operation_mean_cost(self, start_time: datetime.datetime, time_duration: Union[str, datetime.timedelta], power_data: dict) -> float:
                """
                Calculate total cost of operation over a time period using average power usage.

                Args:
                    start_time (datetime.datetime): Start time of the operation.
                    time_duration (str or timedelta): Duration of the operation.
                    power_data (dict): Dictionary with 'peak' key containing list of power values.

                Returns:
                    float: Total cost over the operation period.
                """
                # Use default tariff
                tariff_id = self.tariff_id
                # Calculate mean power usage from the provided power data (e.g., from "peak" values)
                power_mean = self.get_mean(power_data["kW"])

                # If time_duration is a string, convert it to a timedelta
                if isinstance(time_duration, str):
                    hours, minutes, seconds = map(int, time_duration.split(":"))
                    duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
                elif isinstance(time_duration, datetime.timedelta):
                    # If already a timedelta, use as-is
                    duration = time_duration
                else:
                    # Raise an error if time_duration is not of expected types
                    raise ValueError("time_duration must be a string in 'HH:MM:SS' format or a timedelta")
                
                # Set initial time pointer and calculate the end time
                current_time = start_time
                end_time = start_time + duration

                # Start with total cost as 0
                total_price = 0.0

                # Loop through each hour in the interval
                while current_time <= end_time:
                    try:
                        # Retrieve power price components for the current hour
                        power_components = self.parent.get_power_price(tariff_id,current_time)
                        # Extract and sum price values from all components (e.g., grid cost, tax, etc.)
                        hour_price = sum(self.extract_price_value(comp["price"]) for comp in power_components)
                        # Multiply hourly price by average power usage to get cost for this hour
                        total_price += hour_price * power_mean

                    except Exception:
                        # If an error occurs (e.g., missing price data), assume operation fails and set cost to infinite
                        total_price = float("inf")
                        break
                    # Advance time by one hour
                    current_time += datetime.timedelta(hours=1)
                # Return total cost for the time interval
                return total_price