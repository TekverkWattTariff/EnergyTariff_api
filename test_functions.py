import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from api_InteractionLayer import Tariffs


class TestTariffs(unittest.TestCase):
    def setUp(self):
        self.tariff = Tariffs(v="V1", url="https://fake.api")

    @patch.object(Tariffs, "get_tariff")
    def test_get_tariff(self, mock_get_tariff):
        mock_tariff = MagicMock()
        mock_tariff.tariff_id = "tariff-123"
        mock_get_tariff.return_value = mock_tariff

        result = self.tariff.get_tariff("tariff-123")
        self.assertEqual(result, mock_tariff)

    @patch.object(Tariffs, "get_tariffs")
    def test_get_tariffs_ids(self, mock_get_tariffs):
        mock_tariffs = [
        MagicMock(),
        MagicMock(),
        MagicMock()
        ]
        # Explicitly set string values
        mock_tariffs[0].tariff_id = "id-0"
        mock_tariffs[1].tariff_id = "id-1"
        mock_tariffs[2].tariff_id = "id-2"
        mock_get_tariffs.return_value = mock_tariffs

        result = self.tariff.get_tariffs_ids()
        self.assertEqual(result, ["id-0", "id-1", "id-2"])

    @patch.object(Tariffs, "get_tariffs")
    def test_get_id_valid_index(self, mock_get_tariffs):
        mock_t = MagicMock()
        mock_t.tariff_id  = "abc"
        mock_get_tariffs.return_value = [mock_t]

        result = self.tariff.get_id(0)
        self.assertEqual(result, "abc")

    @patch.object(Tariffs, "get_tariffs", return_value=[])
    def test_get_id_out_of_range(self, mock_get_tariffs):
        with self.assertRaises(IndexError):
            self.tariff.get_id(0)

    @patch.object(Tariffs, "get_tariffs")
    def test_set_and_check_id(self, mock_get_tariffs):
        mock_t = MagicMock()
        mock_t.tariff_id  = "my-id"
        mock_get_tariffs.return_value = [mock_t]

        self.tariff.set_id("my-id")
        self.assertTrue(self.tariff.chek_id("my-id"))
        self.assertFalse(self.tariff.chek_id("missing-id"))


class TestPrice(unittest.TestCase):
    def setUp(self):
        self.tariff = Tariffs(v="V1", url="https://fake.api")
        self.price = self.tariff.Price(self.tariff)

    def test_extract_price_value(self):
        print("in string try: price_data:", 300)
        result = self.price.Power.extract_price_value(self.price.Power, {"price": 300})
        self.assertEqual(result, 300)


if __name__ == "__main__":
    unittest.main()