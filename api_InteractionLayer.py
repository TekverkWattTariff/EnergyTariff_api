"""This code initializes the API client and defines functions based on the tariff API"""
import math
import sys
import os
import re
import time
import datetime
import isodate
import json
from typing import Optional, Union
from dateutil.parser import isoparse
import threading
import queue as q 

# Add OpenAPI-generated path for imports
sys.path.append(os.path.abspath("Openapi/GeneratedApiFiles"))

# Import OpenAPI-generated classes
from Openapi.GeneratedApiFiles.openapi_client.api_client import ApiClient
from Openapi.GeneratedApiFiles.openapi_client.configuration import Configuration
from Openapi.GeneratedApiFiles.openapi_client.api import tariff_api
#==========================For Helper Functions============================
from Openapi.GeneratedApiFiles.openapi_client.models.tariff import Tariff

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
    v = "v0"
    url = ""
    tariff_id = ""
    api_instance = tariff_api.TariffApi
    _json_path = ""

    def __init__(self, v: str, url: Optional[str] = None, json_path: Optional[str] = None, tariff_id: Optional[str] = None) -> None:
        """
        Initialize the Tariffs class with API configuration.

        If no URL is provided, it will attempt to load data from the JSON path.
        If neither are provided, an error is raised.

        Args:
            v (str): API version to use.
            url (Optional[str]): API base URL. If None, a JSON file must be provided.
            json_path (Optional[str]): Path to a local JSON file with tariff data.
            tariff_id (Optional[str]): Optional default tariff ID to set.
        """
        self.v = v
        self._json_path = json_path
        self.tariff_id = tariff_id
        self.last_updated = None
        self.cost_queue = q.Queue()
        self.tariffs_queue = q.Queue()
        self.single_tariff_queue = q.Queue()

        # Initialize nested classes
        self.price = self.Price(self)
        self.energy = self.price.Energy(self.price)
        self.power = self.price.Power(self.price)

        if url:
            clean_url = url.replace("/v0/tariffs", "")
            self.url = clean_url
            config = Configuration(host=clean_url)
            client = ApiClient(configuration=config)
            self.api_instance = tariff_api.TariffApi(api_client=client)
            self.tariffs = self.get_tariffs()  # API mode
        elif json_path:
            self.url = None
            self.api_instance = None
            self.tariffs = self.get_tariffs_byJson(json_path)  # JSON mode
        else:
            raise ValueError("No URL or JSON path provided.")

        if tariff_id is not None:
            self.set_id(tariff_id)
    
    def set_json_path(self, path: str) -> None:
        """Sets the local JSON file path to be used as fallback or source."""
        self._json_path = path

    def get_json_path(self) -> str:
        """Gets the currently set JSON file path."""
        return self._json_path # type: ignore

    def get_company(self, tariff_id: str) -> str:
        """
        Get the company name associated with a given tariff ID.

        Args:
            tariff_id (str): Tariff ID.

        Returns:
            str: Company name.
        """
        self.check_id(tariff_id)
        tariff = self.get_tariff(tariff_id)
        return tariff.company_name # type: ignore
    
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
        Retrieve all available tariffs.

        If a JSON path is set, it loads tariffs from that file.
        Otherwise, it fetches from the live API endpoint.

        Returns:
            list: A list of tariff objects.
        """
        if self._json_path is None:
            response = self.api_instance.get_tariffs(self.v) # type: ignore
            return response.tariffs # type: ignore
        else: #JSON file
            raw_tariffs = self.get_tariffs_byJson(self._json_path)
            tariffs = []
            for t in raw_tariffs:
                obj = self.dict_to_tariff(t)
                if obj is not None:
                    tariffs.append(obj)
            return tariffs
        
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
            raise ValueError(f"ERROR - File not found at: {path}")
            return []

        try:
            # Open and load the JSON file
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"ERROR - Failed to decode JSON: {e}")
            return []
        except Exception as e:
            raise ValueError(f"ERROR - Unexpected error while reading file: {e}")
            return []

        # Check if 'tariffs' key exists and is a list
        tariffs = data.get('tariffs', [])
        if not isinstance(tariffs, list):
            raise ValueError("ERROR - 'tariffs' key missing or not a list in JSON data.")
            return []

        return tariffs

    def get_tariff(self, tariff_id: Optional[str] = None) -> Optional[object]:
        """
        Retrieve a specific tariff object based on its ID.

        Args:
            tariff_id (Optional[str]): Tariff ID to search for. If None, uses self.tariff_id.

        Returns:
            Optional[object]: Tariff object if found, otherwise None.
        """
        tariffs = []
        check = self.check_id(tariff_id) # type: ignore
        if not check:
            raise Exception(f"Tariff ID {tariff_id} does not exist.")
        tariffs = self.get_tariffs()
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
        response = self.api_instance.get_tariff_by_id(self.v,tariff_id)# type: ignore
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
            tariff_id = tariffs[index].id
            return tariff_id
        raise IndexError("Index out of range")
    
    def set_id(self, tariff_id: str) -> None:
        """
        Set the default tariff ID for the instance.

        Args:
            tariff_id (str): Tariff ID to set.
        """
        check = self.check_id(tariff_id)
        if not check:
            raise Exception(f"Tariff ID {tariff_id} does not exist.")
        self.tariff_id = tariff_id
        return

    def check_id(self, tariff_id: str) -> bool:
        """
        Check whether the given tariff ID exists among available tariffs.

        Args:
            tariff_id (str): The tariff ID to verify.

        Returns:
            bool: True if tariff exists, False otherwise.
        """
        tariffs = self.get_tariffs()

        # Extrahera alla tillgängliga ID:n (använd .id om objekt, annars dict)
        available_ids = [
            getattr(t, 'id', None) if not isinstance(t, dict) else t.get('id')
            for t in tariffs
        ]

        return tariff_id in available_ids

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
    #==========================Continuous Functions============================
    def _update_tariffs_loop(self, interval_seconds: int):
        """
        Background loop that periodically fetches all tariffs.

        This function runs in a separate thread and continuously updates tariff data
        at a fixed interval, placing the latest result in a queue.

        Args:
            interval_seconds (int): Number of seconds between each update cycle.
        """
        while True:
            try:
                tariffs = self.get_tariffs()
                self.tariffs_queue.put(tariffs)
                #print(f"[{datetime.datetime.now()}] Tariffs updated.") # Debugg
            except Exception as e:
                raise ValueError(f"Error during tariffs update: {e}") # Debugg
            time.sleep(interval_seconds)

    def _update_single_tariff_loop(self, tariff_id: str, time_interval: datetime.timedelta):
        """
        Background loop to periodically update a specific tariff.

        Continuously checks if the time interval has passed, and if so, fetches
        an updated version of the specified tariff and places it in a queue.

        Args:
            tariff_id (str): The ID of the tariff to update.
            time_interval (datetime.timedelta): Minimum duration to wait between updates.
        """
        while True:
            now = datetime.datetime.now()
            if self.last_updated is None or now - self.last_updated >= time_interval:
                try:
                    tariff = self.get_tariff(tariff_id)
                    self.single_tariff_queue.put(tariff)
                    self.last_updated = now
                    #print(f"[{now}] Tariff '{tariff_id}' updated.") # Debugg
                except Exception as e:
                    raise ValueError(f"Error during single tariff update: {e}")
            time.sleep(time_interval.total_seconds())
    #To use continus API interactions
    def start_tariffs_background_update(self, interval_seconds: int = 60):
        """
        Starts a background thread that regularly updates all tariffs.

        Args:
            interval_seconds (int): Time interval between updates (in seconds).
        """
        thread = threading.Thread(
            target=self._update_tariffs_loop,
            args=(interval_seconds,),
            daemon=True
        )
        thread.start()

    def start_single_tariff_background_update(self, tariff_id: Optional[str] = None, time_interval: datetime.timedelta = datetime.timedelta(minutes=1)):
        """
        Starts a background thread that updates a single tariff on a time interval.

        Args:
            tariff_id (str, optional): ID of the tariff to update. Defaults to class value.
            time_interval (timedelta): Time between updates.

        Raises:
            ValueError: If no tariff_id is given or it does not exist.
        """
        if tariff_id is None:
            if self.tariff_id is not None:
                tariff_id = self.tariff_id
            else:
                raise ValueError("No tariff_id provided or set.")
        elif not self.check_id(tariff_id):
            raise ValueError(f"Tariff ID '{tariff_id}' does not exist.")

        thread = threading.Thread(
            target=self._update_single_tariff_loop,
            args=(tariff_id, time_interval),
            daemon=True
        )
        thread.start()
    #After thred is startet use this functions
    def get_latest_tariffs(self):
        """
        Returns the most recently fetched full tariffs, if available.

        Returns:
            list | None: Latest tariffs or None if queue is empty.
        """
        if not self.tariffs_queue.empty():
            return self.tariffs_queue.get()
        return None

    def get_latest_single_tariff(self):
        """
        Returns the most recently updated single tariff, if available.

        Returns:
            object | None: Latest tariff object or None if queue is empty.
        """
        if not self.single_tariff_queue.empty():
            return self.single_tariff_queue.get()
        return None
    #==========================Helper Functions============================
    def dict_to_tariff(self, data: dict) -> Tariff:
        try:
            # Clean ISO date with timezone
            last_updated = isoparse(data.get("lastUpdated")) if data.get("lastUpdated") else None # type: ignore

            # Construct raw dicts for nested models
            valid_period_dict = {
                "from_including": data["validPeriod"]["fromIncluding"],
                "to_excluding": data["validPeriod"]["toExcluding"]
            } if "validPeriod" in data else None

            tariff_data = {
                "id": data.get("id"),
                "name": data.get("name"),
                "description": data.get("description"),
                "product": data.get("product"),
                "company_name": data.get("companyName"),
                "company_org_no": data.get("companyOrgNo"),
                "direction": data.get("direction"),
                "time_zone": data.get("timeZone"),
                "last_updated": last_updated,
                "valid_period": valid_period_dict,
                "billing_period": data.get("billingPeriod"),
                "fixed_price": data.get("fixedPrice"),
                "energy_price": data.get("energyPrice"),
                "power_price": data.get("powerPrice"),
            }

            return Tariff(**tariff_data)

        except Exception as e:
            raise ValueError(f"[ERROR] Failed to convert dict to Tariff: {e}")
            return None # type: ignore

    class Price:
        """
        Container class for price-related logic (fixed, energy, power).

        This class holds submodules to calculate or retrieve prices and cost calculations
        for energy and power based on a specific tariff.
        """

        api_PriceInstant = tariff_api.TariffApi
        tariff_id = str

        def __init__(self,parent) -> None:
            """
            Initializes the price class with a reference to its parent Tariff instance.

            Args:
                parent (Tariff): Instance of the parent class Tariff.
            """
            self.parent = parent
            self.energy = self.Energy(self) # Initialize Energy as a subcomponent
            self.power = self.Power(self)  # Initialize Power as a subcomponent

            self.last_updated = None
            self.cost_queue = q.Queue()  # to hold the latest cost value
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
                    valid_from = comp.valid_period.from_including # type: ignore
                    valid_to = comp.valid_period.to_excluding # type: ignore

                    if isinstance(valid_from, str):
                        valid_from = datetime.datetime.strptime(valid_from, "%Y-%m-%d").date()
                    if isinstance(valid_to, str):
                        valid_to = datetime.datetime.strptime(valid_to, "%Y-%m-%d").date()

                    valid_ok = valid_from <= date_input < valid_to

                if not valid_ok:
                    continue

                # If no recurring_periods, component is always active
                if not hasattr(comp, "recurring_periods") or not comp.recurring_periods: # type: ignore
                    return comp

                # Check if the time is within any active recurring periods
                for period in comp.recurring_periods: # type: ignore
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
            try:
                tariff = self.parent.get_tariff(tariff_id)
                components = getattr(tariff.energy_price, "components", [])
            except Exception as e:
                raise ValueError(f"[ERROR] Failed in get_energy_price: {e}")
                raise e
            
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
                        "costFunction": getattr(tariff.power_price,"costFunction",None),
                        "peakIdentificationSettings": getattr(comp, "peak_identification_settings", None)
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
        #==========================Helper Functions================================
        def extract_price_value(self, price_obj: Union[dict, object]) -> float:
            """
            Extracts a numeric price (preferably including VAT) from a dict or object.

            Args:
                price_obj (dict or object): A price dictionary or object.

            Returns:
                float: Extracted price value.

            Raises:
                ValueError: If no valid price could be found.
            """
            # Helper to normalize dict keys (lowercase, remove underscores)
            def normalize_key(k: str) -> str:
                return k.replace("_", "").lower()

            if isinstance(price_obj, dict):
                # Normalize keys
                norm = {normalize_key(k): v for k, v in price_obj.items()}
                if "priceincvat" in norm:
                    return float(norm["priceincvat"])
                elif "priceexvat" in norm:
                    return float(norm["priceexvat"])

            # Object with 'price' attribute
            try:
                price_attr = price_obj.price  # type: ignore
                if isinstance(price_attr, (float, int)):
                    return float(price_attr)
                elif isinstance(price_attr, dict):
                    norm = {normalize_key(k): v for k, v in price_attr.items()}
                    if "priceincvat" in norm:
                        return float(norm["priceincvat"])
                    elif "priceexvat" in norm:
                        return float(norm["priceexvat"])
            except AttributeError:
                pass

            # Object is a wrapper with a 'price' key that contains a dict
            try:
                price_data = price_obj["price"]  # type: ignore
                if isinstance(price_data, (float, int)):
                    return float(price_data)
                elif isinstance(price_data, dict):
                    norm = {normalize_key(k): v for k, v in price_data.items()}
                    if "priceincvat" in norm:
                        return float(norm["priceincvat"])
                    elif "priceexvat" in norm:
                        return float(norm["priceexvat"])
            except (TypeError, KeyError):
                pass

            raise ValueError(f"Could not extract price from object: {price_obj}")

        def extract_price_function(self, price_obj: Union[dict, object]) -> float:
            """
            Extracts a numerical price from a price object.

            Supports multiple input formats such as dicts or objects with price attributes.

            Args:
                price_obj (Union[dict, object]): Price object or dictionary.

            Returns:
                float: Extracted price (preferably including VAT).

            Raises:
                ValueError: If no valid price can be extracted.
            """

            # === EARLY EXIT if price_obj is already a price dict ===
            if isinstance(price_obj, dict) and "costFunction" in price_obj:
                return price_obj["costFunction"]

            # If object with .costFunction attribute
            try:
                cost_function = price_obj.costFunction # type: ignore
                if isinstance(cost_function, str):
                    return cost_function # type: ignore
            except AttributeError:
                pass

            # If dict with 'costFunction' key nested
            try:
                cost_data = price_obj["costFunction"] # type: ignore
                if isinstance(cost_data, str):
                    return cost_data # type: ignore
                elif isinstance(cost_data, dict) and "costFunction" in cost_data:
                    return cost_data["costFunction"]
            except (KeyError, TypeError):
                pass

            raise ValueError("Could not extract costFunction from the input object.")
    
        class Energy:
            """
            Handles energy price-related logic, such as retrieving component prices
            and computing operational energy cost over time.

            Methods may fallback to class-wide energy data if no explicit input is given.
            """
            tariff_id = str
            energy_data = [{"datetime":None,"kW":None}]
            def __init__(self,parent) -> None:
                """
                Initializes the Energy class with a reference to its parent Price instance.

                Args:
                    parent (Price): Instance of the parent class Price.
                """
                self.parent = parent
                self.last_updated = None
                self.cost_queue = q.Queue()  # to hold the latest cost value
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

            def set_data(self, energy_data_input: list[dict[str, Union[str, float]]]) -> list[dict[str, Union[str, float]]]:
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
                            dp["datetime"].isoformat() # type: ignore
                            if isinstance(dp["datetime"], datetime.datetime) # type: ignore
                            else str(dp["datetime"]) # type: ignore
                        )
                        cleaned_data.append({"datetime": dt_str, "kW": dp["kW"]}) # type: ignore
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
                    key=lambda x: datetime.datetime.fromisoformat(x["datetime"]) # type: ignore
                )
                return self.energy_data # type: ignore

            def get_mean(self, energy_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> float:
                """
                Calculate the mean energy value from a list of dicts with 'kW'.

                Args:
                    energy_data_input (list[dict]): Each dict must have a 'kW' key.

                Returns:
                    float: Mean kW value.
                """
                if energy_data_input is not None:
                    energy_data = energy_data_input
                else:
                    energy_data = self.energy_data

                if not energy_data or not isinstance(energy_data, list):
                    raise ValueError("Energy data must be a non-empty list of dicts.")

                mean_value = sum(d["kW"] for d in energy_data) / len(energy_data) # type: ignore
                return mean_value
                        
            def get_duration(self, energy_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> datetime.timedelta:
                """
                Calculate duration between first and last timestamps in the data.

                Args:
                    data (list): List of data dicts with 'datetime' key.

                Returns:
                    datetime.timedelta: Duration.
                """
                if energy_data_input is not None:
                    energy_data = energy_data_input
                else:
                    energy_data = self.energy_data

                if len(energy_data) < 2:
                    raise ValueError("Not enough energy data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in energy_data] # type: ignore
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def get_optimal_start(self, energy_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> datetime.datetime:
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
                # If no energy_data is given use class set data
                if energy_data_input is not None:
                    energy_data = energy_data_input
                else:
                    energy_data = self.energy_data

                if not isinstance(energy_data, list) or len(energy_data) < 2:
                    raise ValueError("Not enough data points to calculate duration.")

                # Calculate duration from first to last timestamp
                start_time = datetime.datetime.fromisoformat(energy_data[0]["datetime"]) # type: ignore
                end_time = datetime.datetime.fromisoformat(energy_data[-1]["datetime"]) # type: ignore
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
                            hour_price = sum(self.parent.extract_price_value(comp["price"]) for comp in energy_components)
                            total_price += hour_price

                        except Exception:
                            total_price = float("inf")
                            break
                    if total_price < lowest_total_price:
                        lowest_total_price = total_price
                        best_start = check_time

                    check_time += datetime.timedelta(hours=1)
                #print(f"total_price={total_price}")
                return best_start # type: ignore
            
            def get_cost(self, now: datetime.datetime, kW: float) -> float: # type: ignore
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
                    energy_components = self.parent.get_energy_price(tariff_id, now)
                    for comp in energy_components:
                        # Sum up all price components (e.g., energy, grid fee, taxes, etc.)
                        price_per_kWh = self.parent.extract_price_value(comp["price"])
                        # Calculate cost as price per kWh multiplied by the power usage (kW)
                        cost = price_per_kWh * kW
                        return float(cost)

                except Exception as e:
                    # If price lookup fails, return infinite cost (or optionally log the error)
                    raise ValueError(f"Error calculating price at {now}: {e}")
                    return float("inf")

            def get_operation_cost(self, start_time: datetime.datetime, time_duration: Union[str, datetime.timedelta], energy_data_input: Optional[list[dict[str, Union[str, float]]]]) -> float:
                """
                Compute the cost of energy usage over a specified interval.

                Args:
                    start_time (datetime.datetime): Starting point of the operation.
                    time_duration (Union[str, datetime.timedelta]): Operation length as a string ("HH:MM:SS") or timedelta.
                    energy_data_input (Optional[list]): Optional list of data points. If None, uses class-stored energy data.

                Returns:
                    float: Total calculated energy cost.

                Raises:
                    Exception: If no tariff ID is set or data is missing.
                """

                if self.tariff_id is None:
                    raise Exception("No tariff_id is set for energy class")
                # Use default tariff
                tariff_id = self.tariff_id
                # If no energy_data is given use class set data
                if energy_data_input is not None:
                    energy_data = energy_data_input
                else:
                    energy_data = self.energy_data

                # Calculate mean power usage from the provided power data (e.g., from "peak" values)
                energy_mean = self.get_mean(energy_data) # type: ignore

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
                        energy_components = self.parent.get_energy_price(tariff_id,current_time)
                        for comp in energy_components:
                            # Extract and sum price values from all components (e.g., grid cost, tax, etc.)
                            hour_price = self.parent.extract_price_value(comp["price"]) # type: ignore

                        # Multiply hourly price by average power usage to get cost for this hour
                        total_price += hour_price * energy_mean # type: ignore

                    except Exception:
                        # If an error occurs (e.g., missing price data), assume operation fails and set cost to infinite
                        total_price = float("inf")
                        break
                    # Advance time by one hour
                    current_time += datetime.timedelta(hours=1)
                # Return total cost for the time interval
                return total_price

            #==========================Continuous Functions============================
            # Internal loop that runs in background
            def _cost_update_loop(self, kW, interval_seconds):
                """
                Update function for cost
                """
                while True:
                    now = datetime.datetime.now()
                    try:
                        cost = self.get_cost(now, kW)
                        self.last_updated = now
                        self.cost_queue.put(cost)  # Store cost in queue
                    except Exception as e:
                        raise ValueError(f"Error during cost update: {e}")
                    time.sleep(interval_seconds)

            def _energy_data_recording_loop(self, kW: float, interval_seconds: int):
                """
                Continuously records kW energy data at the given interval by calling set_data.

                Args:
                    kW (float): Power consumption to record.
                    interval_seconds (int): Time in seconds between recordings.
                """
                while True:
                    now = datetime.datetime.now()
                    try:
                        # Prepare data point
                        data_point = {"datetime": now, "kW": kW}
                        self.set_data([data_point])  # Store using your existing method
                        #print(f"[{now}] Energy data recorded: {kW} kW") # Debugg
                    except Exception:
                        #print(f"Error during energy data recording: {e}") # Debugg
                        time.sleep(interval_seconds)

            # Functions to start the background thread
            def start_background_energy_recording(self, kW: float, interval_seconds: int = 60):
                """
                Starts a background thread that records energy data (datetime + kW) every interval.

                Args:
                    kW (float): Power usage to record.
                    interval_seconds (int): Time between recordings.
                """
                thread = threading.Thread(
                    target=self._energy_data_recording_loop,
                    args=(kW, interval_seconds),
                    daemon=True  # Stops when the main program exits
                )
                thread.start()

            def start_background_cost_updates(self, kW: float, interval_seconds: int = 60):
                """
                Starts a background thread that updates the cost every `interval_seconds` seconds.
                """
                thread = threading.Thread(
                    target=self._cost_update_loop,
                    args=(kW, interval_seconds),
                    daemon=True  # Stops when the main program ends
                )
                thread.start()
            # After starting threds use the get funtions
            def get_latest_cost(self):
                """
                Retrieves the most recent cost from the queue, if available.
                """
                if not self.cost_queue.empty():
                    return self.cost_queue.get()
                return None

            def get_latest_energy_data(self):
                """
                Returns the most recent energy data point, if available.
                """
                if self.energy_data:
                    return self.energy_data[-1]
                return None


        class Power:
            """
            Handles power pricing, especially peak-based power tariff calculations.

            Supports ISO8601 durations and structured tariff component evaluation.
            Defaults to class power data if no explicit list is provided.
            """
            tariff_id = None
            power_data = [{"datetime":None,"peak":None}]
            def __init__(self,parent) -> None:
                """
                Initializes the Power class with a reference to its parent Price instance.

                Args:
                    parent (Price): Instance of the parent class Price.
                """
                self.parent = parent
                self.last_updated = None
                self.cost_queue = q.Queue()  # to hold the latest cost value
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

            def set_data(self, power_data_input: list[dict[str, Union[str, float]]]) -> list[dict[str, Union[str, float]]]:
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
                            dp["datetime"].isoformat() # type: ignore
                            if isinstance(dp["datetime"], datetime.datetime) # type: ignore
                            else str(dp["datetime"]) # type: ignore
                        )
                        cleaned_data.append({"datetime": dt_str, "kW": dp["kW"]}) # type: ignore
                    elif isinstance(dp, (tuple, list)) and len(dp) == 2:
                        dt, kW = dp
                        if isinstance(dt, datetime.datetime):
                            cleaned_data.append({"datetime": dt.isoformat(), "kW": kW})
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
                    key=lambda x: datetime.datetime.fromisoformat(x["datetime"]) # type: ignore
                )
                return self.power_data # type: ignore

            def get_mean(self, power_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> float:
                """
                Calculate the mean power value from a list of values.

                Args:
                    power_data (list[float]): List of power values.

                Returns:
                    float: Mean value.
                """
                if power_data_input is not None:
                    power_data = power_data_input
                else:
                    power_data = self.power_data

                if not power_data or not isinstance(power_data, list):
                    raise ValueError("Energy data must be a non-empty list of dicts.")

                mean_value = sum(d["kW"] for d in power_data) / len(power_data) # type: ignore
                return mean_value
            
            def get_duration(self, power_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> datetime.timedelta:
                """
                Calculate duration between first and last timestamps in the data.

                Args:
                    data (list): List of data dicts with 'datetime' key.

                Returns:
                    datetime.timedelta: Duration.
                """

                if power_data_input is not None:
                    power_data = power_data_input
                else:
                    power_data = self.power_data

                if len(power_data) < 2:
                    raise ValueError("Not enough power data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in power_data]# type: ignore
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def get_optimal_start(self, power_data_input: Optional[list[dict[str, Union[str, float]]]] = None) -> datetime.datetime:
                """
                Finds the optimal start time within the next 24h that minimizes
                total power cost including peak cost impact

                Args:
                    power_data (list[dict], optional): List of power data points.

                Returns:
                    datetime.datetime: Optimal start time.

                Raises:
                    ValueError: If input data is missing or invalid.
                """
                #print(f"in optimal_start. power_data={power_data} ")
                if power_data_input is None:
                    power_data = self.power_data
                else: 
                    power_data = power_data_input

                if not isinstance(power_data, list) or len(power_data) < 2:
                    raise ValueError("Not enough data points to calculate duration.")

                # Calculate duration from first to last timestamp
                start_time = datetime.datetime.fromisoformat(power_data[0]["datetime"]) # type: ignore
                end_time = datetime.datetime.fromisoformat(power_data[-1]["datetime"]) # type: ignore
                #print(f"start_time={start_time} and end_time={end_time}")
                duration = end_time - start_time
                #print(f"duraiton={duration}")
                hours = int(duration.total_seconds() // 3600)

                if hours <= 0:
                    raise ValueError("Duration must be at least one hour.")

                # Loop through potential start times over the next 24 hours
                now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
                latest_start = now + datetime.timedelta(hours=(24 - hours))  # latest valid start

                best_start = None
                lowest_cost = float("inf")

                check_time = now
                while check_time <= latest_start:
                    # Simulated power_data to given start time
                    simulated_data = []
                    for i in range(hours):
                        entry = power_data[i % len(power_data)]  # wrap if not enough
                        new_time = check_time + datetime.timedelta(hours=i)
                        simulated_data.append({
                            "datetime": new_time.isoformat(),
                            "kW": float(entry["kW"]) # type: ignore
                        })

                    # Calculate operation cost with peak-rules
                    cost = self.get_operation_cost(
                        start_time=check_time,
                        time_duration=duration,
                        power_data_input=simulated_data
                    )

                    # Saves the best price point
                    if cost < lowest_cost:
                        lowest_cost = cost
                        best_start = check_time

                    check_time += datetime.timedelta(hours=1)

                return best_start # type: ignore
            
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
                    power_components = self.parent.get_power_price(tariff_id, now)

                    # Sum up all price components (e.g., power, grid fee, taxes, etc.)
                    price_per_kWh = sum(self.parent.extract_price_value(comp["price"]) for comp in power_components)

                    # Calculate cost as price per kWh multiplied by the power usage (kW)
                    cost = price_per_kWh * kW
                    return cost

                except Exception as e:
                    # If price lookup fails, return infinite cost (or optionally log the error)
                    raise ValueError(f"Error calculating price at {now}: {e}")
                    return float("inf")

            def get_operation_cost(self, start_time: datetime.datetime, time_duration: Union[str, datetime.timedelta], power_data_input: Optional[list[dict[str, Union[str, float]]]]) -> float:
                """
                Calculate power cost using tariff peak rules.

                Args:
                    start_time (datetime.datetime): Start time for operation cost window.
                    time_duration (str | timedelta): Duration string ("HH:MM:SS") or a timedelta object.
                    power_data_input (Optional[list]): Optional power data. Falls back on class-stored data if None.

                Returns:
                    float: Total calculated cost.

                Raises:
                    ValueError: On missing or invalid data.
                """
                if self.tariff_id is None:
                    raise Exception("No tariff_id is set for power class")

                # Parse duration
                if isinstance(time_duration, str):
                    h, m, s = map(int, time_duration.split(":"))
                    duration = datetime.timedelta(hours=h, minutes=m, seconds=s)
                elif isinstance(time_duration, datetime.timedelta):
                    duration = time_duration
                else:
                    raise ValueError("time_duration must be string or timedelta")

                tariff_id = self.tariff_id
                power_data = power_data_input if power_data_input else self.power_data

                if not power_data:
                    raise ValueError("No power data available")

                # Assumption: One value per HOUR
                sampling_interval = datetime.timedelta(hours=1)

                # Determine how many data points are needed to cover duration
                n_points_needed = int(duration.total_seconds() // sampling_interval.total_seconds())

                # Slice or repeat power data to cover required duration
                values = [float(d["kW"]) for d in power_data] # type: ignore
                if len(values) < n_points_needed:
                    repeats = (n_points_needed // len(values)) + 1
                    values = (values * repeats)[:n_points_needed]
                else:
                    values = values[:n_points_needed]

                # Generate artificial timestamps
                simulated_data = []
                for i, kW in enumerate(values):
                    fake_time = start_time + i * sampling_interval
                    simulated_data.append({"datetime": fake_time.isoformat(), "kW": kW})

                total_cost = 0.0
                power_components = self.parent.get_power_price(tariff_id, start_time)

                peak_values = {}

                for comp in power_components:
                    price_val = self.parent.extract_price_value(comp["price"])
                    peak_settings = comp.get("peakIdentificationSettings", {})
                    component_ref = comp.get("reference", "main")
                    #print(f"peak_settings type: {type(peak_settings)}") # Debugg

                    if not peak_settings:
                        mean_kw = self.get_mean(simulated_data)  # type: ignore
                        total_cost += mean_kw * price_val
                        continue

                    # Peak settings with defults
                    peak_func = getattr(peak_settings, "peak_function", "peak(base)")
                    peak_duration = isodate.parse_duration(getattr(peak_settings, "peak_duration", "PT1H"))
                    peak_period = isodate.parse_duration(getattr(peak_settings, "peak_identification_period", "P1D"))
                    n_peaks = int(getattr(peak_settings, "number_of_peaks_for_average_calculation", 1)) # type: ignore

                    # Group into daily periods (or simulated periods)
                    period_buckets: dict[int, list[dict]] = {}
                    for entry in simulated_data:
                        dt = datetime.datetime.fromisoformat(entry["datetime"])
                        offset = (dt - start_time).total_seconds()
                        period_index = int(offset // peak_period.total_seconds())
                        period_buckets.setdefault(period_index, []).append(entry)

                    for period_data in period_buckets.values():
                        windows: dict[int, list[float]] = {}
                        for entry in period_data:
                            dt = datetime.datetime.fromisoformat(entry["datetime"])
                            window_index = int((dt - start_time).total_seconds() // peak_duration.total_seconds())
                            windows.setdefault(window_index, []).append(entry["kW"])  # type: ignore

                        max_peaks = [max(group) for group in windows.values() if group]
                        top_peaks = sorted(max_peaks, reverse=True)[:n_peaks]
                        peak_avg = sum(top_peaks) / len(top_peaks) if top_peaks else 0

                        peak_values[component_ref] = peak_avg
                        #Fall back so tekverk api dont brake code
                        if "base" not in peak_values:
                            peak_values["base"] = peak_values.get("main", 0.0)

                        if "reactive" not in peak_values:
                            peak_values["reactive"] = 0.0

                        result_kw = self.evaluate_peak_function(peak_func, peak_values)
                        total_cost += result_kw * price_val

                return total_cost       
            #==========================Helper Functions================================
            @staticmethod
            def parse_iso_duration(duration_str: str) -> datetime.timedelta:
                """
                Convert ISO 8601 duration strings like 'PT1H' or 'P1D' to timedelta.
                """
                try:
                    return isodate.parse_duration(duration_str)
                except Exception as e:
                    raise ValueError(f"Invalid ISO duration '{duration_str}': {e}")
            from typing import Dict
            @staticmethod
            def evaluate_peak_function(function_str: str, peak_values: Dict[str, float]) -> float:
                """
                Evaluates a peak function expression like "peak(main)", "max(0, peak(base) - peak(high)/2)", etc.
                Supports legacy references like "peak(base)" and "peak(reactive)".
                
                Args:
                    function_str (str): The peak function string.
                    peak_values (dict): Mapping from reference name to peak value.
                        Must include keys like "main", "base", "high", etc. if referenced in function_str.

                Returns:
                    float: The result of evaluating the function.

                Raises:
                    ValueError: If a required reference is missing or evaluation fails.
                """

                # Handle both new and legacy keys
                def peak_replacer(match):
                    ref = match.group(1)
                    if ref not in peak_values:
                        raise ValueError(f"Missing peak value for reference: '{ref}'")
                    return str(peak_values[ref])

                # Replace all peak(...) references
                expr = re.sub(r"peak\((\w+)\)", peak_replacer, function_str)

                # Safe builtins
                allowed = {
                    "max": max,
                    "min": min,
                    "abs": abs,
                    "round": round,
                    "math": math
                }

                try:
                    return eval(expr, {"__builtins__": None}, allowed)
                except Exception as e:
                    raise ValueError(f"Could not evaluate peakFunction '{function_str}': {e}")
            #==========================Continuous Functions============================
            # Internal loop that runs in background
            def _cost_update_loop(self, kW, interval_seconds):
                """
                Update function for cost
                """
                while True:
                    now = datetime.datetime.now()
                    try:
                        cost = self.get_cost(now, kW)
                        self.last_updated = now
                        self.cost_queue.put(cost)  # Store cost in queue
                    except Exception as e:
                        raise ValueError(f"Error during cost update: {e}")
                    time.sleep(interval_seconds)

            def _power_data_recording_loop(self, kW: float, interval_seconds: int):
                """
                Continuously records kW power data at the given interval by calling set_power_data.

                Args:
                    kW (float): Power consumption to record.
                    interval_seconds (int): Time in seconds between recordings.
                """
                while True:
                    now = datetime.datetime.now()
                    try:
                        # Prepare a data point
                        data_point = {"datetime": now, "kW": kW}
                        self.set_data([data_point])  # Store using your custom method
                        #print(f"[{now}] Power data recorded: {kW} kW") # Debugg
                    except Exception as e:
                        raise ValueError(f"Error during power data recording: {e}")
                    time.sleep(interval_seconds)
            
            # Functions to start the background thread
            def start_background_cost_updates(self, kW: float, interval_seconds: int = 60):
                """
                Starts a background thread that updates the cost every `interval_seconds` seconds.
                """
                thread = threading.Thread(
                    target=self._cost_update_loop,
                    args=(kW, interval_seconds),
                    daemon=True  # Stops when the main program ends
                )
                thread.start()
            
            def start_background_power_recording(self, kW: float, interval_seconds: int = 60):
                """
                Starts a background thread that records power data (datetime + kW) every interval.

                Args:
                    kW (float): Power value to record.
                    interval_seconds (int): Time between recordings.
                """
                thread = threading.Thread(
                    target=self._power_data_recording_loop,
                    args=(kW, interval_seconds),
                    daemon=True  # Daemon threads stop when main program exits
                )
                thread.start()

            # After starting threds use the get funtions
            def get_latest_cost(self):
                """
                Retrieves the most recent cost from the queue, if available.
                """
                if not self.cost_queue.empty():
                    return self.cost_queue.get()
                return None