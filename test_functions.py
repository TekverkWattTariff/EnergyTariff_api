import unittest
import threading
import time
import queue
from datetime import datetime
from unittest.mock import patch, MagicMock
from api_InteractionLayer import Tariffs

class TestTariffs(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("api_InteractionLayer.Tariffs.get_tariffs")
        self.mock_get_tariffs = self.patcher.start()

        self.mock_tariff = MagicMock()
        self.mock_tariff.id = "tariff-123"
        self.mock_tariff.name = "Tariff A"
        self.mock_tariff.company_name = "Company X"
        self.mock_tariff.tariff_id = "tariff-123"
        self.mock_get_tariffs.return_value = [self.mock_tariff]

        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")

    def tearDown(self):
        self.patcher.stop()

    def test_get_tariffs_ids(self):
        self.assertEqual(self.tariff.get_tariffs_ids(), ["tariff-123"])

    def test_get_tariffs_names(self):
        self.assertEqual(self.tariff.get_tariffs_names(), ["Tariff A"])

    def test_get_companys(self):
        self.assertEqual(self.tariff.get_companys(), ["Company X"])

    def test_get_id_byName(self):
        self.tariff.get_companys = lambda: ["Company X"]
        result = self.tariff.get_id_byName("Tariff A", "Company X")
        self.assertEqual(result, "tariff-123")
class TestPriceMethods(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("api_InteractionLayer.Tariffs.get_tariffs")
        self.mock_get_tariffs = self.patcher.start()

        self.mock_tariff = MagicMock()
        self.mock_tariff.id = "tariff-123"
        self.mock_tariff.name = "Tariff A"
        self.mock_tariff.company_name = "Company X"
        self.mock_get_tariffs.return_value = [self.mock_tariff]

        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")

    def tearDown(self):
        self.patcher.stop()

    def test_extract_price_value_variants(self):
        cases = [
            ({"priceIncVat": 1.5}, 1.5),
            ({"priceExVat": 2.5}, 2.5),
            ({"price": {"priceIncVat": 3.5}}, 3.5),
            ({"price": {"priceExVat": 4.5}}, 4.5),
        ]
        for input_data, expected in cases:
            result = self.tariff.price.extract_price_value(input_data)
            self.assertEqual(result, expected)

    def test_extract_price_function(self):
        result = self.tariff.price.extract_price_function({"costFunction": "FixedCost"})
        self.assertEqual(result, "FixedCost")
class TestPowerBackgroundUpdate(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("api_InteractionLayer.Tariffs.get_tariffs")
        self.mock_get_tariffs = self.patcher.start()

        self.mock_tariff = MagicMock()
        self.mock_tariff.id = "tariff-123"
        self.mock_tariff.name = "Tariff A"
        self.mock_tariff.company_name = "Company X"
        self.mock_get_tariffs.return_value = [self.mock_tariff]

        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")

        self.tariff.energy.get_cost = MagicMock(return_value=2.5)
        self.tariff.power.get_cost = MagicMock(return_value=2.5)

    def tearDown(self):
        self.patcher.stop()

    def test_background_cost_update_loop(self):
        self.tariff.power.start_background_cost_updates(kW=2.5, interval_seconds=1)
        time.sleep(1.5)
        latest_cost = self.tariff.power.get_latest_cost()
        self.assertIsNotNone(latest_cost)
        self.assertEqual(latest_cost, 2.5)


class MockPower:
    def __init__(self):
        self.cost_queue = queue.Queue()
        self.last_updated = None

    def get_cost(self, now, kW):
        return 2.5

    def start_background_cost_updates(self, kW, interval_seconds=1):
        def loop():
            while True:
                cost = self.get_cost(datetime.now(), kW)
                self.last_updated = datetime.now()
                self.cost_queue.put(cost)
                time.sleep(interval_seconds)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def get_latest_cost(self):
        if not self.cost_queue.empty():
            return self.cost_queue.get()
        return None


if __name__ == "__main__":
    unittest.main()
