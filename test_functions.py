import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from api_InteractionLayer import Tariffs


class TestTariffs(unittest.TestCase):
    def setUp(self):
        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")

    @patch.object(Tariffs, "get_tariff")
    def test_get_tariff(self, mock_get_tariff):
        mock_tariff = MagicMock(tariff_id="tariff-123")
        mock_get_tariff.return_value = mock_tariff
        result = self.tariff.get_tariff("tariff-123")
        self.assertEqual(result.tariff_id, "tariff-123")

    @patch.object(Tariffs, "get_tariffs")
    def test_get_tariffs_ids(self, mock_get_tariffs):
        mock_tariffs = [
            MagicMock(tariff_id="id-0"),
            MagicMock(tariff_id="id-1"),
            MagicMock(tariff_id="id-2")
        ]
        mock_get_tariffs.return_value = mock_tariffs
        result = self.tariff.get_tariffs_ids()
        self.assertEqual(result, ["id-0", "id-1", "id-2"])

    @patch.object(Tariffs, "get_tariffs")
    def test_get_tariffs_names(self, mock_get_tariffs):
        mock_tariffs = [
            MagicMock(name="name-0"),
            MagicMock(name="name-1")
        ]
        # Simulera att .name returnerar str
        for i, t in enumerate(mock_tariffs):
            t.name = f"name-{i}"
        mock_get_tariffs.return_value = mock_tariffs
        result = self.tariff.get_tariffs_names()
        self.assertEqual(result, ["name-0", "name-1"])

    @patch.object(Tariffs, "get_tariffs")
    def test_get_id_valid_index(self, mock_get_tariffs):
        mock_tariff  = MagicMock(id="abc")
        mock_get_tariffs.return_value = [mock_tariff ]
        result = self.tariff.get_id(0)
        self.assertEqual(result, "abc")

    @patch.object(Tariffs, "get_tariffs", return_value=[])
    def test_get_id_out_of_range(self, mock_get_tariffs):
        with self.assertRaises(IndexError):
            self.tariff.get_id(0)

    @patch.object(Tariffs, "get_tariffs")
    def test_set_and_check_id(self, mock_get_tariffs):
        mock_tariff  = MagicMock(id="my-id")
        mock_get_tariffs.return_value = [mock_tariff]
        self.tariff.set_id("my-id")
        self.assertTrue(self.tariff.chek_id("my-id"))
        self.assertFalse(self.tariff.chek_id("missing-id"))

    @patch.object(Tariffs, "get_tariffs")
    def test_get_companys(self, mock_get_tariffs):
        mock_tariffs = [
            MagicMock(company_name="Company-0"),
            MagicMock(company_name="Company-1")
        ]
        mock_get_tariffs.return_value = mock_tariffs
        result = self.tariff.get_companys()
        self.assertEqual(result, ["Company-0", "Company-1"])

    @patch.object(Tariffs, "get_tariff")
    @patch.object(Tariffs, "chek_id")
    def test_get_company(self, mock_chek_id, mock_get_tariff):
        mock_chek_id.return_value = True
        mock_tariff = MagicMock(company_name="TestCo")
        mock_get_tariff.return_value = mock_tariff
        result = self.tariff.get_company("tariff-123")
        self.assertEqual(result, "TestCo")

    @patch.object(Tariffs, "get_tariffs")
    def test_get_id_byName(self, mock_get_tariffs):
        mock_tariff = MagicMock()
        mock_tariff.name = "Standard"
        mock_tariff.company_name = "CompanyX"
        mock_tariff.id = "id-42"
        mock_get_tariffs.return_value = [mock_tariff]
        self.tariff.get_companys = lambda: ["CompanyX"]
        result = self.tariff.get_id_byName("Standard", "CompanyX")
        self.assertEqual(result, "id-42")


class TestPrice(unittest.TestCase):
    def setUp(self):
        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")
        self.price = self.tariff.Price(self.tariff)

    def test_extract_price_value(self):
        price_data = {"price": {"price_inc_vat": 250.0}}
        result = self.price.Power.extract_price_value(self.price.Power, price_data)
        self.assertEqual(result, 250.0)

    def test_extract_price_function(self):
        price_data = {"costFunction": "FixedCost"}
        result = self.price.Power.extract_price_function(self.price.Power, price_data)
        self.assertEqual(result, "FixedCost")


class TestEnergyAndPower(unittest.TestCase):
    def setUp(self):
        self.tariff = Tariffs(v="V1", url="https://fake.api", tariff_id="tariff-123")
        self.price = self.tariff.Price(self.tariff)
        self.energy = self.price.Energy(self.price)
        self.power = self.price.Power(self.price)

    def test_set_energy_data_single_entry(self):
        dt = datetime.now()
        data = {"datetime": dt, "kW": 2.5}
        result = self.energy.set_data(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["kW"], 2.5)

    def test_set_power_data_multiple_entries(self):
        dt1 = datetime.now()
        dt2 = dt1 + timedelta(hours=1)
        data = [{"datetime": dt1, "kW": 1.0}, {"datetime": dt2, "kW": 3.0}]
        result = self.power.set_data(data)
        self.assertEqual(len(result), 2)

    def test_get_mean_with_input_list_of_dicts(self):
        energy_data = [
            {"datetime": "2024-01-01T12:00", "kW": 2.0},
            {"datetime": "2024-01-01T13:00", "kW": 4.0},
            {"datetime": "2024-01-01T14:00", "kW": 6.0},
        ]
        result = self.energy.get_mean(energy_data)
        self.assertEqual(result, 4.0)

    def test_get_duration_valid_data(self):
        dt1 = datetime.now()
        dt2 = dt1 + timedelta(hours=2)
        data = [
            {"datetime": dt1.isoformat(), "kW": 1.0},
            {"datetime": dt2.isoformat(), "kW": 3.0}
        ]
        duration = self.energy.get_duration(data)
        self.assertEqual(duration, timedelta(hours=2))

    @patch.object(Tariffs.Price, "get_energy_price")
    def test_get_optimal_start_valid(self, mock_get_energy_price):
        start = datetime.now().replace(minute=0, second=0, microsecond=0)
        data = [
            {"datetime": (start + timedelta(hours=i)).isoformat(), "kW": 1.0}
            for i in range(3)
        ]
        self.energy.energy_data = data
        mock_get_energy_price.return_value = [{"price": {"price_inc_vat": 1.0}}]
        result = self.energy.get_optimal_start()
        self.assertIsInstance(result, datetime)

    @patch.object(Tariffs.Price, "get_energy_price")
    def test_get_operation_mean_cost(self, mock_get_energy_price):
        start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        data = [
            {"datetime": (start_time + timedelta(hours=i)).isoformat(), "kW": 2.0}
            for i in range(2)
        ]
        self.energy.energy_data = data
        mock_get_energy_price.return_value = [{"price": {"price_inc_vat": 1.0}}]
        cost = self.energy.get_operation_mean_cost(start_time, "02:00:00", data)
        self.assertGreaterEqual(cost, 0.0)

    @patch.object(Tariffs.Price, "get_energy_price")
    def test_get_cost_valid(self, mock_get_energy_price):
        now = datetime.now()
        mock_get_energy_price.return_value = [{"price": {"price_inc_vat": 1.0}}]
        cost = self.energy.get_cost(now, 2.0)
        self.assertEqual(cost, 2.0)


if __name__ == "__main__":
    unittest.main()