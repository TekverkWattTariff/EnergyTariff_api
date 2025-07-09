import unittest
from api_InteractionLayer import Tariffs
from datetime import datetime

class TestTariffs(unittest.TestCase):

    def setUp(self):
        self.tariff = Tariffs(v="V1", url="http://dummy.url", tariff_id="test-id")

    def test_get_company(self):
        result = self.tariff.get_company("test-id")
        self.assertIsNotNone(result)

    def test_get_companys(self):
        result = self.tariff.get_companys()
        self.assertIsInstance(result, list)

    def test_get_tariff(self):
        result = self.tariff.get_tariff()
        self.assertIsNotNone(result)

    def test_get_tariff_byName(self):
        company = self.tariff.get_companys()[0] if self.tariff.get_companys() else None
        if company:
            result = self.tariff.get_tariff_byName("SomeName", company)
            self.assertIsNotNone(result)

    def test_get_tariffs_ids(self):
        ids = self.tariff.get_tariffs_ids()
        self.assertIsInstance(ids, list)

    def test_get_tariffs_names(self):
        names = self.tariff.get_tariffs_names()
        self.assertIsInstance(names, list)

    def test_get_id(self):
        index = 0
        result = self.tariff.get_id(index)
        self.assertIsNotNone(result)

    def test_set_id(self):
        self.tariff.set_id("new-id")
        self.assertEqual(self.tariff.tariff_id, "new-id")

    def test_chek_id(self):
        self.assertTrue(self.tariff.chek_id("test-id"))

class TestPrice(unittest.TestCase):

    def setUp(self):
        self.parent = Tariffs(v="V1", url="http://dummy.url", tariff_id="test-id")
        self.price = self.parent.Price(self.parent)

    def test_set_id(self):
        self.price.set_id("new-id")
        self.assertEqual(self.price.tariff_id, "new-id")

    def test_get_fixed_price(self):
        dt = datetime.now()
        result = self.price.get_fixed_price("test-id", dt)
        self.assertIsNotNone(result)

    def test_get_energy_price(self):
        dt = datetime.now()
        result = self.price.get_energy_price("test-id", dt)
        self.assertIsNotNone(result)

    def test_get_power_price(self):
        dt = datetime.now()
        result = self.price.get_power_price("test-id", dt)
        self.assertIsNotNone(result)

    def test_get_price(self):
        dt = datetime.now()
        result = self.price.get_price("test-id", dt)
        self.assertIsNotNone(result)

    def test_set_data(self):
        dummy_data = {"energy": 0.3}
        self.price.set_data(dummy_data)

    def test_get_duration(self):
        result = self.price.get_duration()
        self.assertIsInstance(result, int)

    def test_extract_price_value(self):
        dummy_price = {"value": 100}
        val = self.price.extract_price_value(dummy_price)
        self.assertEqual(val, 100)

    def test_extract_price_function(self):
        dummy_price = {"function": lambda: 5}
        result = self.price.extract_price_function(dummy_price)
        self.assertEqual(result(), 5)

class TestPower(unittest.TestCase):

    def setUp(self):
        self.parent = Tariffs(v="V1", url="http://dummy.url", tariff_id="test-id")
        self.power = self.parent.Price.Power(self.parent)

    def test_set_id(self):
        self.power.set_id("new-id")
        self.assertEqual(self.power.tariff_id, "new-id")

    def test_set_data(self):
        self.power.set_data({"power": 100})  # Kontrollera vad den förväntar sig

    def test_get_duration(self):
        result = self.power.get_duration()
        self.assertIsInstance(result, int)

    def test_extract_price_value(self):
        result = self.power.extract_price_value({"value": 300})
        self.assertEqual(result, 300)

    def test_extract_price_function(self):
        result = self.power.extract_price_function({"function": lambda: 42})
        self.assertEqual(result(), 42)

if __name__ == "__main__":
    unittest.main()
