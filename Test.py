""""""
import sys
import os
import datetime

import api_InteractionLayer
print("\nStart of TEST")
url = "https://api.tekniskaverken.net/subscription/public/v0/tariffs"
#url = "https://api.goteborgenergi.cloud/gridtariff/v0/tariffs"
Tariff = api_InteractionLayer.Tariffs("v0",url)
Tariff2 = api_InteractionLayer.Tariffs("V0")
Price = Tariff.Price(Tariff)
Power = Price.Power(Price)
#print(f"{tariff.get_api_teriffs_names()}") #debugg
tariffs = Tariff.get_tariffs()
path = "C://Users/Local/Desktop/Projekts/Test/tariffs-response_tekniska-verken.json"
tariffs2 = Tariff2.get_tariffs_byJson(path)
"""
print("Tillgängliga prislistor:\n")
for i, tariff in enumerate(tariffs):
    print(f"{i}: {tariff.name} -> {tariff.id}")
"""
# Användarinmatning
val = input("Ange siffran för det abonnemang du vill se info om: ")

try:
    index = int(val)
    chosen_tariff = tariffs[index]
    print(f"Du valde: {chosen_tariff.name}")
    print(f"ID: {chosen_tariff.id}")

    print(f"\nFrome json file with path: {path}")
    print(f"Du valde: {chosen_tariff.name}")
    print(f"ID: {chosen_tariff.id}")
    chosen_index = index
    
    # Här anropar du API-funktion
    print(f"Trying to fetch tariff with ID: {chosen_tariff.id}")
    tariff_data = Tariff.get_tariff(chosen_tariff.id)

except (ValueError, IndexError) as e:
    print("Fel: Ogiltig inmatning.")

id = Tariff.get_id(chosen_index)
#ids = Tariff.get_tariffs_ids()
#print(f"Ids: {ids}")
names = Tariff.get_tariffs_names()
#print(f"Tariff names: {names}")
company = Tariff.get_company(id)
print(f"Company: {company}")
id = Tariff.get_id_byName(names[chosen_index],company)

now = datetime.datetime.now()
result = Price.get_price(id, now)

print("{")
for category, components in result.items():
    print(f"'{category}': [")
    for i, comp in enumerate(components):
        prefix = "\n" if i > 0 else ""
        print(f"{prefix}{comp},")
    print("],")
print("}")

now = datetime.datetime.now().replace(hour=5, minute=30, second=0, microsecond=0)
result = Price.get_price(id, now)

print("{")
for category, components in result.items():
    print(f"'{category}': [")
    for i, comp in enumerate(components):
        prefix = "\n" if i > 0 else ""
        print(f"{prefix}{comp},")
    print("],")
print("}")


power_raw_data = [
    {"datetime": datetime.datetime(2025, 5, 1, 12), "peak": 50},
    {"datetime": datetime.datetime(2025, 5, 1, 13), "peak": 30},
    {"datetime": datetime.datetime(2025, 5, 1, 14), "peak": 50},
    {"datetime": datetime.datetime(2025, 5, 1, 15), "peak": 75},
    {"datetime": datetime.datetime(2025, 5, 1, 16), "peak": 80},
    {"datetime": datetime.datetime(2025, 5, 1, 17), "peak": 75},
    {"datetime": datetime.datetime(2025, 5, 1, 18), "peak": 25},
    {"datetime": datetime.datetime(2025, 5, 1, 19), "peak": 10},
    {"datetime": datetime.datetime(2025, 5, 1, 20), "peak": 7},
    {"datetime": datetime.datetime(2025, 5, 1, 21), "peak": 4}
]
Power.set_id(id)
power_data = Power.set_data(power_raw_data)
start_time = Power.get_optimal_start(power_data)
print(f"Optimal time to start: {start_time}")