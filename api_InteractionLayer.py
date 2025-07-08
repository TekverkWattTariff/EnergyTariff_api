"""This code initializes the API client and defines functions based on the tariff API"""
import sys
import os
import datetime

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
    on time intervals and provided consumption data.

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
    
    def __init__(self,v,url,tariff_id = None) -> None:
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
        url = url.replace("/v0/tariffs", "")
        self.url = url

        # Create OpenAPI configuration
        config = Configuration(host=url)

        # Initialize API client
        client = ApiClient(configuration=config)
        self.api_instance = tariff_api.TariffApi(api_client=client)
        #print(f"api_instance type: {type(self.api_instance)}") #Debugg
        pass
    
    def get_company(self,tariff_id):
        """
        Returns the company name of the given tariff ID.

        Args:
            tariff_id (str): ID of the tariff.

        Returns:
            str: Name of the company associated with the tariff.
        """
        self.chek_id(tariff_id)
        tariff = self.get_tariff(tariff_id)
        return tariff.company_name
    
    def get_companys(self):
        """
        Returns a list of all company names in the API.

        Returns:
            list[str]: List of company names.
        """
        companys = []
        for tariff in self.get_tariffs():
            companys.append(tariff.company_name)
        return companys

    def get_tariffs(self):
        """
        Returns all tariffs available in the API.

        Returns:
            list: List of tariff objects.
        """
        response = self.api_instance.get_tariffs(self.v)
        return response.tariffs
    
    def get_tariff(self,tariff_id=None):
        """
        Returns the tariff object for a given tariff ID.

        Args:
            tariff_id (str): ID of the tariff.

        Returns:
            object | None: Tariff object or None if not found.
        """
        tariffs = self.get_tariffs()
        for t in tariffs:
            if t.id == tariff_id:
                return t
        return None
    
    def get_tariff_byName(self,tariff_name,company):
        """
        Returns a tariff object based on its name and company.

        Args:
            tariff_name (str): Name of the tariff.
            company (str): Name of the company.

        Returns:
            object: Tariff object.
        """
        tariff_id = self.get_id_byName(tariff_name,company)
        response = self.api_instance.get_tariff_by_id(self.v,tariff_id)
        return response.tariff
    
    def get_tariffs_ids(self):
        """
        Returns a list of all tariff IDs available in the API.

        Returns:
            list[str]: List of tariff IDs.
        """
        ids = []
        tariffs = self.get_tariffs()
        for tariff in tariffs:
            ids.append(tariff.id)
        return ids
    
    def get_tariffs_names(self):
        """
        Returns a list of all tariff names available in the API.

        Returns:
            list[str]: List of tariff names.
        """
        names = []
        for tariff in self.get_tariffs():
            names.append(tariff.name)
        return names
    
    def get_id(self,index):
        """
        Returns a tariff ID at the given index in the list of tariffs.

        Args:
            index (int): Index of the tariff.

        Returns:
            str: Tariff ID.
        """
        tariffs = self.get_tariffs()
        tariff = tariffs[index]
        #print(f"Selected index: {index}, tariff id: {tariff.id}")  # Debug
        return tariff.id
    
    def set_id(self,tariff_id):
        """
        Sets the default class tariff ID.

        Args:
            tariff_id (str): Tariff ID to set.
        """
        self.tariff_id = tariff_id
        return

    def chek_id(self,tariff_id):
        """
        Returns the given tariff ID or the class default if None.

        Args:
            tariff_id (str or None): Tariff ID or None.

        Returns:
            str: Valid tariff ID.
        """
        if tariff_id == None:
                tariff_id = self.tariff_id
        return tariff_id

    def get_id_byName(self,tariff_name,company):
        """
        Returns the ID of a tariff by its name and company.

        Args:
            tariff_name (str): Name of the tariff.
            company (str): Name of the company.

        Returns:
            str: Tariff ID.
        """
        if company not in self.get_companys():
            print(f"company {company} dos not exist in api")

        index = next(
            (i for i, t in enumerate(self.get_tariffs()) 
                if t.name == tariff_name and t.company_name == company), 
            None
        )
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
            self.tariff_id = parent.tariff_id
            return
        
        def set_id(self,tariff_id):
            """
            Sets the default class tariff ID.

            Args:
                tariff_id (str): Tariff ID to set.
            """
            self.tariff_id = tariff_id
            return

        def find_matching_time_period(self, components, datetime_input):
            """
            Helper function to find the appropriate component based on datetime_input.
            Components without recurring_periods are considered always active.
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

        def get_fixed_price(self, tariff_id, datetime_input):
            """
            Retrieve all fixed price components for the given tariff and datetime.
            Returns a list of matching components with price and metadata.
            
            Args:
                tariff_id (str): The tariff identifier.
                datetime_input (datetime.datetime): The datetime to check validity against.

            Returns:
                list: List of dicts with 'id', 'name', 'price', and 'pricedPeriod'.
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

        def get_energy_price(self, tariff_id, datetime_input):
            """
            Retrieve the energy price component for the given tariff and datetime.
            Returns a default zero price dict if no matching component is found.

            Args:
                tariff_id (str): The tariff identifier.
                datetime_input (datetime.datetime): The datetime for which to retrieve the price.

            Returns:
                dict: A dictionary containing price information with keys:
                    'price' (dict with 'priceExVat', 'priceIncVat', 'currency'),
                    and 'pricedPeriod' (str).
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
        
        def get_power_price(self, tariff_id, datetime_input):
            """
            Retrieve the power price component for the given tariff and datetime.
            Returns a default zero price dict if no matching component is found.

            Args:
                tariff_id (str): The tariff identifier.
                datetime_input (datetime.datetime): The datetime for which to retrieve the price.

            Returns:
                dict: A dictionary containing price information with keys:
                    'price' (dict with 'priceExVat', 'priceIncVat', 'currency'),
                    and 'pricedPeriod' (str).
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

        def get_price(self, tariff_id, datetime_input):
            """
            Retrieve all three price components (fixed, energy, power) for the given tariff and datetime.

            Args:
                tariff_id (str): The tariff identifier.
                datetime_input (datetime.datetime): The datetime for which to retrieve the prices.

            Returns:
                dict: A dictionary with keys 'fixed_price', 'energy_price', and 'power_price',
                    each containing a price dictionary as returned by the respective methods.
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
                self.energy_data = [{"datetime":None,int:None}]
                self.tariff_id = parent.tariff_id
                pass

            def set_id(self,tariff_id):
                """
                Sets the default class tariff ID.

                Args:
                    tariff_id (str): Tariff ID to set.
                """
                self.tariff_id = tariff_id
                return

            def set_data(self, energy_data_input):
                """
                Accepts and stores energy data.

                Supports:
                - A single dictionary with 'datetime' and 'Consumption' keys
                - A list of such dictionaries
                - A list of (datetime, Consumption) tuples

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
                    if isinstance(dp, dict) and "datetime" in dp and "Consumption" in dp:
                        # Ensure datetime is ISO string
                        dt_str = (
                            dp["datetime"].isoformat()
                            if isinstance(dp["datetime"], datetime.datetime)
                            else str(dp["datetime"])
                        )
                        cleaned_data.append({"datetime": dt_str, "Consumption": dp["Consumption"]})
                    elif isinstance(dp, (tuple, list)) and len(dp) == 2:
                        dt, Consumption = dp
                        if isinstance(dt, datetime.datetime):
                            cleaned_data.append({"datetime": dt.isoformat(), "Consumption": Consumption})
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

            def get_mean(self,energy_data):
                """
                Calculate the mean energy value from a list of values.

                Args:
                    energy_data (list[float]): List of energy values.

                Returns:
                    float: Mean value.
                """
                mean_value = sum(energy_data)/len(energy_data)
                return mean_value
            
            def get_duration(self):
                """
                Calculate duration between the first and last energy data point.

                Returns:
                    datetime.timedelta: Time duration.

                Raises:
                    ValueError: If fewer than two data points exist.
                """
                if len(self.energy_data) < 2:
                    raise ValueError("Not enough energy data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in self.energy_data]
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def extract_price_value(self,price_obj):
                """
                Extracts a float price value from a nested price object or dict.
                Prefers 'priceIncVat', then 'priceExVat', then a direct float.

                Args:
                    price_obj (object or dict): Price container.

                Returns:
                    float: Numeric price.

                Raises:
                    ValueError: If no valid price found.
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

            def extract_price_function(self, price_obj):
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

            def get_optimal_start(self, energy_data=None):
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
                        #print(f"current_time: {current_time}")
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
                print(f"total_price={total_price}")
                return best_start
            
        
        class Power:
            """
            Subclass of Price for power data handling and optimization logic.

            Handles:
            - Storing and processing time-series power data.
            - Calculating durations and averages.
            - Finding optimal start times for minimizing power costs.
            """
            tariff_id = None
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
                self.power_data = [{"datetime":None,int:None}]
                self.tariff_id = parent.tariff_id
                pass

            def set_id(self,tariff_id):
                """
                Sets the default class tariff ID.

                Args:
                    tariff_id (str): Tariff ID to set.
                """
                self.tariff_id = tariff_id
                return

            def set_data(self, power_data_input):
                """
                Accepts and stores power data.

                Supports:
                - A single dictionary with 'datetime' and 'peak' keys
                - A list of such dictionaries
                - A list of (datetime, peak) tuples

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
                    if isinstance(dp, dict) and "datetime" in dp and "peak" in dp:
                        # Ensure datetime is ISO string
                        dt_str = (
                            dp["datetime"].isoformat()
                            if isinstance(dp["datetime"], datetime.datetime)
                            else str(dp["datetime"])
                        )
                        cleaned_data.append({"datetime": dt_str, "peak": dp["peak"]})
                    elif isinstance(dp, (tuple, list)) and len(dp) == 2:
                        dt, peak = dp
                        if isinstance(dt, datetime.datetime):
                            cleaned_data.append({"datetime": dt.isoformat(), "peak": peak})
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

            def get_mean(self,power_data):
                """
                Calculate the mean power value from a list of values.

                Args:
                    power_data (list[float]): List of power values.

                Returns:
                    float: Mean value.
                """
                mean_value = sum(power_data)/len(power_data)
                return mean_value
            
            def get_duration(self):
                """
                Calculate duration between the first and last power data point.

                Returns:
                    datetime.timedelta: Time duration.

                Raises:
                    ValueError: If fewer than two data points exist.
                """
                if len(self.power_data) < 2:
                    raise ValueError("Not enough power data points to determine duration.")
                #Converts to datetime obj
                datetimes = [datetime.datetime.fromisoformat(p["datetime"]) for p in self.power_data]
                #Calculate time difrence
                duration = datetimes[-1] - datetimes[0] #End - Start
                return duration
            
            def extract_price_value(self,price_obj):
                """
                Extracts a float price value from a nested price object or dict.
                Prefers 'priceIncVat', then 'priceExVat', then a direct float.

                Args:
                    price_obj (object or dict): Price container.

                Returns:
                    float: Numeric price.

                Raises:
                    ValueError: If no valid price found.
                """
                #print(f"In extract_price: {price_obj}") #Debug

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

            def extract_price_function(self, price_obj):
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

            def get_optimal_start(self, power_data=None):
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
                        #print(f"current_time: {current_time}")
                        try:
                            power_components = self.parent.get_energy_price(tariff_id,current_time)
                            hour_price = sum(self.extract_price_value(comp["price"]) for comp in power_components)
                            total_price += hour_price

                        except Exception:
                            total_price = float("inf")
                            break
                    if total_price < lowest_total_price:
                        lowest_total_price = total_price
                        best_start = check_time

                    check_time += datetime.timedelta(hours=1)
                print(f"total_price={total_price}")
                return best_start
