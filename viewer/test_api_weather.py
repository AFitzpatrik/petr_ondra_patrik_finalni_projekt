import requests
from django.core.cache import cache
from django.test import TestCase
from viewer.api_weather import get_weather_for_city
from unittest.mock import patch, MagicMock


class GetWeatherForCityTests(TestCase):

    def setUp(self):
        print('-' * 80)
        print(f"Spouští se test: {self._testMethodName}")
        cache.clear()

    @patch('viewer.api_weather.requests.get')
    def test_get_weather_for_city(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'weather': [{'description': 'jasno'}],
            'main': {'temp': 25.20},
        }
        mock_get.return_value = mock_response
        result = get_weather_for_city('Plzeň')

        self.assertIsNotNone(result)
        self.assertEqual(result['description'], 'jasno')
        self.assertEqual(result['temperature'], 25.2)

    @patch('viewer.api_weather.requests.get')
    def test_get_weather_for_city_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = get_weather_for_city('Město_neexistuje')

        self.assertIsNone(result)

    @patch('viewer.api_weather.requests.get')
    def test_get_weather_for_city_exception_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Simulace timeoutu")
        result = get_weather_for_city('Plzeň')

        self.assertIsNone(result)

    @patch('viewer.api_weather.requests.get')
    def test_get_weather_for_city_invalid_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'weather': [{'description': 'jasno'}],
        }
        mock_get.return_value = mock_response

        result = get_weather_for_city('Plzeň')

        self.assertIsNone(result)
