# Test2.py
import requests
from api_InteractionLayer import Tariffs  # Importera din klass
import pprint

# Ange API-url och version
url = "https://api.goteborgenergi.cloud/gridtariff"
#url = "https://api.tekniskaverken.net/subscription/public"
version = "v0"

# Skapa ett Tariffs-objekt
api = Tariffs(v=version, url=url)

try:
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    pprint.pprint(data)
except Exception as e:
    print("Fel vid direkt API-anrop:", e)

try:
    response = api.api_instance.get_tariffs(version)
    print("Typ av svar:", type(response))
    print("Innehåll:", response)
except Exception as e:
    print("Fel vid direkt API-anrop:", e)

# Hämta alla tariffs
try:
    tariffs = api.get_tariffs()
    pprint.pprint(tariffs)  # Snygg utskrift av innehållet
except Exception as e:
    print("Ett fel uppstod:", e)
