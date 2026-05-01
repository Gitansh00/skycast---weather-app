import unittest
from unittest.mock import patch, MagicMock
from weather import parse_current_weather, parse_forecast, get_current_weather


MOCK_CURRENT = {
    "name": "London",
    "sys": {"country": "GB"},
    "main": {"temp": 15.6, "feels_like": 13.2, "humidity": 72, "pressure": 1012},
    "weather": [{"description": "broken clouds", "icon": "04d"}],
    "wind": {"speed": 5.2},
    "visibility": 10000,
}

MOCK_FORECAST = {
    "list": [
        {
            "dt_txt": "2024-06-01 12:00:00",
            "main": {"temp_max": 18.0, "temp_min": 11.0, "humidity": 65},
            "weather": [{"description": "clear sky", "icon": "01d"}],
        },
        {
            "dt_txt": "2024-06-02 12:00:00",
            "main": {"temp_max": 20.0, "temp_min": 13.0, "humidity": 55},
            "weather": [{"description": "few clouds", "icon": "02d"}],
        },
    ]
}


class TestParseCurrentWeather(unittest.TestCase):
    def test_city_and_country(self):
        result = parse_current_weather(MOCK_CURRENT)
        self.assertEqual(result["city"], "London")
        self.assertEqual(result["country"], "GB")

    def test_temp_is_rounded(self):
        result = parse_current_weather(MOCK_CURRENT)
        self.assertEqual(result["temp"], 16)

    def test_wind_converted_to_kmh(self):
        result = parse_current_weather(MOCK_CURRENT)
        self.assertAlmostEqual(result["wind_speed"], 18.7, places=0)

    def test_visibility_converted_to_km(self):
        result = parse_current_weather(MOCK_CURRENT)
        self.assertEqual(result["visibility"], 10.0)

    def test_description_is_titled(self):
        result = parse_current_weather(MOCK_CURRENT)
        self.assertEqual(result["description"], "Broken Clouds")


class TestParseForecast(unittest.TestCase):
    def test_returns_correct_number_of_days(self):
        result = parse_forecast(MOCK_FORECAST)
        self.assertEqual(len(result), 2)

    def test_temp_max_is_rounded(self):
        result = parse_forecast(MOCK_FORECAST)
        self.assertEqual(result[0]["temp_max"], 18)

    def test_forecast_has_required_keys(self):
        result = parse_forecast(MOCK_FORECAST)
        for key in ["date", "temp_max", "temp_min", "description", "icon", "humidity"]:
            self.assertIn(key, result[0])


class TestGetCurrentWeather(unittest.TestCase):
    @patch("weather.requests.get")
    def test_raises_on_404(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_resp
        with self.assertRaises(Exception):
            get_current_weather("FakeCity123")

    @patch("weather.requests.get")
    def test_successful_call(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = MOCK_CURRENT
        mock_get.return_value = mock_resp
        result = get_current_weather("London")
        self.assertEqual(result["city"], "London")


if __name__ == "__main__":
    unittest.main()
