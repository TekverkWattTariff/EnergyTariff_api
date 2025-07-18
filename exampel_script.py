""""""
#import sys
#import os
import time
import datetime

import api_InteractionLayer
print("\nStart of TEST")
url = "https://api.tekniskaverken.net/subscription/public/v0/tariffs"
#url = "https://api.goteborgenergi.cloud/gridtariff/v0/tariffs"
path = "C://Users/Local/Desktop/Projekts/Test/tariffsresponse.json"
Tariff = api_InteractionLayer.Tariffs("v0",url)
Tariff2 = api_InteractionLayer.Tariffs("V0",None,path)
#print(f"{tariff.get_api_teriffs_names()}") #debugg
tariffs = Tariff.get_tariffs()


print(f"Trisf by Json: {Tariff2}")
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
    print(f"Fel: Ogiltig inmatning. {e}")

id = Tariff.get_id(chosen_index) # type: ignore
id2 = Tariff2.get_id(chosen_index) # type: ignore
names = Tariff.get_tariffs_names()
company = Tariff.get_company(id)
print(f"Company: {company}")
id = Tariff.get_id_byName(names[chosen_index],company) # type: ignore

now = datetime.datetime.now()
result = Tariff.price.get_price(id, now)
result2 = Tariff2.price.get_price(id2, now)
"""
print("Tariff 1: {")
for category, components in result.items():
    print(f"'{category}': [")
    for i, comp in enumerate(components):
        prefix = "\n" if i > 0 else ""
        print(f"{prefix}{comp},")
    print("],")
print("}")

print("Tariff 2: {")
for category, components in result2.items():
    print(f"'{category}': [")
    for i, comp in enumerate(components):
        prefix = "\n" if i > 0 else ""
        print(f"{prefix}{comp},")
    print("],")
print("}")
"""
now = datetime.datetime.now().replace(hour=5, minute=30, second=0, microsecond=0)
result = Tariff.price.get_price(id, now)
"""
print("{")
for category, components in result.items():
    print(f"'{category}': [")
    for i, comp in enumerate(components):
        prefix = "\n" if i > 0 else ""
        print(f"{prefix}{comp},")
    print("],")
print("}")
"""

power_raw_data = [
    {"datetime": datetime.datetime(2025, 5, 1, 0), "kW": 5},
    {"datetime": datetime.datetime(2025, 5, 1, 1), "kW": 4},
    {"datetime": datetime.datetime(2025, 5, 1, 2), "kW": 3},
    {"datetime": datetime.datetime(2025, 5, 1, 3), "kW": 3},
    {"datetime": datetime.datetime(2025, 5, 1, 4), "kW": 4},
    {"datetime": datetime.datetime(2025, 5, 1, 5), "kW": 6},
    {"datetime": datetime.datetime(2025, 5, 1, 6), "kW": 12},
    {"datetime": datetime.datetime(2025, 5, 1, 7), "kW": 25},
    {"datetime": datetime.datetime(2025, 5, 1, 8), "kW": 35},
    {"datetime": datetime.datetime(2025, 5, 1, 9), "kW": 45},
    {"datetime": datetime.datetime(2025, 5, 1, 10), "kW": 55},
    {"datetime": datetime.datetime(2025, 5, 1, 11), "kW": 60},
    {"datetime": datetime.datetime(2025, 5, 1, 12), "kW": 50},
    {"datetime": datetime.datetime(2025, 5, 1, 13), "kW": 30},
    {"datetime": datetime.datetime(2025, 5, 1, 14), "kW": 50},
    {"datetime": datetime.datetime(2025, 5, 1, 15), "kW": 75},
    {"datetime": datetime.datetime(2025, 5, 1, 16), "kW": 80},
    {"datetime": datetime.datetime(2025, 5, 1, 17), "kW": 75},
    {"datetime": datetime.datetime(2025, 5, 1, 18), "kW": 25},
    {"datetime": datetime.datetime(2025, 5, 1, 19), "kW": 10},
    {"datetime": datetime.datetime(2025, 5, 1, 20), "kW": 7},
    {"datetime": datetime.datetime(2025, 5, 1, 21), "kW": 4},
    {"datetime": datetime.datetime(2025, 5, 1, 22), "kW": 3},
    {"datetime": datetime.datetime(2025, 5, 1, 23), "kW": 2},
]

Tariff.price.power.set_id(id)
power_data = Tariff.price.power.set_data(power_raw_data)
start_time = Tariff.price.power.get_optimal_start(power_data)
print(f"Optimal time to start: {start_time}")
time_str  = "4:30"
Tariff.price.energy.set_id(id)
operatianal_cost = Tariff.price.energy.get_operation_cost(now,"4:30:00",power_data)
print(f"Cost of using energy for {time_str} is {operatianal_cost}")

now = datetime.datetime.now().replace(year=2026,hour=5, minute=30, second=0, microsecond=0)
power_data = Tariff2.power.set_data(power_raw_data)
Tariff2.price.power.set_id(id2)
operatianal_cost = Tariff2.price.power.get_operation_cost(now,"4:30:00",power_data)
print(f"Cost of using energy for {time_str} is {operatianal_cost}")

# === Exemple på continus functions ===
Tariff2.set_id(id2)
# === STÄLL IN ETT KRAFTVÄRDE (i kW) ===
mock_kw_value = 75  # Exempelvärde

# === STARTA BAKGRUNDSUPPDATERINGAR ===
Tariff2.price.power.start_background_cost_updates(kW=mock_kw_value, interval_seconds=10)
Tariff2.price.power.start_background_power_recording(kW=mock_kw_value, interval_seconds=10)

# === LOOPA FÖR ATT VISA KOSTNAD FRÅN QUEUE ===
print("Kör bakgrundsuppdatering... (CTRL+C för att avsluta)\n")

try:
    while True:
        latest_cost = Tariff2.price.power.get_latest_cost()
        if latest_cost is not None:
            print(f"[{datetime.datetime.now()}] Aktuell beräknad kostnad: {latest_cost:.2f} kr")
        else:
            print("Ingen kostnad tillgänglig ännu...")
        time.sleep(10)

except KeyboardInterrupt:
    print("\nAvslutat av användaren.")